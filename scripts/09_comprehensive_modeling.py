import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'
bbb = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), low_memory=False)
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))

# Sort
bbb = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).reset_index(drop=True)

bbb['is_legal_ball'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
bbb['is_batter_ball'] = bbb['extras_type'] != 'wide'
bbb['ball_total_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']
bbb['is_bowler_extra'] = bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['bowler_runs'] = bbb['runs'] + np.where(bbb['is_bowler_extra'], bbb['extras1_runs'] + bbb['extras_2_runs'], 0)
bowler_dismissals = ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']
bbb['is_bowler_wicket'] = bbb['dismissal_type'].isin(bowler_dismissals)

# Calculate cumulative innings runs and wickets before each ball
bbb['cum_runs'] = bbb.groupby(['match_id', 'innings'])['ball_total_runs'].cumsum() - bbb['ball_total_runs']
bbb['cum_wickets'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket'].astype(int)
bbb['legal_balls_bowled'] = bbb.groupby(['match_id', 'innings'])['is_legal_ball'].cumsum() - bbb['is_legal_ball'].astype(int)
bbb['balls_remaining'] = np.maximum(0, 120 - bbb['legal_balls_bowled'])
bbb['wickets_in_hand'] = 10 - bbb['cum_wickets']

inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['ball_total_runs'].sum().reset_index()
inn1_totals.rename(columns={'ball_total_runs': 'inn1_total'}, inplace=True)
matches_merged = matches[['match_id', 'comp_id', 'revised_target', 'knock_out', 'stage']].merge(
    comps[['comp_id', 'comp_name', 'match_format', 'season']], on='comp_id', how='left'
)
bbb = bbb.merge(inn1_totals, on='match_id', how='left')
bbb = bbb.merge(matches_merged, on='match_id', how='left')

bbb['target'] = np.where(bbb['revised_target'].notnull() & (bbb['revised_target'] > 0),
                         bbb['revised_target'],
                         bbb['inn1_total'] + 1)
bbb['runs_needed'] = np.maximum(0, bbb['target'] - bbb['cum_runs'])
bbb['rrr'] = np.where(
    (bbb['innings'] == 2) & (bbb['balls_remaining'] > 0),
    (bbb['runs_needed'] * 6.0) / bbb['balls_remaining'],
    0.0
)

# Over-by-over baselines
over_baselines = bbb.groupby('overid').agg(
    exp_runs=('bowler_runs', 'mean'),
    exp_wicket=('is_bowler_wicket', 'mean')
).reset_index()
bbb = bbb.merge(over_baselines, on='overid', how='left')

# Pressure definition
p_super_over = bbb['innings'] > 2
p_chase_death = (bbb['innings'] == 2) & (bbb['overid'] >= 16) & (bbb['runs_needed'] > 0) & (bbb['runs_needed'] <= 75) & (bbb['rrr'] >= 7.0) & (bbb['rrr'] <= 24.0)
p_chase_crunch = (bbb['innings'] == 2) & (bbb['overid'].between(11, 15)) & (bbb['rrr'] >= 9.5) & (bbb['rrr'] <= 18.0) & (bbb['wickets_in_hand'] <= 7)
p_chase_close = (bbb['innings'] == 2) & (bbb['balls_remaining'] <= 36) & (bbb['runs_needed'] > 0) & (bbb['runs_needed'] <= 55) & (bbb['rrr'] >= 7.0)
p_chase_collapse = (bbb['innings'] == 2) & (bbb['cum_wickets'] >= 4) & (bbb['runs_needed'] >= 30) & (bbb['balls_remaining'] >= 12) & (bbb['rrr'] <= 20.0)
p_inn1_death = (bbb['innings'] == 1) & (bbb['overid'] >= 16)
p_inn1_collapse = (bbb['innings'] == 1) & (bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 3)

bbb['is_pressure'] = p_super_over | p_chase_death | p_chase_crunch | p_chase_close | p_chase_collapse | p_inn1_death | p_inn1_collapse

# Weighting: IPL is the highest quality league (1.2x), Knockouts (1.2x)
bbb['weight'] = np.where(bbb['match_format'] == 'T20', 1.2, 1.0) * np.where(bbb['knock_out'] == 1, 1.2, 1.0)

print("Data preprocessed successfully.")
print(f"Total balls: {len(bbb)}, Pressure balls: {bbb['is_pressure'].sum()}")

# --- BATTING MODEL ---
print("\n--- RUNNING BATTING MODEL ---")

# Batter Match-level consistency
match_bat = bbb[bbb['is_pressure'] & bbb['is_batter_ball']].groupby(['match_id', 'striker_id', 'striker_name']).agg(
    m_balls=('runs', 'count'),
    m_runs=('runs', 'sum'),
    m_exp_runs=('exp_runs', 'sum'),
    m_dismissals=('is_wicket', 'sum')
).reset_index()
# High impact inning: if faced >= 6 pressure balls, was runs >= exp_runs or SR >= 145?
match_bat['is_impactful'] = (match_bat['m_balls'] >= 6) & ((match_bat['m_runs'] >= match_bat['m_exp_runs']) | ((match_bat['m_runs']/match_bat['m_balls']) >= 1.45))
bat_consistency = match_bat.groupby(['striker_id', 'striker_name']).agg(
    clutch_innings=('m_balls', lambda x: (x >= 6).sum()),
    impactful_innings=('is_impactful', 'sum')
).reset_index()
bat_consistency['consistency_rate'] = np.where(
    bat_consistency['clutch_innings'] > 0,
    bat_consistency['impactful_innings'] / bat_consistency['clutch_innings'],
    0.0
)

# Overall Batting Stats under pressure
bat_p = bbb[bbb['is_pressure'] & bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
    bf_p=('runs', 'count'),
    runs_p=('runs', 'sum'),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum'),
    dots_p=('runs', lambda x: (x == 0).sum()),
    dismissals_p=('is_wicket', 'sum'),
    exp_runs_p=('exp_runs', 'sum'),
    matches_p=('match_id', 'nunique'),
    ipl_balls_p=('match_id', lambda x: (bbb.loc[x.index, 'match_format'] == 'T20').sum())
).reset_index()

# Batting Stats in Normal situations
bat_n = bbb[(~bbb['is_pressure']) & bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
    bf_n=('runs', 'count'),
    runs_n=('runs', 'sum'),
    dismissals_n=('is_wicket', 'sum')
).reset_index()

bat_all = bat_p.merge(bat_n, on=['striker_id', 'striker_name'], how='left').fillna(0)
bat_all = bat_all.merge(bat_consistency, on=['striker_id', 'striker_name'], how='left').fillna(0)

# Filter minimum sample: min 140 pressure balls
bat_qual = bat_all[bat_all['bf_p'] >= 140].copy()

# Compute key metrics
bat_qual['sr_p'] = (bat_qual['runs_p'] / bat_qual['bf_p']) * 100
bat_qual['avg_p'] = bat_qual['runs_p'] / np.maximum(1, bat_qual['dismissals_p'])
bat_qual['dot_pct_p'] = (bat_qual['dots_p'] / bat_qual['bf_p']) * 100
bat_qual['bnd_pct_p'] = ((bat_qual['fours_p'] + bat_qual['sixes_p']) / bat_qual['bf_p']) * 100
bat_qual['runs_above_exp_per_100'] = ((bat_qual['runs_p'] - bat_qual['exp_runs_p']) / bat_qual['bf_p']) * 100

bat_qual['sr_n'] = np.where(bat_qual['bf_n'] > 0, (bat_qual['runs_n'] / bat_qual['bf_n']) * 100, bat_qual['sr_p'])
bat_qual['sr_delta'] = bat_qual['sr_p'] - bat_qual['sr_n']

# Sample reliability weight: K = 100
bat_qual['sample_weight'] = bat_qual['bf_p'] / (bat_qual['bf_p'] + 100)

# Z-scores / Min-Max Normalization for Batting Score
def norm(series):
    s_min, s_max = series.min(), series.max()
    return (series - s_min) / (s_max - s_min) if s_max > s_min else series * 0

# Core Components (weights: Scoring Efficiency 35%, Runs Above Expected 20%, Dismissal Resistance/Avg 15%, Delta Uplift 15%, Consistency 15%)
bat_qual['score_sr'] = norm(bat_qual['sr_p'])
bat_qual['score_rae'] = norm(bat_qual['runs_above_exp_per_100'])
bat_qual['score_avg'] = norm(np.clip(bat_qual['avg_p'], 10, 50))
bat_qual['score_delta'] = norm(np.clip(bat_qual['sr_delta'], -15, 45))
bat_qual['score_cons'] = norm(bat_qual['consistency_rate'])
bat_qual['score_boundary'] = norm(bat_qual['bnd_pct_p'])
bat_qual['score_dot_resist'] = norm(100 - bat_qual['dot_pct_p'])

raw_bat_score = (
    0.25 * bat_qual['score_sr'] +
    0.20 * bat_qual['score_rae'] +
    0.15 * bat_qual['score_avg'] +
    0.15 * bat_qual['score_delta'] +
    0.15 * bat_qual['score_cons'] +
    0.10 * bat_qual['score_boundary']
)

# Apply sample reliability shrinkage towards league median (50.0)
bat_qual['BPRI'] = 100 * (raw_bat_score * bat_qual['sample_weight'] + 0.50 * (1 - bat_qual['sample_weight']))
bat_ranked = bat_qual.sort_values('BPRI', ascending=False).reset_index(drop=True)
bat_ranked['rank'] = bat_ranked.index + 1

print("\n=== TOP 20 BATTERS UNDER PRESSURE (BPRI) ===")
cols_show = ['rank', 'striker_name', 'bf_p', 'runs_p', 'sr_p', 'avg_p', 'sr_delta', 'consistency_rate', 'runs_above_exp_per_100', 'BPRI']
print(bat_ranked[cols_show].head(20).to_string())


# --- BOWLING MODEL ---
print("\n--- RUNNING BOWLING MODEL ---")

# Match-level consistency for bowlers
match_bowl = bbb[bbb['is_pressure']].groupby(['match_id', 'bowler_id', 'bowler_name']).agg(
    m_balls=('is_legal_ball', 'sum'),
    m_runs=('bowler_runs', 'sum'),
    m_exp_runs=('exp_runs', 'sum'),
    m_wickets=('is_bowler_wicket', 'sum')
).reset_index()
# High impact spell: bowled >= 6 legal balls, conceded <= expected runs or took 1+ wickets
match_bowl['is_impactful'] = (match_bowl['m_balls'] >= 6) & ((match_bowl['m_runs'] <= match_bowl['m_exp_runs']) | (match_bowl['m_wickets'] >= 1))
bowl_consistency = match_bowl.groupby(['bowler_id', 'bowler_name']).agg(
    clutch_spells=('m_balls', lambda x: (x >= 6).sum()),
    impactful_spells=('is_impactful', 'sum')
).reset_index()
bowl_consistency['consistency_rate'] = np.where(
    bowl_consistency['clutch_spells'] > 0,
    bowl_consistency['impactful_spells'] / bowl_consistency['clutch_spells'],
    0.0
)

# Overall Bowling Stats under pressure
bowl_p = bbb[bbb['is_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    balls_p=('is_legal_ball', 'sum'),
    runs_p=('bowler_runs', 'sum'),
    wickets_p=('is_bowler_wicket', 'sum'),
    dots_p=('bowler_runs', lambda x: (x == 0).sum()),
    fours_p=('is_four', 'sum'),
    sixes_p=('is_six', 'sum'),
    exp_runs_p=('exp_runs', 'sum'),
    exp_wickets_p=('exp_wicket', 'sum'),
    matches_p=('match_id', 'nunique'),
    ipl_balls_p=('match_id', lambda x: (bbb.loc[x.index, 'match_format'] == 'T20').sum())
).reset_index()

# Normal situations
bowl_n = bbb[~bbb['is_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    balls_n=('is_legal_ball', 'sum'),
    runs_n=('bowler_runs', 'sum'),
    wickets_n=('is_bowler_wicket', 'sum')
).reset_index()

bowl_all = bowl_p.merge(bowl_n, on=['bowler_id', 'bowler_name'], how='left').fillna(0)
bowl_all = bowl_all.merge(bowl_consistency, on=['bowler_id', 'bowler_name'], how='left').fillna(0)

# Filter minimum sample: min 150 legal balls
bowl_qual = bowl_all[bowl_all['balls_p'] >= 150].copy()

bowl_qual['overs_p'] = bowl_qual['balls_p'] / 6.0
bowl_qual['econ_p'] = bowl_qual['runs_p'] / bowl_qual['overs_p']
bowl_qual['sr_p'] = np.where(bowl_qual['wickets_p'] > 0, bowl_qual['balls_p'] / bowl_qual['wickets_p'], 50.0)
bowl_qual['dot_pct_p'] = (bowl_qual['dots_p'] / bowl_qual['balls_p']) * 100
bowl_qual['bnd_conceded_pct_p'] = ((bowl_qual['fours_p'] + bowl_qual['sixes_p']) / bowl_qual['balls_p']) * 100

bowl_qual['overs_saved_p'] = (bowl_qual['exp_runs_p'] - bowl_qual['runs_p']) / bowl_qual['overs_p']
bowl_qual['wickets_above_exp'] = bowl_qual['wickets_p'] - bowl_qual['exp_wickets_p']

bowl_qual['overs_n'] = bowl_qual['balls_n'] / 6.0
bowl_qual['econ_n'] = np.where(bowl_qual['overs_n'] > 0, bowl_qual['runs_n'] / bowl_qual['overs_n'], bowl_qual['econ_p'])
bowl_qual['econ_delta'] = bowl_qual['econ_n'] - bowl_qual['econ_p'] # Positive is better!

# Sample reliability weight: K = 120 balls (20 overs)
bowl_qual['sample_weight'] = bowl_qual['balls_p'] / (bowl_qual['balls_p'] + 120)

# Components (weights: Runs Saved Above Over Par 25%, Economy Rate 20%, Wickets/SR 20%, Consistency 15%, Dot% 10%, Delta Uplift 10%)
bowl_qual['score_runs_saved'] = norm(bowl_qual['overs_saved_p'])
bowl_qual['score_econ'] = norm(15.0 - np.clip(bowl_qual['econ_p'], 5.0, 15.0))
bowl_qual['score_sr'] = norm(40.0 - np.clip(bowl_qual['sr_p'], 8.0, 40.0))
bowl_qual['score_dot'] = norm(bowl_qual['dot_pct_p'])
bowl_qual['score_bnd_suppress'] = norm(35.0 - np.clip(bowl_qual['bnd_conceded_pct_p'], 5.0, 35.0))
bowl_qual['score_delta'] = norm(np.clip(bowl_qual['econ_delta'], -2.0, 3.0))
bowl_qual['score_cons'] = norm(bowl_qual['consistency_rate'])

raw_bowl_score = (
    0.25 * bowl_qual['score_runs_saved'] +
    0.20 * bowl_qual['score_econ'] +
    0.20 * bowl_qual['score_sr'] +
    0.15 * bowl_qual['score_cons'] +
    0.10 * bowl_qual['score_dot'] +
    0.10 * bowl_qual['score_delta']
)

bowl_qual['BoPRI'] = 100 * (raw_bowl_score * bowl_qual['sample_weight'] + 0.50 * (1 - bowl_qual['sample_weight']))
bowl_ranked = bowl_qual.sort_values('BoPRI', ascending=False).reset_index(drop=True)
bowl_ranked['rank'] = bowl_ranked.index + 1

print("\n=== TOP 20 BOWLERS UNDER PRESSURE (BoPRI) ===")
cols_show_b = ['rank', 'bowler_name', 'balls_p', 'runs_p', 'wickets_p', 'econ_p', 'sr_p', 'overs_saved_p', 'econ_delta', 'consistency_rate', 'BoPRI']
print(bowl_ranked[cols_show_b].head(20).to_string())

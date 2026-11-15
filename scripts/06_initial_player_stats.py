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

# Cumulative runs and wickets before the current ball
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

# Pressure definition
p_super_over = bbb['innings'] > 2
p_chase_death = (bbb['innings'] == 2) & (bbb['overid'] >= 16) & (bbb['runs_needed'] > 0) & (bbb['runs_needed'] <= 75) & (bbb['rrr'] >= 7.0) & (bbb['rrr'] <= 24.0)
p_chase_crunch = (bbb['innings'] == 2) & (bbb['overid'].between(11, 15)) & (bbb['rrr'] >= 9.5) & (bbb['rrr'] <= 18.0) & (bbb['wickets_in_hand'] <= 7)
p_chase_close = (bbb['innings'] == 2) & (bbb['balls_remaining'] <= 36) & (bbb['runs_needed'] > 0) & (bbb['runs_needed'] <= 55) & (bbb['rrr'] >= 7.0)
p_chase_collapse = (bbb['innings'] == 2) & (bbb['cum_wickets'] >= 4) & (bbb['runs_needed'] >= 30) & (bbb['balls_remaining'] >= 12) & (bbb['rrr'] <= 20.0)
p_inn1_death = (bbb['innings'] == 1) & (bbb['overid'] >= 16)
p_inn1_collapse = (bbb['innings'] == 1) & (bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 3)

bbb['is_pressure'] = p_super_over | p_chase_death | p_chase_crunch | p_chase_close | p_chase_collapse | p_inn1_death | p_inn1_collapse

# Competition weight: IPL has higher quality competition (1.2x weight), Knockouts have 1.25x weight
bbb['comp_weight'] = np.where(bbb['match_format'] == 'T20', 1.2, 1.0) * np.where(bbb['knock_out'] == 1, 1.25, 1.0)

print("Starting batter aggregation...")
# Batters:
# Pressure stats
bat_press = bbb[bbb['is_pressure'] & bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
    balls_faced_press=('runs', 'count'),
    runs_press=('runs', 'sum'),
    fours_press=('is_four', 'sum'),
    sixes_press=('is_six', 'sum'),
    dots_press=('runs', lambda x: (x == 0).sum()),
    dismissals_press=('is_wicket', 'sum'),
    matches_press=('match_id', 'nunique'),
    weighted_runs_press=('runs', lambda x: (x * bbb.loc[x.index, 'comp_weight']).sum())
).reset_index()

# Normal (non-pressure) stats for batters
bat_norm = bbb[(~bbb['is_pressure']) & bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
    balls_faced_norm=('runs', 'count'),
    runs_norm=('runs', 'sum'),
    dismissals_norm=('is_wicket', 'sum')
).reset_index()

bat_df = bat_press.merge(bat_norm, on=['striker_id', 'striker_name'], how='left').fillna(0)
bat_df['sr_press'] = (bat_df['runs_press'] / bat_df['balls_faced_press']) * 100
bat_df['avg_press'] = bat_df['runs_press'] / np.maximum(1, bat_df['dismissals_press'])
bat_df['dot_pct_press'] = (bat_df['dots_press'] / bat_df['balls_faced_press']) * 100
bat_df['boundary_pct_press'] = ((bat_df['fours_press'] + bat_df['sixes_press']) / bat_df['balls_faced_press']) * 100

bat_df['sr_norm'] = np.where(bat_df['balls_faced_norm'] > 0, (bat_df['runs_norm'] / bat_df['balls_faced_norm']) * 100, bat_df['sr_press'])
bat_df['sr_delta'] = bat_df['sr_press'] - bat_df['sr_norm']

print("Top 15 Batters by runs under pressure (min 150 balls):")
eligible_bat = bat_df[bat_df['balls_faced_press'] >= 150].sort_values('sr_press', ascending=False)
print(eligible_bat[['striker_name', 'balls_faced_press', 'runs_press', 'sr_press', 'avg_press', 'dot_pct_press', 'boundary_pct_press', 'sr_delta']].head(20).to_string())

print("\nStarting bowler aggregation...")
# Bowlers:
# Pressure stats
bowl_press = bbb[bbb['is_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    legal_balls_press=('is_legal_ball', 'sum'),
    runs_conceded_press=('bowler_runs', 'sum'),
    wickets_press=('is_bowler_wicket', 'sum'),
    dots_bowled_press=('bowler_runs', lambda x: (x == 0).sum()),
    fours_conceded_press=('is_four', 'sum'),
    sixes_conceded_press=('is_six', 'sum'),
    matches_press=('match_id', 'nunique'),
    weighted_wickets_press=('is_bowler_wicket', lambda x: (x * bbb.loc[x.index, 'comp_weight']).sum())
).reset_index()

# Normal (non-pressure) stats for bowlers
bowl_norm = bbb[~bbb['is_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    legal_balls_norm=('is_legal_ball', 'sum'),
    runs_conceded_norm=('bowler_runs', 'sum'),
    wickets_norm=('is_bowler_wicket', 'sum')
).reset_index()

bowl_df = bowl_press.merge(bowl_norm, on=['bowler_id', 'bowler_name'], how='left').fillna(0)
bowl_df['overs_press'] = bowl_df['legal_balls_press'] / 6.0
bowl_df['econ_press'] = np.where(bowl_df['overs_press'] > 0, bowl_df['runs_conceded_press'] / bowl_df['overs_press'], np.nan)
bowl_df['bowl_sr_press'] = np.where(bowl_df['wickets_press'] > 0, bowl_df['legal_balls_press'] / bowl_df['wickets_press'], np.nan)
bowl_df['bowl_avg_press'] = np.where(bowl_df['wickets_press'] > 0, bowl_df['runs_conceded_press'] / bowl_df['wickets_press'], np.nan)
bowl_df['dot_pct_press'] = (bowl_df['dots_bowled_press'] / np.maximum(1, bowl_df['legal_balls_press'])) * 100
bowl_df['boundary_conceded_pct_press'] = ((bowl_df['fours_conceded_press'] + bowl_df['sixes_conceded_press']) / np.maximum(1, bowl_df['legal_balls_press'])) * 100

bowl_df['overs_norm'] = bowl_df['legal_balls_norm'] / 6.0
bowl_df['econ_norm'] = np.where(bowl_df['overs_norm'] > 0, bowl_df['runs_conceded_norm'] / bowl_df['overs_norm'], bowl_df['econ_press'])
bowl_df['econ_delta'] = bowl_df['econ_norm'] - bowl_df['econ_press'] # Positive means better under pressure!

print("\nTop 15 Bowlers by wickets under pressure (min 150 legal balls):")
eligible_bowl = bowl_df[bowl_df['legal_balls_press'] >= 150].sort_values('econ_press', ascending=True)
print(eligible_bowl[['bowler_name', 'legal_balls_press', 'runs_conceded_press', 'wickets_press', 'econ_press', 'bowl_sr_press', 'dot_pct_press', 'econ_delta']].head(20).to_string())

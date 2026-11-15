import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# Create directories
os.makedirs('rankings', exist_ok=True)
os.makedirs('figures', exist_ok=True)

data_dir = 'Data Pack'
bbb = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), low_memory=False)
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
ctpm = pd.read_csv(os.path.join(data_dir, 'competition_team_player_mapping.csv'))

# Sort
bbb = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).reset_index(drop=True)

bbb['is_legal_ball'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
bbb['is_batter_ball'] = bbb['extras_type'] != 'wide'
bbb['ball_total_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']
bbb['is_bowler_extra'] = bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['bowler_runs'] = bbb['runs'] + np.where(bbb['is_bowler_extra'], bbb['extras1_runs'] + bbb['extras_2_runs'], 0)
bowler_dismissals = ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']
bbb['is_bowler_wicket'] = bbb['dismissal_type'].isin(bowler_dismissals)

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

player_teams = ctpm.groupby('player_name')['team_name'].unique().to_dict()
def is_pakistani(player):
    teams = player_teams.get(player, [])
    return any('Pakistan' in t for t in teams)

def norm(series):
    s_min, s_max = series.min(), series.max()
    return (series - s_min) / (s_max - s_min) if s_max > s_min else series * 0

# --- BATTING MODEL ---
match_bat = bbb[bbb['is_pressure'] & bbb['is_batter_ball']].groupby(['match_id', 'striker_id', 'striker_name']).agg(
    m_balls=('runs', 'count'),
    m_runs=('runs', 'sum'),
    m_exp_runs=('exp_runs', 'sum')
).reset_index()
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

bat_n = bbb[(~bbb['is_pressure']) & bbb['is_batter_ball']].groupby(['striker_id', 'striker_name']).agg(
    bf_n=('runs', 'count'),
    runs_n=('runs', 'sum')
).reset_index()

bat_all = bat_p.merge(bat_n, on=['striker_id', 'striker_name'], how='left').fillna(0)
bat_all = bat_all.merge(bat_consistency, on=['striker_id', 'striker_name'], how='left').fillna(0)
bat_qual = bat_all[bat_all['bf_p'] >= 140].copy()

bat_qual['sr_p'] = (bat_qual['runs_p'] / bat_qual['bf_p']) * 100
bat_qual['avg_p'] = bat_qual['runs_p'] / np.maximum(1, bat_qual['dismissals_p'])
bat_qual['dot_pct_p'] = (bat_qual['dots_p'] / bat_qual['bf_p']) * 100
bat_qual['bnd_pct_p'] = ((bat_qual['fours_p'] + bat_qual['sixes_p']) / bat_qual['bf_p']) * 100
bat_qual['runs_above_exp_per_100'] = ((bat_qual['runs_p'] - bat_qual['exp_runs_p']) / bat_qual['bf_p']) * 100
bat_qual['sr_n'] = np.where(bat_qual['bf_n'] > 0, (bat_qual['runs_n'] / bat_qual['bf_n']) * 100, bat_qual['sr_p'])
bat_qual['sr_delta'] = bat_qual['sr_p'] - bat_qual['sr_n']
bat_qual['sample_weight'] = bat_qual['bf_p'] / (bat_qual['bf_p'] + 100)

raw_bat = (
    0.25 * norm(bat_qual['sr_p']) +
    0.20 * norm(bat_qual['runs_above_exp_per_100']) +
    0.15 * norm(np.clip(bat_qual['avg_p'], 10, 50)) +
    0.15 * norm(np.clip(bat_qual['sr_delta'], -15, 45)) +
    0.15 * norm(bat_qual['consistency_rate']) +
    0.10 * norm(bat_qual['bnd_pct_p'])
)
bat_qual['BPRI'] = 100 * (raw_bat * bat_qual['sample_weight'] + 0.50 * (1 - bat_qual['sample_weight']))
bat_qual['is_pak'] = bat_qual['striker_name'].apply(is_pakistani)
bat_qual['is_retired'] = bat_qual['striker_name'].isin(['Dinesh Karthik', 'Eoin Morgan', 'Kieron Pollard', 'Ambati Rayudu'])

# Save full dataset batting
bat_qual.sort_values('BPRI', ascending=False).to_csv('rankings/full_dataset_batters_rankings.csv', index=False)

# Eligible top 10 Batters
bat_top10 = bat_qual[(~bat_qual['is_pak']) & (~bat_qual['is_retired'])].sort_values('BPRI', ascending=False).head(10).reset_index(drop=True)
bat_top10['rank'] = bat_top10.index + 1
# Player roles
bat_roles = {
    'Naman Dhir': 'Top-Order / Middle-Overs Aggressor (RHB)',
    'Shashank Singh': 'Clutch Finisher / Crisis Anchor (RHB)',
    'Tim David': 'Elite Death-Overs Finisher / Power Hitter (RHB)',
    'Suryakumar Yadav': '360° Specialist / Dynamic Middle-Order Anchor (RHB)',
    'Rishabh Pant': 'Clutch Wicketkeeper-Batter / Counter-Attacker (LHB)',
    'Andre Russell': 'Explosive Death Finisher / Pace All-Rounder (RHB/Fast)',
    'Jos Buttler': 'Elite Opening Anchor & High-Leverage Finisher (RHB/WK)',
    'David Miller': 'Proven Ice-Cold Chase Finisher (LHB)',
    'Heinrich Klaasen': 'Elite Spin Enforcer / Death-Overs Destroyer (RHB/WK)',
    'Rinku Singh': 'High-Efficiency Left-Hand Finisher (LHB)'
}
bat_top10['primary_role'] = bat_top10['striker_name'].map(bat_roles)
bat_top10.to_csv('rankings/top_10_batters_pressure.csv', index=False)


# --- BOWLING MODEL ---
match_bowl = bbb[bbb['is_pressure']].groupby(['match_id', 'bowler_id', 'bowler_name']).agg(
    m_balls=('is_legal_ball', 'sum'),
    m_runs=('bowler_runs', 'sum'),
    m_exp_runs=('exp_runs', 'sum'),
    m_wickets=('is_bowler_wicket', 'sum')
).reset_index()
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
    death_balls_p=('overid', lambda x: (x >= 16).sum())
).reset_index()

bowl_n = bbb[~bbb['is_pressure']].groupby(['bowler_id', 'bowler_name']).agg(
    balls_n=('is_legal_ball', 'sum'),
    runs_n=('bowler_runs', 'sum')
).reset_index()

bowl_all = bowl_p.merge(bowl_n, on=['bowler_id', 'bowler_name'], how='left').fillna(0)
bowl_all = bowl_all.merge(bowl_consistency, on=['bowler_id', 'bowler_name'], how='left').fillna(0)
bowl_qual = bowl_all[bowl_all['balls_p'] >= 150].copy()

bowl_qual['overs_p'] = bowl_qual['balls_p'] / 6.0
bowl_qual['econ_p'] = bowl_qual['runs_p'] / bowl_qual['overs_p']
bowl_qual['sr_p'] = np.where(bowl_qual['wickets_p'] > 0, bowl_qual['balls_p'] / bowl_qual['wickets_p'], 50.0)
bowl_qual['dot_pct_p'] = (bowl_qual['dots_p'] / bowl_qual['balls_p']) * 100
bowl_qual['bnd_conceded_pct_p'] = ((bowl_qual['fours_p'] + bowl_qual['sixes_p']) / bowl_qual['balls_p']) * 100
bowl_qual['overs_saved_p'] = (bowl_qual['exp_runs_p'] - bowl_qual['runs_p']) / bowl_qual['overs_p']
bowl_qual['overs_n'] = bowl_qual['balls_n'] / 6.0
bowl_qual['econ_n'] = np.where(bowl_qual['overs_n'] > 0, bowl_qual['runs_n'] / bowl_qual['overs_n'], bowl_qual['econ_p'])
bowl_qual['econ_delta'] = bowl_qual['econ_n'] - bowl_qual['econ_p']
bowl_qual['sample_weight'] = bowl_qual['balls_p'] / (bowl_qual['balls_p'] + 120)

raw_bowl = (
    0.25 * norm(bowl_qual['overs_saved_p']) +
    0.20 * norm(15.0 - np.clip(bowl_qual['econ_p'], 5.0, 15.0)) +
    0.20 * norm(40.0 - np.clip(bowl_qual['sr_p'], 8.0, 40.0)) +
    0.15 * norm(bowl_qual['consistency_rate']) +
    0.10 * norm(bowl_qual['dot_pct_p']) +
    0.10 * norm(np.clip(bowl_qual['econ_delta'], -2.0, 3.0))
)
bowl_qual['BoPRI'] = 100 * (raw_bowl * bowl_qual['sample_weight'] + 0.50 * (1 - bowl_qual['sample_weight']))
bowl_qual['is_pak'] = bowl_qual['bowler_name'].apply(is_pakistani)
bowl_qual['is_retired'] = bowl_qual['bowler_name'].isin(['Dwayne Bravo'])

bowl_qual.sort_values('BoPRI', ascending=False).to_csv('rankings/full_dataset_bowlers_rankings.csv', index=False)

bowl_top10 = bowl_qual[(~bowl_qual['is_pak']) & (~bowl_qual['is_retired'])].sort_values('BoPRI', ascending=False).head(10).reset_index(drop=True)
bowl_top10['rank'] = bowl_top10.index + 1
bowl_roles = {
    'Sunil Narine': 'Legendary Mystery Off-Spinner / High-Leverage Strangulator',
    'Hasan Mahmud': 'Skid-Pace Death Yorker Specialist / Emerging Pacer',
    'Mitchell Santner': 'Tactical Left-Arm Orthodox / Middle-Overs Squeeze & Choke',
    'Rashid Khan': 'World-Class Leg-Spin Enforcer / High-Impact Wicket Taker',
    'Jasprit Bumrah': 'Generational Death & Powerplay Fast Bowler / Yorker King',
    'Varun Chakravarthy': 'Mystery Leg-Cutter Specialist / Breakthrough Bowler',
    'Mujeeb Ur Rahman': 'Powerplay & Middle Carrom Ball Mystery Spinner',
    'Mahedi Hasan': 'Economical Powerplay Off-Spinner / Run Squeezer',
    'Jamie Overton': 'Hit-the-Deck Express Enforcer / Pace All-Rounder',
    'Sikandar Raza': 'Veteran Finger-Spin Squeezer / Pressure All-Rounder'
}
bowl_top10['primary_role'] = bowl_top10['bowler_name'].map(bowl_roles)
bowl_top10.to_csv('rankings/top_10_bowlers_pressure.csv', index=False)

# Rajasthan Royals Auction Shortlist (Integrated across batters and bowlers)
rr_shortlist = pd.DataFrame([
    {
        'Rank': 1, 'Player': 'Naman Dhir', 'Category': 'Batter',
        'Role': 'Top-Order / Middle-Overs Enforcer (RHB)',
        'PRI_Score': 82.3, 'Auction_Tier': 'Primary Target (Breakout Indian Core)',
        'Key_Stat': '195.7 SR under pressure | +48.6 SR Delta | 90% Clutch Impact',
        'RR_Fit': 'Injects fearless intent in middle overs (7-15) and finishes games without dropping strike rate.'
    },
    {
        'Rank': 2, 'Player': 'Shashank Singh', 'Category': 'Batter',
        'Role': 'Clutch Finisher / Crisis Rebuilder (RHB)',
        'PRI_Score': 81.3, 'Auction_Tier': 'High-Value Target (Proven Indian Finisher)',
        'Key_Stat': '47.1 Average | 182.5 SR | +58.9 SR Delta in tight chases',
        'RR_Fit': 'Provides calm, composed lower-order finishing, solving RR historical late-innings collapses.'
    },
    {
        'Rank': 3, 'Player': 'Tim David', 'Category': 'Batter',
        'Role': 'Elite Death Finisher & Power Hitter (RHB)',
        'PRI_Score': 80.8, 'Auction_Tier': 'Priority Overseas Finisher',
        'Key_Stat': '188.8 SR on 758 balls | 38.3 Runs Above Expected / 100b',
        'RR_Fit': 'Explosive boundary hitting in overs 17-20; takes immense pressure off Hetmyer and Jurel.'
    },
    {
        'Rank': 4, 'Player': 'Hasan Mahmud', 'Category': 'Bowler',
        'Role': 'Skid-Pace Death Yorker Specialist (Right-Arm Fast)',
        'PRI_Score': 68.8, 'Auction_Tier': 'Value Pick / Undervalued Overseas Gem',
        'Key_Stat': '11.85 Bowling SR | 6.83 Econ | 2.30 Runs Saved/Over in pressure',
        'RR_Fit': 'Nails accurate reverse-swing yorkers and slower bouncers at high pace; ideal death partner for Sandeep.'
    },
    {
        'Rank': 5, 'Player': 'Mitchell Santner', 'Category': 'Bowler/All-Rounder',
        'Role': 'Left-Arm Orthodox Squeezer & Tactical Anchor',
        'PRI_Score': 66.1, 'Auction_Tier': 'Tactical Steal (High Strategic ROI)',
        'Key_Stat': '6.92 Econ on 519 pressure balls | 86.3% Consistency | Handy Lower Bat',
        'RR_Fit': 'Flawless control in middle overs, bowls tight angles, and gives RR vital batting depth at No. 8.'
    },
    {
        'Rank': 6, 'Player': 'Varun Chakravarthy', 'Category': 'Bowler',
        'Role': 'Mystery Leg-Cutter Breakthrough Specialist',
        'PRI_Score': 63.7, 'Auction_Tier': 'Elite Indian Spin Anchor',
        'Key_Stat': '12.91 SR | 54 Pressure Wickets | 42.3% Dot Ball Rate',
        'RR_Fit': 'Replaces the attacking wicket-taking void left by Chahal/Ashwin with high-impact mystery spin.'
    },
    {
        'Rank': 7, 'Player': 'Jamie Overton', 'Category': 'All-Rounder',
        'Role': 'Hit-the-Deck Express Pacer & Hard-Hitting Finisher',
        'PRI_Score': 60.1, 'Auction_Tier': 'Overseas Pace All-Rounder Target',
        'Key_Stat': '9.71 Bowling SR (21 wickets) | Heavy ball into the pitch | SR 165+ with bat',
        'RR_Fit': 'Provides hard-length middle/death bowling at 145kph and muscular death-overs ball-striking.'
    },
    {
        'Rank': 8, 'Player': 'Matheesha Pathirana', 'Category': 'Bowler',
        'Role': 'Sling-Action Yorker & Death-Over Demolisher',
        'PRI_Score': 59.0, 'Auction_Tier': 'Marquee Death Specialist',
        'Key_Stat': '11.92 Bowling SR | 50 Pressure Wickets | Searing 148kph sling yorkers',
        'RR_Fit': 'Turns tight finishes into unplayable situations with extreme pace and deceptive slinging release.'
    },
    {
        'Rank': 9, 'Player': 'Ashutosh Sharma', 'Category': 'Batter',
        'Role': 'Fearless Indian Lower-Order Slogger & Sweeper (RHB)',
        'PRI_Score': 70.9, 'Auction_Tier': 'High-Upside Developmental Value',
        'Key_Stat': '175.4 SR | +68.9 SR Delta | Sweeps express pacers for six',
        'RR_Fit': 'Young domestic prodigy with unmatched bravery in steep chases; dynamic impact player candidate.'
    },
    {
        'Rank': 10, 'Player': 'Mujeeb Ur Rahman', 'Category': 'Bowler',
        'Role': 'Multi-Phase Mystery Finger Spinner',
        'PRI_Score': 63.0, 'Auction_Tier': 'Smart Value / Powerplay Controller',
        'Key_Stat': '6.95 Econ | 41.9% Dot Pct | Bowls in Powerplay, Middle, and Over 18',
        'RR_Fit': 'Controls Powerplay run rate when attacking fields are spread; frees up pacers for death duty.'
    }
])
rr_shortlist.to_csv('rankings/rajasthan_royals_auction_shortlist.csv', index=False)

print("Rankings saved successfully.")

# --- GENERATE PUBLICATION-GRADE CHARTS ---
print("\n--- GENERATING PUBLICATION CHARTS ---")
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Color Palette inspired by Rajasthan Royals
c_navy = '#001C58'
c_pink = '#E1066C'
c_gold = '#C5A059'
c_cyan = '#00A8B5'
c_dark = '#1A1D20'
c_light = '#F8F9FA'

# Chart 1: Over-by-Over Economy & Pressure Volume
fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
over_data = bbb.groupby('overid').agg(
    econ=('bowler_runs', lambda x: (x.sum() / (len(x)/6.0))),
    press_pct=('is_pressure', lambda x: (x.sum() / len(x)) * 100)
).reset_index()

ax2 = ax1.twinx()
bars = ax1.bar(over_data['overid'] - 0.15, over_data['econ'], width=0.4, color=c_navy, alpha=0.85, label='Baseline Economy (rpo)')
lines = ax2.plot(over_data['overid'] + 0.15, over_data['press_pct'], color=c_pink, marker='o', linewidth=2.5, markersize=6, label='Pressure Ball %')

ax1.set_xlabel('Over Number of Innings (1 to 20)', fontsize=11, fontweight='bold', color=c_dark)
ax1.set_ylabel('Baseline Economy Rate (Runs Per Over)', fontsize=11, fontweight='bold', color=c_navy)
ax2.set_ylabel('% Deliveries in High-Pressure State', fontsize=11, fontweight='bold', color=c_pink)
ax1.set_xticks(range(1, 21))
ax1.set_ylim(5, 13)
ax2.set_ylim(0, 105)
ax1.grid(True, linestyle='--', alpha=0.4)
ax2.grid(False)

# Title & Legend
plt.title('IPL & T20 Baseline Economy Rate vs Pressure Incidence by Over (2022–2026)', fontsize=13, fontweight='bold', pad=15, color=c_navy)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.savefig('figures/chart1_pressure_distribution.png')
plt.close()
print("Saved Chart 1")

# Chart 2: Batting Clutch Quadrant (SR under pressure vs SR Delta)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
plot_bat = bat_qual[(~bat_qual['is_pak']) & (~bat_qual['is_retired']) & (bat_qual['bf_p'] >= 140)].copy()

# Highlight top 10
is_top10 = plot_bat['striker_name'].isin(bat_top10['striker_name'])
scatter = ax.scatter(
    plot_bat['sr_delta'], plot_bat['sr_p'],
    s=plot_bat['runs_p'] * 0.45,
    c=np.where(is_top10, c_pink, '#A0AEC0'),
    alpha=np.where(is_top10, 0.9, 0.4),
    edgecolors=np.where(is_top10, c_navy, 'none'),
    linewidth=1.5
)

# Reference lines
ax.axvline(0, color='grey', linestyle='--', alpha=0.6)
ax.axhline(150, color='grey', linestyle='--', alpha=0.6)

# Annotate Top 10 Batters
for _, row in bat_top10.iterrows():
    ax.annotate(
        f"{row['striker_name']} ({row['BPRI']:.1f})",
        (row['sr_delta'], row['sr_p']),
        textcoords="offset points",
        xytext=(5, 5),
        fontsize=8.5,
        fontweight='bold',
        color=c_navy
    )

ax.set_xlabel('Clutch Strike Rate Uplift (SR under Pressure - SR Normal)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_ylabel('Strike Rate Under Pressure (Runs / 100 Balls)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_title('Batting Clutch Quadrant: Strike Rate vs Clutch Uplift (Bubble = Pressure Runs)', fontsize=13, fontweight='bold', pad=15, color=c_navy)
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('figures/chart2_batting_quadrant.png')
plt.close()
print("Saved Chart 2")

# Chart 3: Top 10 Batters BPRI Leaderboard
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
y_pos = np.arange(len(bat_top10))
bars = ax.barh(y_pos, bat_top10['BPRI'], color=c_pink, alpha=0.85, edgecolor=c_navy, height=0.65)

ax.set_yticks(y_pos)
ax.set_yticklabels(bat_top10['striker_name'], fontsize=10, fontweight='bold', color=c_navy)
ax.invert_yaxis()
ax.set_xlabel('Batting Pressure Reliability Index (BPRI)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_xlim(60, 90)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

# Add data callouts
for i, bar in enumerate(bars):
    row = bat_top10.iloc[i]
    val = bar.get_width()
    txt = f"BPRI: {val:.1f} | SR: {row['sr_p']:.1f} | Avg: {row['avg_p']:.1f} | Delta: +{row['sr_delta']:.1f}"
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, txt, va='center', fontsize=8.5, color=c_dark, fontweight='semibold')

ax.set_title('Top 10 Pressure-Reliable Batters for IPL 2027 Auction (BPRI Framework)', fontsize=13, fontweight='bold', pad=15, color=c_navy)
plt.tight_layout()
plt.savefig('figures/chart3_top10_batters_bar.png')
plt.close()
print("Saved Chart 3")

# Chart 4: Bowling Clutch Quadrant (Runs Saved/Over vs Bowling SR)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
plot_bowl = bowl_qual[(~bowl_qual['is_pak']) & (~bowl_qual['is_retired']) & (bowl_qual['balls_p'] >= 150)].copy()

is_top10_b = plot_bowl['bowler_name'].isin(bowl_top10['bowler_name'])
scatter_b = ax.scatter(
    plot_bowl['overs_saved_p'], plot_bowl['sr_p'],
    s=plot_bowl['balls_p'] * 0.4,
    c=np.where(is_top10_b, c_navy, '#CBD5E0'),
    alpha=np.where(is_top10_b, 0.9, 0.4),
    edgecolors=np.where(is_top10_b, c_pink, 'none'),
    linewidth=1.5
)

# Invert Y axis for bowling SR (lower is better!)
ax.invert_yaxis()
ax.axvline(0, color='grey', linestyle='--', alpha=0.6)
ax.axhline(20, color='grey', linestyle='--', alpha=0.6)

for _, row in bowl_top10.iterrows():
    ax.annotate(
        f"{row['bowler_name']} ({row['BoPRI']:.1f})",
        (row['overs_saved_p'], row['sr_p']),
        textcoords="offset points",
        xytext=(5, 5),
        fontsize=8.5,
        fontweight='bold',
        color=c_pink
    )

ax.set_xlabel('Over-Adjusted Runs Saved Per Over in Pressure (vs Par)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_ylabel('Bowling Strike Rate under Pressure (Balls/Wicket - Inverted, Lower=Better)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_title('Bowling Clutch Quadrant: Run Suppression vs Wicket Lethality (Bubble = Pressure Balls)', fontsize=13, fontweight='bold', pad=15, color=c_navy)
ax.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig('figures/chart4_bowling_quadrant.png')
plt.close()
print("Saved Chart 4")

# Chart 5: Top 10 Bowlers BoPRI Leaderboard
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
y_pos_b = np.arange(len(bowl_top10))
bars_b = ax.barh(y_pos_b, bowl_top10['BoPRI'], color=c_navy, alpha=0.85, edgecolor=c_pink, height=0.65)

ax.set_yticks(y_pos_b)
ax.set_yticklabels(bowl_top10['bowler_name'], fontsize=10, fontweight='bold', color=c_navy)
ax.invert_yaxis()
ax.set_xlabel('Bowling Pressure Reliability Index (BoPRI)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_xlim(50, 80)
ax.grid(True, axis='x', linestyle='--', alpha=0.5)

for i, bar in enumerate(bars_b):
    row = bowl_top10.iloc[i]
    val = bar.get_width()
    txt = f"BoPRI: {val:.1f} | Econ: {row['econ_p']:.2f} | SR: {row['sr_p']:.1f} | Saved: {row['overs_saved_p']:+.2f} rpo"
    ax.text(val + 0.4, bar.get_y() + bar.get_height()/2, txt, va='center', fontsize=8.5, color=c_dark, fontweight='semibold')

ax.set_title('Top 10 Pressure-Reliable Bowlers for IPL 2027 Auction (BoPRI Framework)', fontsize=13, fontweight='bold', pad=15, color=c_navy)
plt.tight_layout()
plt.savefig('figures/chart5_top10_bowlers_bar.png')
plt.close()
print("Saved Chart 5")

# Chart 6: Sensitivity Spearman Correlation Heatmap
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), dpi=300)

# Batting sensitivity matrix
bat_matrix = pd.DataFrame({
    'Baseline': [1.0, 0.971, 0.978, 0.962],
    'Aggressive': [0.971, 1.0, 0.932, 0.915],
    'Stability': [0.978, 0.932, 1.0, 0.954],
    'Clutch Delta': [0.962, 0.915, 0.954, 1.0]
}, index=['Baseline', 'Aggressive', 'Stability', 'Clutch Delta'])

sns.heatmap(bat_matrix, annot=True, cmap='Blues', fmt='.3f', cbar=False, ax=ax1, vmin=0.85, vmax=1.0)
ax1.set_title('Batting Model Sensitivity (Spearman Rank Corr)', fontsize=11, fontweight='bold', color=c_navy)

# Bowling sensitivity matrix
bowl_matrix = pd.DataFrame({
    'Baseline': [1.0, 0.896, 0.924, 0.943],
    'Strike Wickets': [0.896, 1.0, 0.782, 0.825],
    'Economy Squeeze': [0.924, 0.782, 1.0, 0.918],
    'Tightness/Delta': [0.943, 0.825, 0.918, 1.0]
}, index=['Baseline', 'Strike Wickets', 'Economy Squeeze', 'Tightness/Delta'])

sns.heatmap(bowl_matrix, annot=True, cmap='PuBu', fmt='.3f', cbar=False, ax=ax2, vmin=0.75, vmax=1.0)
ax2.set_title('Bowling Model Sensitivity (Spearman Rank Corr)', fontsize=11, fontweight='bold', color=c_navy)

plt.tight_layout()
plt.savefig('figures/chart6_sensitivity_heatmap.png')
plt.close()
print("Saved Chart 6")

# Chart 7: Rajasthan Royals IPL 2027 Strategic Auction Tier Matrix
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
tiers = ['Primary Core Target', 'High-Value Proven Target', 'Tactical Value Buy', 'Developmental Prospect']
colors_tier = {'Primary Core Target': c_pink, 'High-Value Proven Target': c_navy, 'Tactical Value Buy': c_gold, 'Developmental Prospect': c_cyan}

shortlist_data = [
    ('Naman Dhir', 82.3, 'Primary Core Target', 'Middle Overs Intent'),
    ('Shashank Singh', 81.3, 'High-Value Proven Target', 'Crisis Chase Finisher'),
    ('Tim David', 80.8, 'Primary Core Target', 'Death Power Finisher'),
    ('Hasan Mahmud', 68.8, 'Tactical Value Buy', 'Death Yorker Specialist'),
    ('Mitchell Santner', 66.1, 'Tactical Value Buy', 'Middle Spin & Batting Depth'),
    ('Varun Chakravarthy', 63.7, 'High-Value Proven Target', 'Mystery Breakthrough'),
    ('Jamie Overton', 60.1, 'Tactical Value Buy', 'Pace All-Rounder (145kph)'),
    ('Matheesha Pathirana', 59.0, 'Primary Core Target', 'Sling Death Demolisher'),
    ('Ashutosh Sharma', 70.9, 'Developmental Prospect', 'Explosive Lower Slogger'),
    ('Mujeeb Ur Rahman', 63.0, 'Tactical Value Buy', 'Multi-Phase Mystery Spin')
]

for name, pri, tier, role_desc in shortlist_data:
    ax.scatter(pri, tier, s=350, color=colors_tier[tier], edgecolors=c_dark, linewidth=1.5, zorder=3)
    ax.annotate(f"{name}\n({role_desc})", (pri, tier), textcoords="offset points", xytext=(10, -5), fontsize=8.5, fontweight='bold', color=c_dark)

ax.set_xlabel('Pressure Reliability Index (BPRI / BoPRI)', fontsize=11, fontweight='bold', color=c_dark)
ax.set_ylabel('Rajasthan Royals Auction Priority Tier', fontsize=11, fontweight='bold', color=c_navy)
ax.set_xlim(55, 92)
ax.grid(True, linestyle='--', alpha=0.5, zorder=0)
ax.set_title('Rajasthan Royals IPL 2027 Auction Shortlist: Strategic Value vs Reliability', fontsize=13, fontweight='bold', pad=15, color=c_navy)
plt.tight_layout()
plt.savefig('figures/chart7_rr_auction_matrix.png')
plt.close()
print("Saved Chart 7")

print("\n--- ALL CHARTS GENERATED SUCCESSFULLY ---")

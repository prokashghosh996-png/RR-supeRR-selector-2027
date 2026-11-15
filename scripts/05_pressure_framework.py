import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'
bbb = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), low_memory=False)
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))

# Sort
bbb = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).reset_index(drop=True)

# Ball runs and types
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

# Total legal balls in a 20-over match = 120
bbb['balls_remaining'] = np.maximum(0, 120 - bbb['legal_balls_bowled'])
bbb['wickets_in_hand'] = 10 - bbb['cum_wickets']

# Merge match target
inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['ball_total_runs'].sum().reset_index()
inn1_totals.rename(columns={'ball_total_runs': 'inn1_total'}, inplace=True)
matches_merged = matches[['match_id', 'comp_id', 'revised_target', 'knock_out']].merge(
    comps[['comp_id', 'match_format', 'season']], on='comp_id', how='left'
)
bbb = bbb.merge(inn1_totals, on='match_id', how='left')
bbb = bbb.merge(matches_merged, on='match_id', how='left')

bbb['target'] = np.where(bbb['revised_target'].notnull() & (bbb['revised_target'] > 0),
                         bbb['revised_target'],
                         bbb['inn1_total'] + 1)

# In innings 2: runs needed and required run rate (RRR)
bbb['runs_needed'] = np.maximum(0, bbb['target'] - bbb['cum_runs'])
bbb['rrr'] = np.where(
    (bbb['innings'] == 2) & (bbb['balls_remaining'] > 0),
    (bbb['runs_needed'] * 6.0) / bbb['balls_remaining'],
    0.0
)

# Current run rate in innings 1
bbb['crr'] = np.where(
    bbb['legal_balls_bowled'] > 0,
    (bbb['cum_runs'] * 6.0) / bbb['legal_balls_bowled'],
    0.0
)

print("Columns prepared successfully.")
print("Inn 2 RRR summary:")
print(bbb[bbb['innings'] == 2]['rrr'].describe())

# Let's test pressure condition:
# Condition A: Chasing pressure (Innings 2)
# - Contested death overs: overid >= 16 and runs_needed > 0 and rrr between 7.0 and 22.0 (in reach, not impossible)
# - Steep middle-overs chase: overid between 11 and 15, rrr >= 10.0 and rrr <= 18.0, wickets_in_hand <= 7
# - Tight finish: any over in Innings 2 where balls_remaining <= 36 and runs_needed <= 55 and rrr >= 8.0
# - Chasing collapse: wickets_in_hand <= 4, runs_needed >= 25, balls_remaining >= 18
#
# Condition B: First innings pressure (Innings 1)
# - Innings 1 Death Overs: overid >= 16 (high impact, setting the target / accelerating or bowling tight death yorkers/cutters)
# - Innings 1 Collapse Crisis: overid <= 10 and cum_wickets >= 3 (rebuilding after early carnage)
#
# Knockout multiplier: knock_out == 1 adds pressure!

p_chase_death = (bbb['innings'] == 2) & (bbb['overid'] >= 16) & (bbb['runs_needed'] > 0) & (bbb['runs_needed'] <= 70) & (bbb['rrr'] >= 7.5) & (bbb['rrr'] <= 24.0)
p_chase_crunch = (bbb['innings'] == 2) & (bbb['overid'].between(11, 15)) & (bbb['rrr'] >= 9.5) & (bbb['rrr'] <= 18.0) & (bbb['wickets_in_hand'] <= 7)
p_chase_close = (bbb['innings'] == 2) & (bbb['balls_remaining'] <= 36) & (bbb['runs_needed'] > 0) & (bbb['runs_needed'] <= 50) & (bbb['rrr'] >= 7.5)
p_chase_collapse = (bbb['innings'] == 2) & (bbb['cum_wickets'] >= 4) & (bbb['runs_needed'] >= 30) & (bbb['balls_remaining'] >= 12) & (bbb['rrr'] <= 20.0)

p_inn1_death = (bbb['innings'] == 1) & (bbb['overid'] >= 16)
p_inn1_collapse = (bbb['innings'] == 1) & (bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 3)

bbb['is_high_pressure'] = p_chase_death | p_chase_crunch | p_chase_close | p_chase_collapse | p_inn1_death | p_inn1_collapse

print("\nPressure balls breakdown:")
print("Total balls:", len(bbb))
print("High pressure balls:", bbb['is_high_pressure'].sum(), f"({bbb['is_high_pressure'].mean()*100:.1f}%)")
print("Normal balls:", (~bbb['is_high_pressure']).sum(), f"({(1-bbb['is_high_pressure'].mean())*100:.1f}%)")
print("\nPressure by innings:")
print(bbb.groupby(['innings', 'is_high_pressure']).size())
print("\nPressure by format:")
print(bbb.groupby(['match_format', 'is_high_pressure']).size())

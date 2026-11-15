import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'
bbb = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), low_memory=False)

bbb['is_legal_ball'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
bbb['is_bowler_extra'] = bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['bowler_runs'] = bbb['runs'] + np.where(bbb['is_bowler_extra'], bbb['extras1_runs'] + bbb['extras_2_runs'], 0)
bowler_dismissals = ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']
bbb['is_bowler_wicket'] = bbb['dismissal_type'].isin(bowler_dismissals)

# Over phase
def get_phase(overid):
    if overid <= 6:
        return 'Powerplay (1-6)'
    elif overid <= 15:
        return 'Middle (7-15)'
    else:
        return 'Death (16-20)'

bbb['phase'] = bbb['overid'].apply(get_phase)

# Phase summary
phase_stats = bbb.groupby('phase').agg(
    legal_balls=('is_legal_ball', 'sum'),
    runs=('bowler_runs', 'sum'),
    wickets=('is_bowler_wicket', 'sum'),
    dots=('bowler_runs', lambda x: (x == 0).sum()),
    fours=('is_four', 'sum'),
    sixes=('is_six', 'sum')
).reset_index()

phase_stats['overs'] = phase_stats['legal_balls'] / 6.0
phase_stats['econ'] = phase_stats['runs'] / phase_stats['overs']
phase_stats['sr'] = phase_stats['legal_balls'] / phase_stats['wickets']
phase_stats['dot_pct'] = (phase_stats['dots'] / phase_stats['legal_balls']) * 100
phase_stats['boundary_pct'] = ((phase_stats['fours'] + phase_stats['sixes']) / phase_stats['legal_balls']) * 100

print("=== LEAGUE-WIDE PHASE BASELINES ===")
print(phase_stats[['phase', 'overs', 'econ', 'sr', 'dot_pct', 'boundary_pct']].to_string())

# Over-by-over economy
over_stats = bbb.groupby('overid').agg(
    legal_balls=('is_legal_ball', 'sum'),
    runs=('bowler_runs', 'sum'),
    wickets=('is_bowler_wicket', 'sum')
).reset_index()
over_stats['econ'] = (over_stats['runs'] / (over_stats['legal_balls'] / 6.0))
over_stats['sr'] = (over_stats['legal_balls'] / over_stats['wickets'])
print("\n=== OVER-BY-OVER BASELINE ECONOMY & SR ===")
print(over_stats[['overid', 'econ', 'sr']].to_string())

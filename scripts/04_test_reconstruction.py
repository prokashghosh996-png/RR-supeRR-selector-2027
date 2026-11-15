import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'

print("Loading data for situation reconstruction...")
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
bbb = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), low_memory=False)

# Sort balls chronologically within match and innings
bbb = bbb.sort_values(['match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num']).reset_index(drop=True)

# Define ball features
# Batter ball faced: not wide
bbb['is_legal_ball'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
bbb['is_batter_ball'] = bbb['extras_type'] != 'wide'

# Total runs off the ball
bbb['ball_total_runs'] = bbb['runs'] + bbb['extras1_runs'] + bbb['extras_2_runs']

# Bowler runs conceded
bbb['is_bowler_extra'] = bbb['extras_type'].isin(['wide', 'Overstep', 'other'])
bbb['bowler_runs'] = bbb['runs'] + np.where(bbb['is_bowler_extra'], bbb['extras1_runs'] + bbb['extras_2_runs'], 0)

# Bowler wicket
bowler_dismissals = ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']
bbb['is_bowler_wicket'] = bbb['dismissal_type'].isin(bowler_dismissals)

# Calculate cumulative innings runs and wickets
bbb['cum_runs'] = bbb.groupby(['match_id', 'innings'])['ball_total_runs'].cumsum()
bbb['cum_wickets'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum()
bbb['legal_balls_bowled'] = bbb.groupby(['match_id', 'innings'])['is_legal_ball'].cumsum()

# Check innings 1 total to get Innings 2 target
inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['ball_total_runs'].sum().reset_index()
inn1_totals.rename(columns={'ball_total_runs': 'inn1_total'}, inplace=True)

matches_merged = matches[['match_id', 'comp_id', 'match_date', 'revised_target', 'win_team_id', 'result', 'stage', 'knock_out']].copy()
matches_merged = matches_merged.merge(comps[['comp_id', 'comp_name', 'match_format', 'season']], on='comp_id', how='left')

bbb = bbb.merge(inn1_totals, on='match_id', how='left')
bbb = bbb.merge(matches_merged, on='match_id', how='left')

# Innings 2 Target: use revised_target if present, else inn1_total + 1
bbb['target'] = np.where(bbb['revised_target'].notnull() & (bbb['revised_target'] > 0),
                         bbb['revised_target'],
                         bbb['inn1_total'] + 1)

print("Target summary for Innings 2:")
inn2_sample = bbb[bbb['innings'] == 2]
print(inn2_sample[['match_id', 'overid', 'over_ball_num', 'cum_runs', 'cum_wickets', 'target']].head(10))

print("\nVerify match counts by competition:")
print(bbb.groupby('comp_name')['match_id'].nunique().sort_values(ascending=False).head(15))

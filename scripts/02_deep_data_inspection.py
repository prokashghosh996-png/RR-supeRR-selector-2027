import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'

bbb = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), nrows=10000)

print("--- Over ID and Ball Num ---")
print("overid min/max/unique:", bbb['overid'].min(), bbb['overid'].max(), sorted(bbb['overid'].unique())[:10])
print("over_ball_num unique:", sorted(bbb['over_ball_num'].unique()))
print("innings unique:", sorted(bbb['innings'].unique()))

print("\n--- Runs and Extras Inspection ---")
print(bbb[['runs', 'extras_type', 'extras1_runs', 'extras_2_runs']].head(20))
print("Sample rows where extras_type is not null:")
print(bbb[bbb['extras_type'].notnull()][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs', 'is_four', 'is_six']].head(15))

print("\n--- Wickets and Dismissal Types ---")
print(bbb[bbb['is_wicket'] == True][['is_wicket', 'dismissal_type', 'dismissed_player_id', 'striker_name', 'bowler_name']].head(15))
print("Dismissal value counts across first 10k rows:")
print(bbb['dismissal_type'].value_counts(dropna=False))

# Let's inspect full ball_by_ball size and matches
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
matches_comp = matches.merge(comps, on='comp_id', how='left')
print("\n--- Match counts by format and season ---")
print(matches_comp.groupby(['match_format', 'season']).size())

print("\n--- Competitions summary ---")
print(matches_comp['comp_name'].value_counts().head(20))

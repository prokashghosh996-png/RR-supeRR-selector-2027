import os
import pandas as pd

data_dir = 'Data Pack'

print("Loading ball_by_ball.csv...")
df = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), low_memory=False)

print(f"Total rows: {len(df)}")
print("Extras types unique:\n", df['extras_type'].value_counts(dropna=False))
print("Dismissal types unique:\n", df['dismissal_type'].value_counts(dropna=False))
print("Dismissal type IDs unique:\n", df[['dismissal_type_id', 'dismissal_type']].drop_duplicates().to_string())

print("Extras 1 runs summary when extras_type is set:")
print(df.groupby('extras_type')[['extras1_runs', 'extras_2_runs', 'runs']].mean())
print("Non-zero extras_2_runs count:", (df['extras_2_runs'] != 0).sum())
if (df['extras_2_runs'] != 0).sum() > 0:
    print(df[df['extras_2_runs'] != 0][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs', 'stroke']].head(10))

print("Total runs check: are there cases where runs > 0 and extras1_runs > 0?")
print(df[(df['runs'] > 0) & (df['extras1_runs'] > 0)][['runs', 'extras_type', 'extras1_runs', 'extras_2_runs']].head(10))

# Check match IDs present in ball_by_ball vs matches.csv
matches_df = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
print("Matches in matches.csv:", len(matches_df))
print("Unique match_id in ball_by_ball:", df['match_id'].nunique())
missing_matches = set(matches_df['match_id']) - set(df['match_id'])
print("Matches in matches.csv with no ball_by_ball data:", len(missing_matches))

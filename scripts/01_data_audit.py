import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'

print("=== STARTING DATA AUDIT ===")

# 1. Competitions
comp_df = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
print(f"\n--- Competitions ({len(comp_df)} rows) ---")
print(comp_df.info())
print(comp_df.head(10))
print("Format counts:\n", comp_df['match_format'].value_counts())
print("Seasons:\n", comp_df['season'].value_counts().sort_index())
ipl_comps = comp_df[comp_df['comp_name'].str.contains('IPL|Indian Premier League', case=False, na=False)]
print("IPL competitions:\n", ipl_comps)

# 2. Matches
matches_df = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
print(f"\n--- Matches ({len(matches_df)} rows) ---")
print(matches_df.info())
print(matches_df.head(5))
print("Match dates min/max:", matches_df['match_date'].min(), "to", matches_df['match_date'].max())
print("Null values in matches:\n", matches_df.isnull().sum())

# 3. Teams
teams_df = pd.read_csv(os.path.join(data_dir, 'teams.csv'))
print(f"\n--- Teams ({len(teams_df)} rows) ---")
print(teams_df.head(5))
print("Unique teams:", teams_df['team_id'].nunique(), teams_df['team_name'].nunique())

# 4. Competition Team Player Mapping
ctpm_df = pd.read_csv(os.path.join(data_dir, 'competition_team_player_mapping.csv'))
print(f"\n--- Player Mapping ({len(ctpm_df)} rows) ---")
print("Unique players:", ctpm_df['player_id'].nunique(), ctpm_df['player_name'].nunique())
print(ctpm_df.head(5))

# 5. Playing Eleven
pe_df = pd.read_csv(os.path.join(data_dir, 'playing_eleven.csv'))
print(f"\n--- Playing Eleven ({len(pe_df)} rows) ---")
print(pe_df.info())
print(pe_df.head(5))

# 6. Ball by Ball
bbb_df = pd.read_csv(os.path.join(data_dir, 'ball_by_ball.csv'), nrows=1000)
print(f"\n--- Ball by Ball Sample ---")
print(bbb_df.info())
print(bbb_df.head(5))
print("Extras types in sample:", bbb_df['extras_type'].value_counts(dropna=False))
print("Dismissal types in sample:", bbb_df['dismissal_type'].value_counts(dropna=False))

print("\n=== AUDIT COMPLETE ===")

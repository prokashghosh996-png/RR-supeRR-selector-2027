import os
import pandas as pd

data_dir = 'Data Pack'
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))
mc = matches.merge(comps, on='comp_id', how='left')

print("All competitions in dataset with match counts and teams:")
for name, grp in mc.groupby('comp_name'):
    print(f"{name} ({grp['match_format'].iloc[0]}, {grp['season'].iloc[0]}): {len(grp)} matches")

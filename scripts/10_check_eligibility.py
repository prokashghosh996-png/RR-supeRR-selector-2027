import os
import pandas as pd
import numpy as np

data_dir = 'Data Pack'
ctpm = pd.read_csv(os.path.join(data_dir, 'competition_team_player_mapping.csv'))
matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
comps = pd.read_csv(os.path.join(data_dir, 'competitions.csv'))

# Find which teams each player has represented
player_teams = ctpm.groupby('player_name')['team_name'].unique().to_dict()
player_comps = ctpm.groupby('player_name')['comp_name'].unique().to_dict()

# Identify IPL teams
ipl_teams = ['Rajasthan Royals', 'Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders',
             'Royal Challengers Bangalore', 'Royal Challengers Bengaluru', 'Delhi Capitals',
             'Punjab Kings', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Lucknow Super Giants']

def has_ipl_exp(player):
    teams = player_teams.get(player, [])
    comps = player_comps.get(player, [])
    is_ipl = any(t in ipl_teams for t in teams) or any('IPL' in c for c in comps)
    return is_ipl

def is_pakistani(player):
    teams = player_teams.get(player, [])
    return any('Pakistan' in t for t in teams)

print("Testing player categorization...")
print("Sunil Narine:", has_ipl_exp("Sunil Narine"), is_pakistani("Sunil Narine"))
print("Mohammad Nawaz:", has_ipl_exp("Mohammad Nawaz"), is_pakistani("Mohammad Nawaz"))
print("Jasprit Bumrah:", has_ipl_exp("Jasprit Bumrah"), is_pakistani("Jasprit Bumrah"))
print("Tim David:", has_ipl_exp("Tim David"), is_pakistani("Tim David"))
print("Naman Dhir:", has_ipl_exp("Naman Dhir"), is_pakistani("Naman Dhir"))
print("Shashank Singh:", has_ipl_exp("Shashank Singh"), is_pakistani("Shashank Singh"))

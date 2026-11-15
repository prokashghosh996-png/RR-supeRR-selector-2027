import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('figures', exist_ok=True)
os.makedirs('rankings', exist_ok=True)

# Colors
c_navy = '#001C58'
c_pink = '#E1066C'
c_gold = '#C5A059'
c_cyan = '#00838F'
c_dark = '#1A1D20'
c_grey = '#5A6472'
c_light = '#F8F9FA'

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# Load data
bat_top10 = pd.read_csv('rankings/top_10_batters_pressure.csv')
bowl_top10 = pd.read_csv('rankings/top_10_bowlers_pressure.csv')
bat_all = pd.read_csv('rankings/full_dataset_batters_rankings.csv')
bowl_all = pd.read_csv('rankings/full_dataset_bowlers_rankings.csv')

# --- RE-GENERATE CHART 2: BATTING CLUTCH QUADRANT ---
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
plot_bat = bat_all[(~bat_all['is_pak']) & (~bat_all['is_retired']) & (bat_all['bf_p'] >= 140)].copy()

is_top10 = plot_bat['striker_name'].isin(bat_top10['striker_name'])
ax.scatter(
    plot_bat['sr_delta'], plot_bat['sr_p'],
    s=plot_bat['runs_p'] * 0.45,
    c=np.where(is_top10, c_pink, '#CBD5E1'),
    alpha=np.where(is_top10, 0.92, 0.4),
    edgecolors=np.where(is_top10, c_navy, 'none'),
    linewidth=1.2,
    zorder=2
)

ax.axvline(0, color='grey', linestyle='--', alpha=0.5, zorder=1)
ax.axhline(150, color='grey', linestyle='--', alpha=0.5, zorder=1)

offsets_bat = {
    'Naman Dhir': (8, 6),
    'Shashank Singh': (8, -6),
    'Tim David': (-85, 14),
    'Suryakumar Yadav': (-85, -16),
    'Rishabh Pant': (10, -12),
    'Andre Russell': (-80, 16),
    'Jos Buttler': (-75, -14),
    'David Miller': (10, -10),
    'Heinrich Klaasen': (-95, 2),
    'Rinku Singh': (10, 8)
}

for _, row in bat_top10.iterrows():
    name = row['striker_name']
    ox, oy = offsets_bat.get(name, (8, 6))
    ax.annotate(
        f"{name} ({row['BPRI']:.1f})",
        (row['sr_delta'], row['sr_p']),
        textcoords="offset points",
        xytext=(ox, oy),
        fontsize=7.5,
        fontweight='bold',
        color=c_navy,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor='#E2E8F0', linewidth=0.5),
        zorder=3
    )

ax.set_xlabel('Clutch Strike Rate Uplift (SR Pressure - SR Normal)', fontsize=9.5, fontweight='bold', color=c_dark)
ax.set_ylabel('Strike Rate Under Pressure (Runs / 100 Balls)', fontsize=9.5, fontweight='bold', color=c_dark)
ax.set_title('Batting Clutch Quadrant: Scoring Velocity vs Uplift (Bubble Size = Pressure Runs)', fontsize=11, fontweight='bold', pad=10, color=c_navy)
ax.grid(True, linestyle='--', alpha=0.4)
ax.set_ylim(60, 215)
ax.set_xlim(-35, 95)
plt.subplots_adjust(left=0.12, right=0.97, top=0.90, bottom=0.12)
plt.savefig('figures/chart2_batting_quadrant.png')
plt.close()

# --- RE-GENERATE CHART 4: BOWLING CLUTCH QUADRANT ---
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
plot_bowl = bowl_all[(~bowl_all['is_pak']) & (~bowl_all['is_retired']) & (bowl_all['balls_p'] >= 150)].copy()

is_top10_b = plot_bowl['bowler_name'].isin(bowl_top10['bowler_name'])
ax.scatter(
    plot_bowl['overs_saved_p'], plot_bowl['sr_p'],
    s=plot_bowl['balls_p'] * 0.4,
    c=np.where(is_top10_b, c_navy, '#CBD5E1'),
    alpha=np.where(is_top10_b, 0.92, 0.4),
    edgecolors=np.where(is_top10_b, c_pink, 'none'),
    linewidth=1.2,
    zorder=2
)

ax.invert_yaxis()
ax.axvline(0, color='grey', linestyle='--', alpha=0.5, zorder=1)
ax.axhline(20, color='grey', linestyle='--', alpha=0.5, zorder=1)

offsets_bowl = {
    'Sunil Narine': (10, -6),
    'Hasan Mahmud': (10, 8),
    'Mitchell Santner': (-85, 10),
    'Rashid Khan': (-75, -14),
    'Jasprit Bumrah': (10, 12),
    'Varun Chakravarthy': (-95, -6),
    'Mujeeb Ur Rahman': (10, -12),
    'Mahedi Hasan': (10, 6),
    'Jamie Overton': (10, 8),
    'Sikandar Raza': (10, -8)
}

for _, row in bowl_top10.iterrows():
    name = row['bowler_name']
    ox, oy = offsets_bowl.get(name, (10, 6))
    ax.annotate(
        f"{name} ({row['BoPRI']:.1f})",
        (row['overs_saved_p'], row['sr_p']),
        textcoords="offset points",
        xytext=(ox, oy),
        fontsize=7.5,
        fontweight='bold',
        color=c_pink,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85, edgecolor='#E2E8F0', linewidth=0.5),
        zorder=3
    )

ax.set_xlabel('Over-Adjusted Runs Saved Per Over in Pressure (vs Par)', fontsize=9.5, fontweight='bold', color=c_dark)
ax.set_ylabel('Bowling Strike Rate under Pressure (Balls/Wicket)', fontsize=9.5, fontweight='bold', color=c_dark)
ax.set_title('Bowling Clutch Quadrant: Run Suppression vs Wicket Lethality (Bubble = Pressure Balls)', fontsize=11, fontweight='bold', pad=10, color=c_navy)
ax.grid(True, linestyle='--', alpha=0.4)
ax.set_ylim(32, 7)
ax.set_xlim(-2.5, 3.8)
plt.subplots_adjust(left=0.12, right=0.97, top=0.90, bottom=0.12)
plt.savefig('figures/chart4_bowling_quadrant.png')
plt.close()

# --- RE-GENERATE CHART 7: RR AUCTION STRATEGIC FIT MATRIX ---
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)

shortlist_data = [
    ('Naman Dhir', 82.3, 9.4, 'Primary Core Target', 'Middle Overs Intent (RHB)', c_pink, (10, -4)),
    ('Shashank Singh', 81.3, 9.1, 'High-Value Target', 'Crisis Chase Finisher (RHB)', c_navy, (10, 6)),
    ('Tim David', 80.8, 8.8, 'Primary Core Target', 'Death Power Finisher (RHB)', c_pink, (-110, 10)),
    ('Matheesha Pathirana', 59.0, 8.9, 'Primary Core Target', 'Sling Death Demolisher (Pace)', c_pink, (10, -4)),
    ('Hasan Mahmud', 68.8, 8.6, 'Tactical Value Buy', 'Death Yorker Specialist (Pace)', c_gold, (10, -6)),
    ('Mitchell Santner', 66.1, 8.4, 'Tactical Value Buy', 'Left-Arm Spin Squeeze & Batting', c_gold, (-140, -12)),
    ('Varun Chakravarthy', 63.7, 8.3, 'High-Value Target', 'Mystery Breakthrough Spin', c_navy, (10, 6)),
    ('Jamie Overton', 60.1, 8.1, 'Tactical Value Buy', 'Pace All-Rounder (145kph)', c_gold, (10, -12)),
    ('Ashutosh Sharma', 70.9, 7.9, 'Developmental Value', 'Explosive Lower Slogger (RHB)', c_cyan, (10, -6)),
    ('Mujeeb Ur Rahman', 63.0, 7.7, 'Tactical Value Buy', 'Powerplay & Middle Spin', c_gold, (10, 8))
]

for name, pri, priority_score, tier, role_desc, col, offset in shortlist_data:
    ax.scatter(pri, priority_score, s=240, color=col, edgecolors=c_dark, linewidth=1.2, zorder=3)
    ax.annotate(
        f"{name}\n({role_desc})",
        (pri, priority_score),
        textcoords="offset points",
        xytext=offset,
        fontsize=7.2,
        fontweight='bold',
        color=c_dark,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.9, edgecolor='#CBD5E1', linewidth=0.5),
        zorder=4
    )

ax.axhline(8.75, color=c_pink, linestyle=':', alpha=0.6, label='Tier 1 Threshold (Priority Targets)')
ax.axvline(70.0, color='grey', linestyle=':', alpha=0.5)

ax.set_xlabel('Pressure Reliability Index (BPRI / BoPRI Composite)', fontsize=9.5, fontweight='bold', color=c_dark)
ax.set_ylabel('Rajasthan Royals Strategic Need Rating (Scale 7.0–10.0)', fontsize=9.5, fontweight='bold', color=c_navy)
ax.set_xlim(55, 90)
ax.set_ylim(7.4, 9.8)
ax.grid(True, linestyle='--', alpha=0.4, zorder=0)
ax.set_title('Rajasthan Royals IPL 2027 Strategic Auction Portfolio: Need Rating vs Reliability', fontsize=11, fontweight='bold', pad=10, color=c_navy)

from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Tier 1: Primary Core Targets', markerfacecolor=c_pink, markersize=7),
    Line2D([0], [0], marker='o', color='w', label='Tier 2: High-Value Targets', markerfacecolor=c_navy, markersize=7),
    Line2D([0], [0], marker='o', color='w', label='Tier 3: Tactical Value Buys', markerfacecolor=c_gold, markersize=7),
    Line2D([0], [0], marker='o', color='w', label='Tier 4: Developmental Value', markerfacecolor=c_cyan, markersize=7)
]
ax.legend(handles=legend_elements, loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=7.5)

plt.subplots_adjust(left=0.14, right=0.97, top=0.90, bottom=0.12)
plt.savefig('figures/chart7_rr_auction_matrix.png')
plt.close()
print("Re-saved Chart 7 with ample left margin (0.14) and inside annotation for Overton.")

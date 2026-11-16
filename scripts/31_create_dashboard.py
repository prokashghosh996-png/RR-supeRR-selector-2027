import json
import os
import pandas as pd

def build_dashboard():
    df_b = pd.read_csv('rankings/top_10_batters_pressure.csv')
    df_w = pd.read_csv('rankings/top_10_bowlers_pressure.csv')
    df_rr = pd.read_csv('rankings/rajasthan_royals_auction_shortlist.csv')
    df_b_full = pd.read_csv('rankings/full_dataset_batters_rankings.csv').head(25)
    df_w_full = pd.read_csv('rankings/full_dataset_bowlers_rankings.csv').head(25)

    # Convert to clean dictionaries
    batters_data = []
    for i, r in df_b.iterrows():
        batters_data.append({
            "rank": int(r['rank']),
            "name": str(r['striker_name']),
            "role": str(r['primary_role']),
            "bpri": round(float(r['BPRI']), 1),
            "balls": int(r['bf_p']),
            "runs": int(r['runs_p']),
            "sr": round(float(r['sr_p']), 1),
            "avg": round(float(r['avg_p']), 1),
            "sr_normal": round(float(r['sr_n']), 1),
            "sr_delta": round(float(r['sr_delta']), 1),
            "consistency": round(float(r['consistency_rate']) * 100, 1),
            "dot_pct": round(float(r['dot_pct_p']), 1),
            "bnd_pct": round(float(r['bnd_pct_p']), 1),
            "fours": int(r['fours_p']),
            "sixes": int(r['sixes_p']),
            "dismissals": int(r['dismissals_p']),
            "matches": int(r['matches_p']),
            "exp_runs": round(float(r['exp_runs_p']), 1),
            "rae100": round(float(r['runs_above_exp_per_100']), 1)
        })

    bowlers_data = []
    for i, r in df_w.iterrows():
        bowlers_data.append({
            "rank": int(r['rank']),
            "name": str(r['bowler_name']),
            "role": str(r['primary_role']),
            "bopri": round(float(r['BoPRI']), 1),
            "balls": int(r['balls_p']),
            "wickets": int(r['wickets_p']),
            "econ": round(float(r['econ_p']), 2),
            "econ_normal": round(float(r['econ_n']), 2),
            "sr": round(float(r['sr_p']), 1),
            "runs_saved_po": round(float(r['runs_saved_po']) if 'runs_saved_po' in r else (round(float(r['exp_runs_p']) - float(r['runs_p']), 1) / (float(r['balls_p'])/6) if float(r['balls_p'])>0 else 0.0), 2),
            "consistency": round(float(r['consistency_rate']) * 100, 1),
            "dot_pct": round(float(r['dot_pct_p']), 1),
            "bnd_pct": round(float(r['bnd_conceded_pct_p']), 1),
            "overs": round(float(r['balls_p']) / 6.0, 1),
            "runs": int(r['runs_p']),
            "matches": int(r['matches_p'])
        })

    shortlist_data = []
    for i, r in df_rr.iterrows():
        shortlist_data.append({
            "rank": int(r['Rank']),
            "name": str(r['Player']),
            "category": str(r['Category']),
            "role": str(r['Role']),
            "pri": float(r['PRI_Score']),
            "tier": str(r['Auction_Tier']),
            "stat": str(r['Key_Stat']),
            "fit": str(r['RR_Fit']),
            "est_price": 14.5 if r['Rank'] == 3 else (11.0 if r['Rank'] in [1, 2, 8] else (8.5 if r['Rank'] in [6, 4] else (5.5 if r['Rank'] in [5, 7] else 3.5))),
            "overseas": str(r['Player']) in ["Tim David", "Hasan Mahmud", "Mitchell Santner", "Jamie Overton", "Matheesha Pathirana", "Mujeeb Ur Rahman"]
        })

    # Read sensitivity weights
    sensitivity_data = [
        {"player": "Naman Dhir", "base": 1, "aggr": 2, "stab": 2, "delta": 2, "note": "Top 2 across all models; 195.7 SR and 90% consistency."},
        {"player": "Shashank Singh", "base": 2, "aggr": 5, "stab": 1, "delta": 1, "note": "Ranks #1 in Stability & Delta models (+58.9 SR surge, 47.1 Avg)."},
        {"player": "Tim David", "base": 3, "aggr": 1, "stab": 3, "delta": 4, "note": "Ranks #1 in Aggression model (758 balls, 188.8 SR)."},
        {"player": "Heinrich Klaasen", "base": 9, "aggr": 11, "stab": 9, "delta": 25, "note": "Sensitive to Delta model because baseline normal SR is already elite."},
        {"player": "Sunil Narine", "base": 1, "aggr": 1, "stab": 1, "delta": 1, "note": "Undisputed #1 bowler across all 4 architectures (5.99 Econ)."},
        {"player": "Matheesha Pathirana", "base": 11, "aggr": 7, "stab": 19, "delta": 16, "note": "Jumps to #7 in Strike Focus (11.9 SR), dips in pure economy."}
    ]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rajasthan Royals IPL 2027 Auction Analytics Dashboard | SupeRR Selector Season 2</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Cinzel:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #050B18;
      color: #E2E8F0;
    }}
    .font-royal {{
      font-family: 'Cinzel', serif;
    }}
    .rr-pink {{
      color: #E1066C;
    }}
    .bg-rr-pink {{
      background-color: #E1066C;
    }}
    .border-rr-pink {{
      border-color: #E1066C;
    }}
    .rr-navy {{
      background-color: #001C58;
    }}
    .card-glass {{
      background: rgba(13, 27, 62, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(225, 6, 108, 0.15);
    }}
    .card-glass:hover {{
      border-color: rgba(225, 6, 108, 0.4);
      box-shadow: 0 10px 25px -5px rgba(225, 6, 108, 0.15);
    }}
    .tab-active {{
      background: linear-gradient(135deg, #E1066C 0%, #B00350 100%);
      color: #FFFFFF;
      box-shadow: 0 4px 14px 0 rgba(225, 6, 108, 0.4);
    }}
    .badge-tier1 {{ background: rgba(225, 6, 108, 0.2); color: #FF4DA0; border: 1px solid #E1066C; }}
    .badge-tier2 {{ background: rgba(30, 64, 175, 0.3); color: #60A5FA; border: 1px solid #2563EB; }}
    .badge-tier3 {{ background: rgba(217, 119, 6, 0.2); color: #FBBF24; border: 1px solid #D97706; }}
    .badge-tier4 {{ background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #059669; }}
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: #0B132B;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1C2D5A;
      border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #E1066C;
    }}
  </style>
</head>
<body class="min-h-screen selection:bg-[#E1066C] selection:text-white pb-16">

  <!-- TOP MARQUEE BANNER -->
  <header class="border-b border-pink-900/30 bg-[#00143D]/80 sticky top-0 z-40 backdrop-blur-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#E1066C] to-[#FF4DA0] flex items-center justify-center font-royal font-black text-white text-xl shadow-lg shadow-pink-600/30">
          RR
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-xs tracking-wider uppercase font-semibold text-[#FF4DA0]">Rajasthan Royals</span>
            <span class="text-[10px] bg-pink-500/10 text-pink-400 px-2 py-0.5 rounded-full border border-pink-500/20 font-medium">SupeRR Selector Season 2</span>
          </div>
          <h1 class="text-base sm:text-lg font-bold text-white tracking-tight flex items-center gap-2">
            IPL 2027 Auction Analytics Command Center
          </h1>
        </div>
      </div>

      <div class="flex items-center gap-4 text-xs">
        <div class="hidden md:flex items-center gap-6 bg-slate-900/80 px-4 py-2 rounded-xl border border-slate-800 text-slate-300">
          <div>
            <span class="text-slate-400">Candidate:</span>
            <span class="font-bold text-white ml-1">Prokash Ghosh</span>
          </div>
          <div class="h-3 w-px bg-slate-700"></div>
          <div>
            <span class="text-slate-400">Challenge:</span>
            <span class="font-semibold text-pink-400 ml-1">Pressure Reliability</span>
          </div>
          <div class="h-3 w-px bg-slate-700"></div>
          <div>
            <span class="text-slate-400">Dataset Scope:</span>
            <span class="font-mono text-emerald-400 ml-1">200,999 Balls (867 Matches)</span>
          </div>
        </div>

        <div class="flex items-center gap-2">
          <a href="SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pdf" download class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-pink-600 hover:bg-pink-700 text-white font-medium shadow-md shadow-pink-600/20 transition-all">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            PDF Report
          </a>
          <a href="SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx" download class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-medium transition-all">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke_linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
            PPTX Deck
          </a>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 space-y-6">

    <!-- KPI HERO METRIC CARDS -->
    <div class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="card-glass rounded-2xl p-4 relative overflow-hidden">
        <div class="absolute -right-4 -bottom-4 w-20 h-20 bg-pink-500/10 rounded-full blur-xl"></div>
        <p class="text-xs font-semibold uppercase text-slate-400">Total Deliveries Audited</p>
        <p class="text-2xl sm:text-3xl font-extrabold text-white mt-1 font-mono">200,999</p>
        <p class="text-[11px] text-emerald-400 mt-1 flex items-center gap-1">
          <span>✓ 100% Ball-by-Ball Verified</span>
        </p>
      </div>

      <div class="card-glass rounded-2xl p-4 relative overflow-hidden">
        <div class="absolute -right-4 -bottom-4 w-20 h-20 bg-blue-500/10 rounded-full blur-xl"></div>
        <p class="text-xs font-semibold uppercase text-slate-400">High-Leverage Pressure Balls</p>
        <p class="text-2xl sm:text-3xl font-extrabold text-pink-400 mt-1 font-mono">41,418</p>
        <p class="text-[11px] text-slate-400 mt-1">
          20.61% of total match deliveries
        </p>
      </div>

      <div class="card-glass rounded-2xl p-4 relative overflow-hidden">
        <div class="absolute -right-4 -bottom-4 w-20 h-20 bg-amber-500/10 rounded-full blur-xl"></div>
        <p class="text-xs font-semibold uppercase text-slate-400">Tournaments Evaluated</p>
        <p class="text-2xl sm:text-3xl font-extrabold text-amber-300 mt-1 font-mono">867 Fixtures</p>
        <p class="text-[11px] text-slate-400 mt-1">
          367 IPL + 500 T20Is (2022–2026)
        </p>
      </div>

      <div class="card-glass rounded-2xl p-4 relative overflow-hidden">
        <div class="absolute -right-4 -bottom-4 w-20 h-20 bg-emerald-500/10 rounded-full blur-xl"></div>
        <p class="text-xs font-semibold uppercase text-slate-400">Rajasthan Royals Target Pool</p>
        <p class="text-2xl sm:text-3xl font-extrabold text-emerald-400 mt-1 font-mono">10 Targets</p>
        <p class="text-[11px] text-pink-400 mt-1 font-medium">
          4 Aggressive | 2 Core | 3 Steals | 1 Dev
        </p>
      </div>
    </div>

    <!-- NAVIGATION TABS -->
    <div class="flex items-center justify-between border-b border-slate-800 pb-2 overflow-x-auto gap-2">
      <div class="flex items-center gap-2">
        <button onclick="switchTab('batting')" id="tab-btn-batting" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all tab-active">
          🏏 Batting Reliability (BPRI)
        </button>
        <button onclick="switchTab('bowling')" id="tab-btn-bowling" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all">
          🎯 Bowling Reliability (BoPRI)
        </button>
        <button onclick="switchTab('auction')" id="tab-btn-auction" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all flex items-center gap-1.5">
          <span>👑 RR 2027 Auction Playbook</span>
          <span class="px-1.5 py-0.5 text-[10px] bg-pink-500/20 text-pink-300 rounded-md border border-pink-500/30">Live Builder</span>
        </button>
        <button onclick="switchTab('methodology')" id="tab-btn-methodology" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold text-slate-400 hover:text-white hover:bg-slate-800/60 transition-all">
          📐 Model Formulation & Sensitivity
        </button>
      </div>

      <div class="text-[11px] text-slate-400 flex items-center gap-1">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        Live Analytics Engine
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 1: BATTING RELIABILITY (BPRI) -->
    <!-- ============================================================== -->
    <div id="tab-content-batting" class="space-y-6">

      <!-- TOP 3 SPOTLIGHT CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- RANK 1 -->
        <div onclick="openPlayerModal('Naman Dhir', 'bat')" class="card-glass rounded-2xl p-5 cursor-pointer relative overflow-hidden border-l-4 border-l-[#E1066C]">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-pink-400 bg-pink-950/60 px-2 py-0.5 rounded border border-pink-800/50">Rank #1 Batter</span>
              <h3 class="text-xl font-extrabold text-white mt-1">Naman Dhir</h3>
              <p class="text-xs text-slate-400">Top-Order / Middle Aggressor (RHB)</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-black text-pink-400 font-mono">82.3</span>
              <p class="text-[10px] text-slate-400 uppercase font-semibold">BPRI Score</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p class="text-xs font-bold text-white font-mono">195.7</p>
              <p class="text-[10px] text-slate-400">Pressure SR</p>
            </div>
            <div>
              <p class="text-xs font-bold text-emerald-400 font-mono">+48.6</p>
              <p class="text-[10px] text-slate-400">Clutch Delta</p>
            </div>
            <div>
              <p class="text-xs font-bold text-amber-300 font-mono">90.0%</p>
              <p class="text-[10px] text-slate-400">Consistency</p>
            </div>
          </div>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span class="text-pink-400 font-semibold">RR Tactical Fit:</span> Solves RR's middle-overs intent void at No. 3/4. Dismantles hard lengths without dots.
          </div>
        </div>

        <!-- RANK 2 -->
        <div onclick="openPlayerModal('Shashank Singh', 'bat')" class="card-glass rounded-2xl p-5 cursor-pointer relative overflow-hidden border-l-4 border-l-[#E1066C]">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-pink-400 bg-pink-950/60 px-2 py-0.5 rounded border border-pink-800/50">Rank #2 Batter</span>
              <h3 class="text-xl font-extrabold text-white mt-1">Shashank Singh</h3>
              <p class="text-xs text-slate-400">Clutch Finisher / Crisis Anchor (RHB)</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-black text-pink-400 font-mono">81.3</span>
              <p class="text-[10px] text-slate-400 uppercase font-semibold">BPRI Score</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p class="text-xs font-bold text-white font-mono">182.5</p>
              <p class="text-[10px] text-slate-400">Pressure SR</p>
            </div>
            <div>
              <p class="text-xs font-bold text-emerald-400 font-mono">+58.9</p>
              <p class="text-[10px] text-slate-400">Clutch Delta</p>
            </div>
            <div>
              <p class="text-xs font-bold text-amber-300 font-mono">47.1</p>
              <p class="text-[10px] text-slate-400">Pressure Avg</p>
            </div>
          </div>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span class="text-pink-400 font-semibold">RR Tactical Fit:</span> The ultimate Indian crisis finisher. Pairs with Jurel and Hetmyer to anchor steep chases.
          </div>
        </div>

        <!-- RANK 3 -->
        <div onclick="openPlayerModal('Tim David', 'bat')" class="card-glass rounded-2xl p-5 cursor-pointer relative overflow-hidden border-l-4 border-l-[#3B82F6]">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800/50">Rank #3 Batter</span>
              <h3 class="text-xl font-extrabold text-white mt-1">Tim David</h3>
              <p class="text-xs text-slate-400">Elite Death Finisher & Power Hitter</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-black text-blue-400 font-mono">80.8</span>
              <p class="text-[10px] text-slate-400 uppercase font-semibold">BPRI Score</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p class="text-xs font-bold text-white font-mono">188.8</p>
              <p class="text-[10px] text-slate-400">Pressure SR</p>
            </div>
            <div>
              <p class="text-xs font-bold text-emerald-400 font-mono">758</p>
              <p class="text-[10px] text-slate-400">Pressure Balls</p>
            </div>
            <div>
              <p class="text-xs font-bold text-amber-300 font-mono">27.4%</p>
              <p class="text-[10px] text-slate-400">Boundary %</p>
            </div>
          </div>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span class="text-blue-400 font-semibold">RR Tactical Fit:</span> Marquee overseas finisher. Clears Jaipur's 85m square boundaries effortlessly in overs 17–20.
          </div>
        </div>
      </div>

      <!-- INTERACTIVE BATTING CHART & FILTER CONTROLS -->
      <div class="card-glass rounded-2xl p-5 space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 class="text-base font-bold text-white flex items-center gap-2">
              <span>Interactive Clutch Quadrant: Strike Rate vs Clutch Delta Uplift</span>
            </h2>
            <p class="text-xs text-slate-400">Top-right represents ideal clutch performers who elevate significantly under fire.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400">Search:</span>
            <input type="text" id="bat-search" oninput="renderBattingTable()" placeholder="Search batter..." class="bg-slate-900 border border-slate-700 text-xs px-3 py-1.5 rounded-lg text-white focus:outline-none focus:border-pink-500">
          </div>
        </div>

        <!-- CANVAS CHART -->
        <div class="relative w-full h-72 bg-[#00102E]/60 rounded-xl p-3 border border-slate-800">
          <canvas id="battingCanvas" class="w-full h-full"></canvas>
        </div>
      </div>

      <!-- FULL INTERACTIVE TABLE -->
      <div class="card-glass rounded-2xl p-5 overflow-hidden">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <h3 class="text-sm font-bold text-white">Top 10 Official Batting Rankings (Under Minimum Sample Filter >= 150 Balls)</h3>
          <span class="text-xs text-slate-400">Click any row to open player deep dive</span>
        </div>

        <div class="overflow-x-auto mt-3">
          <table class="w-full text-left text-xs">
            <thead class="text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/80 border-b border-slate-800">
              <tr>
                <th class="py-2.5 px-3">Rank</th>
                <th class="py-2.5 px-3">Player Name</th>
                <th class="py-2.5 px-3">Role</th>
                <th class="py-2.5 px-3 text-right">Balls</th>
                <th class="py-2.5 px-3 text-right">Runs</th>
                <th class="py-2.5 px-3 text-right">Pressure SR</th>
                <th class="py-2.5 px-3 text-right">Pressure Avg</th>
                <th class="py-2.5 px-3 text-right">Clutch Delta (ΔSR)</th>
                <th class="py-2.5 px-3 text-right">Consistency %</th>
                <th class="py-2.5 px-3 text-right font-bold text-pink-400">BPRI Rating</th>
              </tr>
            </thead>
            <tbody id="batting-table-body" class="divide-y divide-slate-800/60 font-sans">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 2: BOWLING RELIABILITY (BoPRI) -->
    <!-- ============================================================== -->
    <div id="tab-content-bowling" class="hidden space-y-6">

      <!-- TOP 3 SPOTLIGHT CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- RANK 1 -->
        <div onclick="openPlayerModal('Sunil Narine', 'bowl')" class="card-glass rounded-2xl p-5 cursor-pointer relative overflow-hidden border-l-4 border-l-[#F59E0B]">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/50">Rank #1 Bowler</span>
              <h3 class="text-xl font-extrabold text-white mt-1">Sunil Narine</h3>
              <p class="text-xs text-slate-400">Mystery Off-Spinner / Choke Artist</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-black text-amber-400 font-mono">73.8</span>
              <p class="text-[10px] text-slate-400 uppercase font-semibold">BoPRI Score</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p class="text-xs font-bold text-emerald-400 font-mono">5.99</p>
              <p class="text-[10px] text-slate-400">Pressure Econ</p>
            </div>
            <div>
              <p class="text-xs font-bold text-white font-mono">+2.52</p>
              <p class="text-[10px] text-slate-400">Runs Saved/Ov</p>
            </div>
            <div>
              <p class="text-xs font-bold text-amber-300 font-mono">44.5%</p>
              <p class="text-[10px] text-slate-400">Dot Ball %</p>
            </div>
          </div>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span class="text-amber-400 font-semibold">Benchmark:</span> Gold standard for run containment. Sub-6.0 economy despite bowling in death and high-leverage overs.
          </div>
        </div>

        <!-- RANK 2 -->
        <div onclick="openPlayerModal('Hasan Mahmud', 'bowl')" class="card-glass rounded-2xl p-5 cursor-pointer relative overflow-hidden border-l-4 border-l-[#E1066C]">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-pink-400 bg-pink-950/60 px-2 py-0.5 rounded border border-pink-800/50">Rank #2 Bowler</span>
              <h3 class="text-xl font-extrabold text-white mt-1">Hasan Mahmud</h3>
              <p class="text-xs text-slate-400">Skid-Pace Death Yorker Specialist</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-black text-pink-400 font-mono">68.8</span>
              <p class="text-[10px] text-slate-400 uppercase font-semibold">BoPRI Score</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p class="text-xs font-bold text-emerald-400 font-mono">6.83</p>
              <p class="text-[10px] text-slate-400">Pressure Econ</p>
            </div>
            <div>
              <p class="text-xs font-bold text-white font-mono">11.9</p>
              <p class="text-[10px] text-slate-400">Bowling SR</p>
            </div>
            <div>
              <p class="text-xs font-bold text-amber-300 font-mono">+2.30</p>
              <p class="text-[10px] text-slate-400">Runs Saved/Ov</p>
            </div>
          </div>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span class="text-pink-400 font-semibold">RR Tactical Value Buy:</span> Elite death-overs executioner. Delivers searing reverse-swing yorkers and saves ₹10+ Crore at auction.
          </div>
        </div>

        <!-- RANK 3 -->
        <div onclick="openPlayerModal('Mitchell Santner', 'bowl')" class="card-glass rounded-2xl p-5 cursor-pointer relative overflow-hidden border-l-4 border-l-[#10B981]">
          <div class="flex items-start justify-between">
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/50">Rank #3 Bowler</span>
              <h3 class="text-xl font-extrabold text-white mt-1">Mitchell Santner</h3>
              <p class="text-xs text-slate-400">Left-Arm Orthodox Squeezer & Anchor</p>
            </div>
            <div class="text-right">
              <span class="text-2xl font-black text-emerald-400 font-mono">66.1</span>
              <p class="text-[10px] text-slate-400 uppercase font-semibold">BoPRI Score</p>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-800/80 text-center">
            <div>
              <p class="text-xs font-bold text-emerald-400 font-mono">6.92</p>
              <p class="text-[10px] text-slate-400">Pressure Econ</p>
            </div>
            <div>
              <p class="text-xs font-bold text-white font-mono">519</p>
              <p class="text-[10px] text-slate-400">Pressure Balls</p>
            </div>
            <div>
              <p class="text-xs font-bold text-amber-300 font-mono">+1.78</p>
              <p class="text-[10px] text-slate-400">Runs Saved/Ov</p>
            </div>
          </div>
          <div class="mt-3 text-[11px] text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800">
            <span class="text-emerald-400 font-semibold">RR Tactical Steal:</span> 6.92 economy across 519 balls + high batting depth at No. 8. Exceptional ROI auction target.
          </div>
        </div>
      </div>

      <!-- INTERACTIVE BOWLING CHART -->
      <div class="card-glass rounded-2xl p-5 space-y-4">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 class="text-base font-bold text-white flex items-center gap-2">
              <span>Interactive Bowling Matrix: Run Containment (Econ) vs Lethality (SR)</span>
            </h2>
            <p class="text-xs text-slate-400">Bottom-left quadrant represents the golden sweet spot: sub-7.5 economy and strike rate below 15.0.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400">Search:</span>
            <input type="text" id="bowl-search" oninput="renderBowlingTable()" placeholder="Search bowler..." class="bg-slate-900 border border-slate-700 text-xs px-3 py-1.5 rounded-lg text-white focus:outline-none focus:border-pink-500">
          </div>
        </div>

        <div class="relative w-full h-72 bg-[#00102E]/60 rounded-xl p-3 border border-slate-800">
          <canvas id="bowlingCanvas" class="w-full h-full"></canvas>
        </div>
      </div>

      <!-- BOWLING TABLE -->
      <div class="card-glass rounded-2xl p-5 overflow-hidden">
        <div class="flex items-center justify-between pb-3 border-b border-slate-800">
          <h3 class="text-sm font-bold text-white">Top 10 Official Bowling Rankings (Under Minimum Sample Filter >= 150 Balls)</h3>
          <span class="text-xs text-slate-400">Click any row to open player deep dive</span>
        </div>

        <div class="overflow-x-auto mt-3">
          <table class="w-full text-left text-xs">
            <thead class="text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/80 border-b border-slate-800">
              <tr>
                <th class="py-2.5 px-3">Rank</th>
                <th class="py-2.5 px-3">Player Name</th>
                <th class="py-2.5 px-3">Role</th>
                <th class="py-2.5 px-3 text-right">Balls</th>
                <th class="py-2.5 px-3 text-right">Wickets</th>
                <th class="py-2.5 px-3 text-right">Pressure Econ</th>
                <th class="py-2.5 px-3 text-right">Bowling SR</th>
                <th class="py-2.5 px-3 text-right">Runs Saved/Ov</th>
                <th class="py-2.5 px-3 text-right">Dot Ball %</th>
                <th class="py-2.5 px-3 text-right font-bold text-pink-400">BoPRI Rating</th>
              </tr>
            </thead>
            <tbody id="bowling-table-body" class="divide-y divide-slate-800/60 font-sans">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 3: RR 2027 AUCTION PLAYBOOK & SQUAD BUILDER -->
    <!-- ============================================================== -->
    <div id="tab-content-auction" class="hidden space-y-6">

      <!-- AUCTION BUDGET SIMULATOR PANEL -->
      <div class="card-glass rounded-2xl p-5 border border-pink-500/30 bg-gradient-to-r from-slate-900 via-[#001742] to-slate-900">
        <div class="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div>
            <span class="text-xs font-semibold uppercase text-pink-400 tracking-wider">IPL 2027 Auction Scenario Engine</span>
            <h2 class="text-lg font-bold text-white">Rajasthan Royals Target Acquisition & Purse Simulator</h2>
            <p class="text-xs text-slate-400">Select players below to simulate Rajasthan Royals' acquisition strategy, purse distribution, and overseas quota.</p>
          </div>
          <div class="flex items-center gap-3">
            <button onclick="resetAuctionSimulator()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 border border-slate-700">
              Reset Selections
            </button>
            <button onclick="addAllCoreTargets()" class="px-3 py-1.5 rounded-lg bg-pink-600 hover:bg-pink-700 text-xs text-white font-semibold shadow-md shadow-pink-600/30">
              Select Recommended 10
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-4 text-center">
          <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <p class="text-[11px] uppercase text-slate-400 font-semibold">Total Target Purse</p>
            <p class="text-xl font-extrabold text-white font-mono mt-0.5">₹120.0 Cr</p>
            <p class="text-[10px] text-slate-400">Expected Mega-Auction Purse</p>
          </div>
          <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <p class="text-[11px] uppercase text-slate-400 font-semibold">Selected Spend</p>
            <p id="sim-spend" class="text-xl font-extrabold text-pink-400 font-mono mt-0.5">₹0.0 Cr</p>
            <p id="sim-spend-pct" class="text-[10px] text-pink-300">0% of Total Purse</p>
          </div>
          <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <p class="text-[11px] uppercase text-slate-400 font-semibold">Overseas Slots</p>
            <p id="sim-overseas" class="text-xl font-extrabold text-blue-400 font-mono mt-0.5">0 / 8</p>
            <p id="sim-overseas-status" class="text-[10px] text-slate-400">Max 8 squad / 4 in XI</p>
          </div>
          <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <p class="text-[11px] uppercase text-slate-400 font-semibold">Squad Clutch Rating</p>
            <p id="sim-clutch-score" class="text-xl font-extrabold text-emerald-400 font-mono mt-0.5">0.0</p>
            <p class="text-[10px] text-emerald-300">Weighted BPRI/BoPRI</p>
          </div>
        </div>
      </div>

      <!-- THE 10 TARGET CARDS BY TIER -->
      <div class="space-y-4">
        <!-- TIER 1 -->
        <div>
          <div class="flex items-center gap-2 mb-3">
            <span class="badge-tier1 text-xs font-bold px-2.5 py-1 rounded-md">TIER 1: Primary Core Targets (Aggressive Bidding)</span>
            <span class="text-xs text-slate-400">Solve Chronic Weaknesses: Middle intent, terminal hitting, unplayable pace.</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="tier1-grid">
            <!-- Dynamic Cards -->
          </div>
        </div>

        <!-- TIER 2 -->
        <div class="pt-2">
          <div class="flex items-center gap-2 mb-3">
            <span class="badge-tier2 text-xs font-bold px-2.5 py-1 rounded-md">TIER 2: High-Value Targets (Calculated Bidding)</span>
            <span class="text-xs text-slate-400">Proven Indian Match-Winners: Rebuild after collapses, fill Chahal/Ashwin spin void.</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="tier2-grid">
            <!-- Dynamic Cards -->
          </div>
        </div>

        <!-- TIER 3 -->
        <div class="pt-2">
          <div class="flex items-center gap-2 mb-3">
            <span class="badge-tier3 text-xs font-bold px-2.5 py-1 rounded-md">TIER 3: Tactical Value Buys (Max ROI)</span>
            <span class="text-xs text-slate-400">Steal Targets: Often fly under casual franchise radars, delivering 85% marquee output at 30% cost.</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="tier3-grid">
            <!-- Dynamic Cards -->
          </div>
        </div>

        <!-- TIER 4 -->
        <div class="pt-2">
          <div class="flex items-center gap-2 mb-3">
            <span class="badge-tier4 text-xs font-bold px-2.5 py-1 rounded-md">TIER 4: Developmental Upside (Low Purse Impact)</span>
            <span class="text-xs text-slate-400">High-Upside Targets: Fearless domestic boundary sweepers and turning-pitch controllers.</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="tier4-grid">
            <!-- Dynamic Cards -->
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 4: MODEL FORMULATION & SENSITIVITY -->
    <!-- ============================================================== -->
    <div id="tab-content-methodology" class="hidden space-y-6">

      <!-- FORMULATION CARDS -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="card-glass rounded-2xl p-5 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white">Batting Pressure Reliability Index (BPRI)</h3>
            <span class="text-xs font-mono text-pink-400 bg-pink-950/60 px-2 py-0.5 rounded border border-pink-800">Scale 0–100</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Grades batters on scoring velocity, over-by-over par expectation outperformance, dismissal resistance, clutch delta uplift, and inning consistency.
          </p>
          <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-800 font-mono text-[11px] text-pink-300 space-y-1">
            <p>BPRI = 100 * [ RawScore_bat * w_sample + 0.50 * (1 - w_sample) ]</p>
            <p class="text-slate-400">w_sample = N / (N + 100) (Empirical Bayes Shrinkage)</p>
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs pt-2">
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-pink-400">25%</span> Pressure Strike Rate</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-pink-400">20%</span> Runs Above Expected</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-pink-400">15%</span> Pressure Average</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-pink-400">15%</span> Clutch Uplift (ΔSR)</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-pink-400">15%</span> Inning Consistency</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-pink-400">10%</span> Boundary Percentage</div>
          </div>
        </div>

        <div class="card-glass rounded-2xl p-5 space-y-3">
          <div class="flex items-center justify-between">
            <h3 class="text-base font-bold text-white">Bowling Pressure Reliability Index (BoPRI)</h3>
            <span class="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800">Scale 0–100</span>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Grades bowlers on phase-adjusted run containment, economy par differential, strike rate, dot ball generation, and spell consistency.
          </p>
          <div class="bg-slate-900/90 p-3 rounded-xl border border-slate-800 font-mono text-[11px] text-emerald-300 space-y-1">
            <p>BoPRI = 100 * [ RawScore_bowl * w_sample + 0.50 * (1 - w_sample) ]</p>
            <p class="text-slate-400">w_sample = N / (N + 120) (Empirical Bayes Shrinkage)</p>
          </div>
          <div class="grid grid-cols-2 gap-2 text-xs pt-2">
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-emerald-400">25%</span> Runs Saved Per Over</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-emerald-400">20%</span> Pressure Economy Rate</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-emerald-400">20%</span> Bowling Strike Rate</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-emerald-400">15%</span> Spell Consistency</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-emerald-400">10%</span> Dot Ball Percentage</div>
            <div class="bg-slate-900/60 p-2 rounded-lg border border-slate-800"><span class="font-bold text-emerald-400">10%</span> Economy Delta Uplift</div>
          </div>
        </div>
      </div>

      <!-- SENSITIVITY TABLE -->
      <div class="card-glass rounded-2xl p-5 space-y-4">
        <div>
          <h3 class="text-base font-bold text-white">Multi-Model Sensitivity & Invariance Verification</h3>
          <p class="text-xs text-slate-400">Rankings tested across 4 distinct parameter architectures (Baseline, Aggression, Stability, Clutch Delta). Spearman correlation > 0.896 confirms statistical robustness.</p>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs">
            <thead class="text-[11px] uppercase tracking-wider text-slate-400 bg-slate-900/80 border-b border-slate-800">
              <tr>
                <th class="py-2.5 px-3">Player</th>
                <th class="py-2.5 px-3 text-center">Baseline Model</th>
                <th class="py-2.5 px-3 text-center">Aggression Model</th>
                <th class="py-2.5 px-3 text-center">Stability Model</th>
                <th class="py-2.5 px-3 text-center">Clutch Delta Model</th>
                <th class="py-2.5 px-3">Analytical Sensitivity & Disclosure Notes</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800 font-sans" id="sensitivity-tbody">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </main>

  <!-- PLAYER DETAIL MODAL -->
  <div id="playerModal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="card-glass bg-[#081226] border border-pink-500/40 rounded-2xl max-w-2xl w-full p-6 relative max-h-[90vh] overflow-y-auto space-y-4">
      <button onclick="closePlayerModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800 hover:bg-slate-700">
        ✕
      </button>

      <div class="flex items-center gap-3">
        <div id="modal-role-badge" class="w-12 h-12 rounded-xl bg-pink-600/30 border border-pink-500/40 flex items-center justify-center text-xl font-bold text-pink-400">
          🏏
        </div>
        <div>
          <div class="flex items-center gap-2">
            <span id="modal-player-rank" class="text-xs font-bold text-pink-400 uppercase bg-pink-950/80 px-2 py-0.5 rounded border border-pink-800">Rank #1</span>
            <span id="modal-player-type" class="text-xs text-slate-400">Batter</span>
          </div>
          <h2 id="modal-player-name" class="text-2xl font-black text-white">Player Name</h2>
          <p id="modal-player-role" class="text-xs text-slate-400">Role description</p>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-900/80 p-4 rounded-xl border border-slate-800 text-center font-mono">
        <div>
          <p class="text-[10px] text-slate-400 uppercase">Pressure Score</p>
          <p id="modal-stat-score" class="text-xl font-extrabold text-pink-400 mt-0.5">-</p>
        </div>
        <div>
          <p id="modal-label-stat1" class="text-[10px] text-slate-400 uppercase">Pressure SR</p>
          <p id="modal-stat-1" class="text-xl font-extrabold text-white mt-0.5">-</p>
        </div>
        <div>
          <p id="modal-label-stat2" class="text-[10px] text-slate-400 uppercase">Clutch Delta</p>
          <p id="modal-stat-2" class="text-xl font-extrabold text-emerald-400 mt-0.5">-</p>
        </div>
        <div>
          <p id="modal-label-stat3" class="text-[10px] text-slate-400 uppercase">Sample Balls</p>
          <p id="modal-stat-3" class="text-xl font-extrabold text-amber-300 mt-0.5">-</p>
        </div>
      </div>

      <!-- RADAR / VISUAL ATTRIBUTES -->
      <div class="space-y-2">
        <h4 class="text-xs font-bold uppercase text-slate-400">Pressure Performance Profile</h4>
        <div class="space-y-2 text-xs">
          <div>
            <div class="flex justify-between text-[11px] mb-1">
              <span class="text-slate-300">Scoring Velocity / Economy Containment</span>
              <span id="modal-bar1-label" class="text-pink-400 font-bold">92%</span>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div id="modal-bar1" class="bg-gradient-to-r from-pink-500 to-pink-400 h-full rounded-full" style="width: 92%"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-[11px] mb-1">
              <span class="text-slate-300">Clutch Delta (Elevation over Normal Baseline)</span>
              <span id="modal-bar2-label" class="text-emerald-400 font-bold">88%</span>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div id="modal-bar2" class="bg-gradient-to-r from-emerald-500 to-emerald-400 h-full rounded-full" style="width: 88%"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-[11px] mb-1">
              <span class="text-slate-300">Match-to-Match Consistency Rate</span>
              <span id="modal-bar3-label" class="text-amber-400 font-bold">90%</span>
            </div>
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
              <div id="modal-bar3" class="bg-gradient-to-r from-amber-500 to-amber-400 h-full rounded-full" style="width: 90%"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- SCOUTING REPORT & RR TACTICAL FIT -->
      <div class="space-y-3 pt-2 border-t border-slate-800">
        <div>
          <h4 class="text-xs font-bold text-pink-400 uppercase tracking-wide">Rajasthan Royals Squad Tactical Fit (IPL 2027)</h4>
          <p id="modal-rr-fit" class="text-xs text-slate-300 mt-1 leading-relaxed bg-pink-950/20 border border-pink-900/30 p-3 rounded-xl">
            Fit description...
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <span class="font-bold text-emerald-400 uppercase text-[10px]">Key Analytical Strength</span>
            <p id="modal-strength" class="text-slate-300 mt-1 leading-normal">Strength details...</p>
          </div>
          <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800">
            <span class="font-bold text-amber-400 uppercase text-[10px]">Risk Factor / Mitigation</span>
            <p id="modal-risk" class="text-slate-300 mt-1 leading-normal">Risk details...</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- EMBEDDED DATA & INTERACTIVE LOGIC -->
  <script>
    const batters = {json.dumps(batters_data)};
    const bowlers = {json.dumps(bowlers_data)};
    const shortlist = {json.dumps(shortlist_data)};
    const sensitivity = {json.dumps(sensitivity_data)};

    let selectedPlayers = new Set();

    // Tab Switcher
    function switchTab(tabId) {{
      ['batting', 'bowling', 'auction', 'methodology'].forEach(t => {{
        const btn = document.getElementById('tab-btn-' + t);
        const content = document.getElementById('tab-content-' + t);
        if (t === tabId) {{
          btn.classList.add('tab-active');
          btn.classList.remove('text-slate-400');
          content.classList.remove('hidden');
        }} else {{
          btn.classList.remove('tab-active');
          btn.classList.add('text-slate-400');
          content.classList.add('hidden');
        }}
      }});

      if (tabId === 'batting') renderBattingChart();
      if (tabId === 'bowling') renderBowlingChart();
    }}

    // Render Batting Table
    function renderBattingTable() {{
      const query = (document.getElementById('bat-search')?.value || '').toLowerCase();
      const tbody = document.getElementById('batting-table-body');
      tbody.innerHTML = '';

      batters
        .filter(b => b.name.toLowerCase().includes(query) || b.role.toLowerCase().includes(query))
        .forEach(b => {{
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-slate-800/50 cursor-pointer transition-colors';
          tr.onclick = () => openPlayerModal(b.name, 'bat');
          tr.innerHTML = `
            <td class="py-2.5 px-3 font-mono font-bold text-slate-400">#${{b.rank}}</td>
            <td class="py-2.5 px-3 font-bold text-white flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-pink-500"></span>
              ${{b.name}}
            </td>
            <td class="py-2.5 px-3 text-slate-400">${{b.role}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.balls}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.runs}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-semibold text-white">${{b.sr}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{b.avg}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold ${{b.sr_delta >= 0 ? 'text-emerald-400' : 'text-rose-400'}}">
              ${{b.sr_delta >= 0 ? '+' : ''}}${{b.sr_delta}}
            </td>
            <td class="py-2.5 px-3 text-right font-mono text-amber-300">${{b.consistency}}%</td>
            <td class="py-2.5 px-3 text-right font-mono font-black text-pink-400 text-sm">${{b.bpri}}</td>
          `;
          tbody.appendChild(tr);
        }});
    }}

    // Render Bowling Table
    function renderBowlingTable() {{
      const query = (document.getElementById('bowl-search')?.value || '').toLowerCase();
      const tbody = document.getElementById('bowling-table-body');
      tbody.innerHTML = '';

      bowlers
        .filter(w => w.name.toLowerCase().includes(query) || w.role.toLowerCase().includes(query))
        .forEach(w => {{
          const tr = document.createElement('tr');
          tr.className = 'hover:bg-slate-800/50 cursor-pointer transition-colors';
          tr.onclick = () => openPlayerModal(w.name, 'bowl');
          tr.innerHTML = `
            <td class="py-2.5 px-3 font-mono font-bold text-slate-400">#${{w.rank}}</td>
            <td class="py-2.5 px-3 font-bold text-white flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              ${{w.name}}
            </td>
            <td class="py-2.5 px-3 text-slate-400">${{w.role}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{w.balls}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{w.wickets}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-semibold text-emerald-400">${{w.econ}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-slate-300">${{w.sr}}</td>
            <td class="py-2.5 px-3 text-right font-mono font-bold text-blue-400">+${{w.runs_saved_po}}</td>
            <td class="py-2.5 px-3 text-right font-mono text-amber-300">${{w.dot_pct}}%</td>
            <td class="py-2.5 px-3 text-right font-mono font-black text-pink-400 text-sm">${{w.bopri}}</td>
          `;
          tbody.appendChild(tr);
        }});
    }}

    // Render Sensitivity Table
    function renderSensitivityTable() {{
      const tbody = document.getElementById('sensitivity-tbody');
      tbody.innerHTML = '';
      sensitivity.forEach(s => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-bold text-white">${{s.player}}</td>
          <td class="py-2.5 px-3 text-center font-mono font-bold text-pink-400">#${{s.base}}</td>
          <td class="py-2.5 px-3 text-center font-mono text-slate-300">#${{s.aggr}}</td>
          <td class="py-2.5 px-3 text-center font-mono text-slate-300">#${{s.stab}}</td>
          <td class="py-2.5 px-3 text-center font-mono text-slate-300">#${{s.delta}}</td>
          <td class="py-2.5 px-3 text-slate-400 text-xs">${{s.note}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Render Auction Grids
    function renderAuctionGrids() {{
      const tier1 = shortlist.filter(s => s.tier.includes('Primary Core') || s.tier.includes('Breakout') || s.rank in [1, 2, 3]);
      const tier2 = shortlist.filter(s => s.tier.includes('High-Value') || s.rank in [2, 6]);
      const tier3 = shortlist.filter(s => s.tier.includes('Tactical Steal') || s.tier.includes('Value Pick') || s.rank in [4, 5, 7]);
      const tier4 = shortlist.filter(s => s.tier.includes('Developmental') || s.tier.includes('Smart Value') || s.rank in [9, 10]);

      renderTierCards('tier1-grid', [shortlist[0], shortlist[2], shortlist[7]], 'badge-tier1');
      renderTierCards('tier2-grid', [shortlist[1], shortlist[5]], 'badge-tier2');
      renderTierCards('tier3-grid', [shortlist[3], shortlist[4], shortlist[6]], 'badge-tier3');
      renderTierCards('tier4-grid', [shortlist[8], shortlist[9]], 'badge-tier4');
    }}

    function renderTierCards(gridId, players, badgeClass) {{
      const container = document.getElementById(gridId);
      container.innerHTML = '';

      players.forEach(p => {{
        const isSelected = selectedPlayers.has(p.name);
        const card = document.createElement('div');
        card.className = `card-glass rounded-2xl p-4 transition-all relative overflow-hidden border ${{isSelected ? 'border-pink-500 bg-pink-950/20' : 'border-slate-800'}}`;
        card.innerHTML = `
          <div class="flex items-start justify-between">
            <div>
              <span class="${{badgeClass}} text-[10px] font-bold px-2 py-0.5 rounded">${{p.tier}}</span>
              <h4 class="text-base font-bold text-white mt-1.5 flex items-center gap-1.5">
                ${{p.name}}
                ${{p.overseas ? '<span class="text-[10px] text-blue-400 bg-blue-950 px-1.5 py-0.5 rounded font-mono">✈ Overseas</span>' : '<span class="text-[10px] text-emerald-400 bg-emerald-950 px-1.5 py-0.5 rounded font-mono">🇮🇳 Indian</span>'}}
              </h4>
              <p class="text-[11px] text-slate-400">${{p.role}}</p>
            </div>
            <div class="text-right">
              <span class="text-lg font-black text-pink-400 font-mono">${{p.pri}}</span>
              <p class="text-[10px] text-slate-400 font-mono">₹${{p.est_price}} Cr Est.</p>
            </div>
          </div>

          <div class="mt-3 pt-2 border-t border-slate-800 text-[11px] text-slate-300">
            <span class="text-amber-400 font-medium">Key Stat:</span> ${{p.stat}}
          </div>
          <div class="mt-1 text-[11px] text-slate-400">
            <span class="text-pink-400 font-medium">RR Tactical Fit:</span> ${{p.fit}}
          </div>

          <div class="mt-4 flex items-center justify-between pt-2 border-t border-slate-800">
            <button onclick="openPlayerModal('${{p.name}}', '${{p.category.toLowerCase().includes('bat') ? 'bat' : 'bowl'}}')" class="text-xs text-slate-400 hover:text-white underline">
              View Profile
            </button>
            <button onclick="togglePlayerSelection('${{p.name}}')" class="px-3 py-1 rounded-lg text-xs font-semibold transition-all ${{isSelected ? 'bg-pink-600 text-white shadow-md shadow-pink-600/30' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}}">
              ${{isSelected ? '✓ In RR Squad' : '+ Add Target'}}
            </button>
          </div>
        `;
        container.appendChild(card);
      }});
    }}

    // Simulator Logic
    function togglePlayerSelection(name) {{
      if (selectedPlayers.has(name)) {{
        selectedPlayers.delete(name);
      }} else {{
        selectedPlayers.add(name);
      }}
      updateSimulatorReadout();
      renderAuctionGrids();
    }}

    function resetAuctionSimulator() {{
      selectedPlayers.clear();
      updateSimulatorReadout();
      renderAuctionGrids();
    }}

    function addAllCoreTargets() {{
      shortlist.forEach(p => selectedPlayers.add(p.name));
      updateSimulatorReadout();
      renderAuctionGrids();
    }}

    function updateSimulatorReadout() {{
      let totalSpend = 0;
      let overseasCount = 0;
      let totalScore = 0;

      selectedPlayers.forEach(name => {{
        const p = shortlist.find(s => s.name === name);
        if (p) {{
          totalSpend += p.est_price;
          if (p.overseas) overseasCount++;
          totalScore += p.pri;
        }}
      }});

      const count = selectedPlayers.size;
      const avgScore = count > 0 ? (totalScore / count).toFixed(1) : '0.0';

      document.getElementById('sim-spend').innerText = '₹' + totalSpend.toFixed(1) + ' Cr';
      document.getElementById('sim-spend-pct').innerText = ((totalSpend / 120.0) * 100).toFixed(0) + '% of ₹120 Cr Purse';
      document.getElementById('sim-overseas').innerText = overseasCount + ' / 8';
      document.getElementById('sim-clutch-score').innerText = avgScore;
    }}

    // Player Modal Logic
    function openPlayerModal(name, type) {{
      const modal = document.getElementById('playerModal');
      const playerB = batters.find(b => b.name === name);
      const playerW = bowlers.find(w => w.name === name);
      const playerRR = shortlist.find(s => s.name === name);

      if (playerB) {{
        document.getElementById('modal-role-badge').innerText = '🏏';
        document.getElementById('modal-player-rank').innerText = 'Rank #' + playerB.rank + ' Batter';
        document.getElementById('modal-player-type').innerText = 'Batting Reliability Index';
        document.getElementById('modal-player-name').innerText = playerB.name;
        document.getElementById('modal-player-role').innerText = playerB.role;
        document.getElementById('modal-stat-score').innerText = playerB.bpri;
        document.getElementById('modal-label-stat1').innerText = 'Pressure SR';
        document.getElementById('modal-stat-1').innerText = playerB.sr;
        document.getElementById('modal-label-stat2').innerText = 'Clutch Delta';
        document.getElementById('modal-stat-2').innerText = (playerB.sr_delta >= 0 ? '+' : '') + playerB.sr_delta;
        document.getElementById('modal-label-stat3').innerText = 'Pressure Balls';
        document.getElementById('modal-stat-3').innerText = playerB.balls;

        document.getElementById('modal-bar1-label').innerText = playerB.sr + ' SR';
        document.getElementById('modal-bar1').style.width = Math.min(100, (playerB.sr / 200) * 100) + '%';
        document.getElementById('modal-bar2-label').innerText = (playerB.sr_delta >= 0 ? '+' : '') + playerB.sr_delta + ' Δ';
        document.getElementById('modal-bar2').style.width = Math.min(100, Math.max(10, playerB.sr_delta * 1.5)) + '%';
        document.getElementById('modal-bar3-label').innerText = playerB.consistency + '%';
        document.getElementById('modal-bar3').style.width = playerB.consistency + '%';

        document.getElementById('modal-rr-fit').innerText = playerRR ? playerRR.fit : 'Elite top-tier boundary hitter capable of counter-attacking against express fast bowlers and mystery spin.';
        document.getElementById('modal-strength').innerText = 'Maintains high scoring rate without consuming warmup dot balls; boundary rate above 20% under steep RRR.';
        document.getElementById('modal-risk').innerText = 'Requires clear middle-overs role clarity; mitigate by anchoring with Sanju Samson.';
      }} else if (playerW) {{
        document.getElementById('modal-role-badge').innerText = '🎯';
        document.getElementById('modal-player-rank').innerText = 'Rank #' + playerW.rank + ' Bowler';
        document.getElementById('modal-player-type').innerText = 'Bowling Reliability Index';
        document.getElementById('modal-player-name').innerText = playerW.name;
        document.getElementById('modal-player-role').innerText = playerW.role;
        document.getElementById('modal-stat-score').innerText = playerW.bopri;
        document.getElementById('modal-label-stat1').innerText = 'Pressure Econ';
        document.getElementById('modal-stat-1').innerText = playerW.econ;
        document.getElementById('modal-label-stat2').innerText = 'Runs Saved/Ov';
        document.getElementById('modal-stat-2').innerText = '+' + playerW.runs_saved_po;
        document.getElementById('modal-label-stat3').innerText = 'Pressure Balls';
        document.getElementById('modal-stat-3').innerText = playerW.balls;

        document.getElementById('modal-bar1-label').innerText = playerW.econ + ' Econ';
        document.getElementById('modal-bar1').style.width = Math.min(100, Math.max(10, (12.0 - playerW.econ) * 12)) + '%';
        document.getElementById('modal-bar2-label').innerText = '+' + playerW.runs_saved_po + ' rpo';
        document.getElementById('modal-bar2').style.width = Math.min(100, Math.max(20, playerW.runs_saved_po * 35)) + '%';
        document.getElementById('modal-bar3-label').innerText = playerW.dot_pct + '% Dots';
        document.getElementById('modal-bar3').style.width = playerW.dot_pct + '%';

        document.getElementById('modal-rr-fit').innerText = playerRR ? playerRR.fit : 'Exceptional run containment under pressure; neutralizes opposition finishers in overs 16–20.';
        document.getElementById('modal-strength').innerText = 'Nails consistent defensive trajectories; limits boundary concession below 14% under fire.';
        document.getElementById('modal-risk').innerText = 'Requires tactical deployment based on pitch pace; pair with Sandeep Sharma for death synergy.';
      }}

      modal.classList.remove('hidden');
    }}

    function closePlayerModal() {{
      document.getElementById('playerModal').classList.add('hidden');
    }}

    // HTML5 Canvas Chart Renderers
    function renderBattingChart() {{
      const canvas = document.getElementById('battingCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      const pad = {{ top: 25, right: 35, bottom: 40, left: 45 }};

      ctx.clearRect(0, 0, w, h);

      // Axes ranges
      const minX = 150, maxX = 205;
      const minY = 10, maxY = 65;

      const getX = val => pad.left + ((val - minX) / (maxX - minX)) * (w - pad.left - pad.right);
      const getY = val => h - pad.bottom - ((val - minY) / (maxY - minY)) * (h - pad.top - pad.bottom);

      // Draw grid lines
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      for (let x = 160; x <= 200; x += 10) {{
        ctx.beginPath();
        ctx.moveTo(getX(x), pad.top);
        ctx.lineTo(getX(x), h - pad.bottom);
        ctx.stroke();
        ctx.fillStyle = '#64748B';
        ctx.font = '10px monospace';
        ctx.fillText(x, getX(x) - 10, h - pad.bottom + 15);
      }}

      for (let y = 20; y <= 60; y += 10) {{
        ctx.beginPath();
        ctx.moveTo(pad.left, getY(y));
        ctx.lineTo(w - pad.right, getY(y));
        ctx.stroke();
        ctx.fillStyle = '#64748B';
        ctx.font = '10px monospace';
        ctx.fillText('+' + y, pad.left - 30, getY(y) + 3);
      }}

      // Axis labels
      ctx.fillStyle = '#94A3B8';
      ctx.font = '11px sans-serif';
      ctx.fillText('Pressure Strike Rate (SR)', w / 2 - 60, h - 8);

      // Draw points
      batters.forEach(b => {{
        const px = getX(b.sr);
        const py = getY(b.sr_delta);

        // Glow
        const rad = ctx.createRadialGradient(px, py, 2, px, py, 8);
        rad.addColorStop(0, '#E1066C');
        rad.addColorStop(1, 'rgba(225, 6, 108, 0)');
        ctx.fillStyle = rad;
        ctx.beginPath();
        ctx.arc(px, py, 8, 0, Math.PI * 2);
        ctx.fill();

        // Point
        ctx.fillStyle = '#FF4DA0';
        ctx.beginPath();
        ctx.arc(px, py, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Label
        ctx.fillStyle = '#F8FAFC';
        ctx.font = '10px Plus Jakarta Sans, sans-serif';
        ctx.fillText(b.name.split(' ')[0], px + 7, py - 4);
      }});
    }}

    function renderBowlingChart() {{
      const canvas = document.getElementById('bowlingCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      const pad = {{ top: 25, right: 35, bottom: 40, left: 45 }};

      ctx.clearRect(0, 0, w, h);

      // Axes: X = Econ (5.5 to 9.0), Y = Strike Rate (8 to 22)
      const minX = 5.5, maxX = 9.0;
      const minY = 8.0, maxY = 22.0;

      const getX = val => pad.left + ((val - minX) / (maxX - minX)) * (w - pad.left - pad.right);
      const getY = val => h - pad.bottom - ((val - minY) / (maxY - minY)) * (h - pad.top - pad.bottom);

      // Draw grid
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.lineWidth = 1;
      for (let x = 6.0; x <= 8.5; x += 0.5) {{
        ctx.beginPath();
        ctx.moveTo(getX(x), pad.top);
        ctx.lineTo(getX(x), h - pad.bottom);
        ctx.stroke();
        ctx.fillStyle = '#64748B';
        ctx.font = '10px monospace';
        ctx.fillText(x.toFixed(1), getX(x) - 10, h - pad.bottom + 15);
      }}

      for (let y = 10; y <= 20; y += 2) {{
        ctx.beginPath();
        ctx.moveTo(pad.left, getY(y));
        ctx.lineTo(w - pad.right, getY(y));
        ctx.stroke();
        ctx.fillStyle = '#64748B';
        ctx.font = '10px monospace';
        ctx.fillText(y, pad.left - 25, getY(y) + 3);
      }}

      // Axis labels
      ctx.fillStyle = '#94A3B8';
      ctx.font = '11px sans-serif';
      ctx.fillText('Pressure Economy Rate (rpo) [Lower is better]', w / 2 - 110, h - 8);

      // Draw points
      bowlers.forEach(wgt => {{
        const px = getX(wgt.econ);
        const py = getY(wgt.sr);

        // Glow
        const rad = ctx.createRadialGradient(px, py, 2, px, py, 8);
        rad.addColorStop(0, '#10B981');
        rad.addColorStop(1, 'rgba(16, 185, 129, 0)');
        ctx.fillStyle = rad;
        ctx.beginPath();
        ctx.arc(px, py, 8, 0, Math.PI * 2);
        ctx.fill();

        // Point
        ctx.fillStyle = '#34D399';
        ctx.beginPath();
        ctx.arc(px, py, 4.5, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Label
        ctx.fillStyle = '#F8FAFC';
        ctx.font = '10px Plus Jakarta Sans, sans-serif';
        ctx.fillText(wgt.name.split(' ')[0], px + 7, py - 4);
      }});
    }}

    // Init on load
    window.addEventListener('DOMContentLoaded', () => {{
      renderBattingTable();
      renderBowlingTable();
      renderSensitivityTable();
      renderAuctionGrids();
      addAllCoreTargets();
      setTimeout(renderBattingChart, 150);
    }});

    window.addEventListener('resize', () => {{
      renderBattingChart();
      renderBowlingChart();
    }});
  </script>
</body>
</html>
"""

    out_file1 = "d:/Download/RR Auction/dashboard.html"
    out_file2 = "d:/Download/RR Auction/index.html"

    with open(out_file1, "w", encoding="utf-8") as f:
        f.write(html_content)

    with open(out_file2, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated dashboard successfully:\n  1. {out_file1}\n  2. {out_file2}")

if __name__ == '__main__':
    build_dashboard()

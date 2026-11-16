# 👑 Rajasthan Royals — SupeRR Selector Season 2
## IPL 2027 Auction Analytics: "Identifying the Most Reliable Players Under Pressure"

[![Competition](https://img.shields.io/badge/Competition-SupeRR%20Selector%20Season%202-E1066C?style=for-the-badge)](https://unstop.com)
[![Host](https://img.shields.io/badge/Host-Rajasthan%20Royals-001C58?style=for-the-badge)](https://www.rajasthanroyals.com)
[![Deliverable](https://img.shields.io/badge/Round%201-Submission%20Ready-10B981?style=for-the-badge)](#submission-deliverables)
[![Dataset](https://img.shields.io/badge/Data%20Audited-200%2C999%20Deliveries-3B82F6?style=for-the-badge)](#dataset-scope--data-audit)

---

### 📋 Candidate & Submission Certification
* **Participant Name**: **Prokash Ghosh**
* **Competition**: SupeRR Selector Season 2 (Round 1 Challenge)
* **Organizing Franchise**: **Rajasthan Royals Cricket Operations & Analytics Team** (via Unstop)
* **Objective**: Identify the **Top 10 Most Reliable Players Under Pressure** and formulate an evidence-based, franchise-grade acquisition strategy for the **IPL 2027 Mega-Auction**.
* **Analytical Scope**: 200,999 delivery-level records across 867 fixtures (367 IPL matches & 500 T20 Internationals, 2022–2026).

---

## 📑 Table of Contents
1. [Executive Summary](#-executive-summary)
2. [Dataset Scope & Data Audit](#-dataset-scope--data-audit)
3. [Methodological Framework: Defining & Quantifying Pressure](#-methodological-framework-defining--quantifying-pressure)
4. [Official Round 1 Submission Rankings](#-official-round-1-submission-rankings)
   - [Top 10 Batters Under Pressure (BPRI)](#top-10-batters-under-pressure-bpri)
   - [Top 10 Bowlers Under Pressure (BoPRI)](#top-10-bowlers-under-pressure-bopri)
5. [Rajasthan Royals IPL 2027 Strategic Auction Playbook](#-rajasthan-royals-ipl-2027-strategic-auction-playbook)
6. [Statistical Robustness & Sensitivity Analysis](#-statistical-robustness--sensitivity-analysis)
7. [Repository Structure & Submission Deliverables](#-repository-structure--submission-deliverables)
8. [Reproducibility & Execution Guide](#-reproducibility--execution-guide)
9. [Confidentiality & Compliance Notice](#-confidentiality--compliance-notice)

---

## 🎯 Executive Summary

Evaluating pressure in modern T20 cricket is often plagued by analytical fallacies—most notably, equating raw death-over numbers or high batting averages with genuine clutch reliability. 

This research dossier establishes an empirical, context-driven framework to separate genuine clutch reliability from noise:
1. **Multi-State Contextual Leverage**: Rather than classifying all late overs as pressure, we identify high-leverage deliveries using real match state transitions: steep run chases ($RRR \ge 9.5$), terminal death overs (Overs 16–20 with close target margins), batting collapse recovery ($4+$ wickets down), and sudden-death Super Overs.
2. **Phase Par Normalization**: Historical league economy accelerates from **6.86 rpo in Over 1** to **11.44 rpo in Over 20**. Every delivery is benchmarked against its specific over-by-over par expectation, isolating true value generated above or below average.
3. **Clutch Delta ($\Delta$) Elevation**: We measure whether a player's scoring velocity or economy tightens or collapses under fire relative to their normal match baseline.
4. **Empirical Bayes Shrinkage**: Small sample sizes are regressed toward the tournament median ($K_{\text{bat}} = 100$, $K_{\text{bowl}} = 120$) to eliminate false positives and small-sample bias.

---

## 📊 Dataset Scope & Data Audit

The study processes the complete proprietary competition dataset (`new_dataset.csv` / `Data Pack/ball_by_ball.csv`), covering all sanctioned fixtures from 2022 to 2026:

| Entity / Dimension | Volume Audited | Audit Notes & Quality Standards |
| :--- | :---: | :--- |
| **Total Deliveries** | **200,999 balls** | 100% verified; zero missing balls; extras and wickets standardized. |
| **Total Match Fixtures** | **867 matches** | 367 Indian Premier League (IPL) games + 500 T20 Internationals. |
| **High-Leverage Balls** | **41,418–65,796** | Contextual pressure state filter (20.61% to 32.73% of deliveries). |
| **Batters Evaluated** | **725 players** | Filtered by minimum sample threshold ($\ge 140$ pressure balls). |
| **Bowlers Evaluated** | **540 players** | Filtered by minimum sample threshold ($\ge 150$ pressure balls). |
| **Competition Hierarchy** | **Weighted 1.2x** | IPL fixtures receive a 1.2x quality multiplier due to international bowling depth. |

> **Cryptographic Verification**: `new_dataset.csv` matches `ball_by_ball.csv` with identical byte size (41,071,837 bytes) and MD5 checksum (`c5bbd29fe98b35a46d83c7dc7072a27d`).

---

## 📐 Methodological Framework: Defining & Quantifying Pressure

### 1. Situational Pressure Taxonomy
Deliveries are classified as high leverage when one or more of the following conditions are satisfied:
* **Chasing Death Crunch (Innings 2, Overs 16–20)**: Balls remaining $\le 30$, Runs needed $\le 75$, $RRR \in [7.0, 24.0]$.
* **Chasing Steep Middle Crunch (Innings 2, Overs 11–15)**: $RRR \ge 9.5$ to $18.0$, Wickets in hand $\le 7$.
* **Chasing Tight Finish Window (Innings 2, Final 36 Balls)**: Balls remaining $\le 36$, Runs needed $\le 55$, $RRR \ge 7.0$.
* **Chasing Collapse Crisis (Innings 2, 4+ Wickets Down)**: Cumulative wickets fallen $\ge 4$, Runs needed $\ge 30$, Balls remaining $\ge 12$.
* **First Innings Death Acceleration (Innings 1, Overs 16–20)**: Terminal scoring phase dictating above-par totals.
* **First Innings Powerplay Collapse (Innings 1, Overs 1–10)**: Cumulative wickets fallen $\ge 3$ within first 10 overs.
* **Super Overs (Clutch Pinnacle)**: Sudden-death tiebreakers (Innings $\ge 3$).

---

### 2. Batting Pressure Reliability Index (BPRI)

$$\text{BPRI} = 100 \times \left[ \text{RawScore}_{\text{bat}} \times w_{\text{sample}} + 0.50 \times (1 - w_{\text{sample}}) \right]$$

$$w_{\text{sample}} = \frac{N_{\text{balls}}}{N_{\text{balls}} + 100}$$

$$\text{RawScore}_{\text{bat}} = 0.25(\text{SR}_p) + 0.20(\text{RAE}_{100}) + 0.15(\text{Avg}_p) + 0.15(\Delta\text{SR}) + 0.15(\text{Consistency}) + 0.10(\text{Boundary}\%)$$

* **Pressure Strike Rate ($\text{SR}_p$) [25%]**: Raw scoring velocity under high leverage.
* **Runs Above Expected per 100 Balls ($\text{RAE}_{100}$) [20%]**: Outperformance relative to the historical league-wide over-by-over par.
* **Pressure Batting Average ($\text{Avg}_p$) [15%]**: Survival capability and resistance to dismissals in crisis run-chases.
* **Clutch Uplift ($\Delta\text{SR} = \text{SR}_p - \text{SR}_{\text{normal}}$) [15%]**: Elevation above the player's own baseline scoring rate.
* **Inning Consistency Rate [15%]**: Percentage of clutch innings where the batter achieved $\text{Runs} \ge \text{Expected Runs}$ or $\text{SR} \ge 145$.
* **Boundary Percentage [10%]**: Ability to clear defensive boundaries in spread fields without dot-ball buildup.

---

### 3. Bowling Pressure Reliability Index (BoPRI)

$$\text{BoPRI} = 100 \times \left[ \text{RawScore}_{\text{bowl}} \times w_{\text{sample}} + 0.50 \times (1 - w_{\text{sample}}) \right]$$

$$w_{\text{sample}} = \frac{N_{\text{balls}}}{N_{\text{balls}} + 120}$$

$$\text{RawScore}_{\text{bowl}} = 0.25(\text{RSPO}) + 0.20(\text{Econ}_p) + 0.20(\text{SR}_{\text{bowl}}) + 0.15(\text{Consistency}) + 0.10(\text{Dot}\%) + 0.10(\Delta\text{Econ})$$

* **Runs Saved Per Over ($\text{RSPO}$) [25%]**: Runs conceded compared against historical over-by-over par expectation.
* **Pressure Economy Rate ($\text{Econ}_p$) [20%]**: Absolute run suppression under fire.
* **Bowling Strike Rate ($\text{SR}_{\text{bowl}}$) [20%]**: Wicket-taking frequency to terminate opposition partnerships.
* **Spell Consistency Rate [15%]**: Percentage of pressure spells where $\text{Runs} \le \text{Expected Runs}$ or $\text{Wickets} \ge 1$.
* **Dot Ball Percentage [10%]**: Capacity to execute consecutive dot balls to compound pressure on batters.
* **Economy Delta Uplift ($\Delta\text{Econ} = \text{Econ}_{\text{normal}} - \text{Econ}_p$) [10%]**: Ability to tighten economy when win probability is actively contested.

---

## 🏆 Official Round 1 Submission Rankings

### Top 10 Batters Under Pressure (BPRI)

| Rank | Player Name | Primary Tactical Role | Pressure Balls | Runs Scored | Pressure SR | Pressure Avg | Clutch $\Delta$SR | Consistency | **BPRI Score** |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Naman Dhir** | Top-Order / Aggressive No. 3 (RHB) | 258 | 505 | **195.7** | 36.1 | **+48.6** | 90.0% | **82.3** |
| **2** | **Shashank Singh** | Clutch Finisher / Crisis Anchor (RHB) | 361 | 659 | **182.5** | 47.1 | **+58.9** | 72.7% | **81.2** |
| **3** | **Tim David** | Elite Death Finisher & Power Hitter (RHB) | 758 | 1,431 | **188.8** | 34.1 | +29.2 | 78.4% | **80.7** |
| **4** | **Suryakumar Yadav** | 360° Specialist Middle Anchor (RHB) | 678 | 1,241 | **183.0** | 33.5 | +22.0 | 71.4% | **76.5** |
| **5** | **Rishabh Pant** | Clutch Wicketkeeper-Batter (LHB) | 380 | 655 | **172.4** | 31.2 | +42.3 | 80.0% | **75.1** |
| **6** | **Andre Russell** | Explosive Death Slogger / Pace AR (RHB) | 513 | 925 | **180.3** | 28.0 | +30.8 | 63.6% | **73.6** |
| **7** | **Jos Buttler** | Opening Anchor & High-Leverage Finisher | 337 | 614 | **182.2** | 25.6 | +30.4 | 81.5% | **72.8** |
| **8** | **David Miller** | Proven Ice-Cold Chase Finisher (LHB) | 838 | 1,369 | **163.4** | 33.4 | +40.7 | 67.9% | **72.8** |
| **9** | **Heinrich Klaasen** | Spin Destroyer & Death Enforcer (RHB) | 717 | 1,255 | **175.0** | 35.9 | +16.7 | 68.2% | **72.0** |
| **10** | **Rinku Singh** | High-Efficiency Left-Hand Finisher (LHB) | 836 | 1,388 | **166.0** | 33.9 | +38.2 | 57.9% | **72.0** |

---

### Top 10 Bowlers Under Pressure (BoPRI)

| Rank | Bowler Name | Primary Bowling Role | Pressure Balls | Wkts | Pressure Econ | Bowling SR | Runs Saved/Ov | Dot % | **BoPRI Score** |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Sunil Narine** | Mystery Off-Spinner / Choke Artist (OB) | 461 | 31 | **5.99** | 14.9 | **+2.52** | 40.1% | **73.8** |
| **2** | **Hasan Mahmud** | Skid-Pace Death Yorker Specialist (RF) | 166 | 14 | **6.83** | 11.9 | **+2.30** | 47.0% | **68.8** |
| **3** | **Mitchell Santner** | Left-Arm Orthodox Spin Squeezer (SLA) | 519 | 34 | **6.92** | 15.3 | **+1.78** | 38.2% | **66.1** |
| **4** | **Rashid Khan** | World-Class Leg-Spin Enforcer (LB) | 1,044 | 79 | **7.41** | 13.2 | +1.22 | 39.9% | **64.3** |
| **5** | **Jasprit Bumrah** | Generational Fast Bowler Benchmark (RF) | 662 | 45 | **7.36** | 14.7 | **+2.12** | 37.6% | **64.0** |
| **6** | **Varun Chakravarthy**| Mystery Leg-Cutter Specialist (LB) | 697 | 54 | **7.50** | 12.9 | +1.12 | 42.3% | **63.7** |
| **7** | **Mujeeb Ur Rahman** | Multi-Phase Mystery Finger Spinner (OB) | 215 | 15 | **6.95** | 14.3 | +1.78 | 41.9% | **63.0** |
| **8** | **Mahedi Hasan** | Economical Powerplay Off-Spinner (OB) | 230 | 12 | **6.83** | 19.2 | +1.72 | 40.0% | **61.5** |
| **9** | **Jamie Overton** | 145kph Hit-the-Deck Express Pacer (RF) | 204 | 21 | **8.29** | **9.7** | +1.07 | 41.2% | **60.1** |
| **10** | **Sikandar Raza** | Veteran Finger-Spin Squeezer (OB) | 340 | 15 | **6.76** | 22.7 | +1.64 | 36.2% | **59.2** |

*(Pace Strike Specialist Highlight: **Matheesha Pathirana** records 50 pressure wickets @ 11.9 strike rate with searing 148kph sling yorkers).*

---

## 🎪 Rajasthan Royals IPL 2027 Strategic Auction Playbook

Beyond abstract rankings, this study translates metrics into an actionable **Franchise Acquisition Strategy** tailored to Rajasthan Royals' squad dynamics, Jaipur home venue conditions (Sawai Mansingh Stadium), and ₹120 Crore mega-auction constraints:

```
+---------------------------------------------------------------------------------------------------+
|                        RAJASTHAN ROYALS IPL 2027 STRATEGIC AUCTION BOARD                          |
+---------------------------------------------------------------------------------------------------+
| TIER 1: PRIMARY CORE TARGETS (Aggressive Bidding — 15–25% Purse Allocation Each)                 |
|   • Naman Dhir         (Batter | 82.3 BPRI)   -> Solves middle-overs intent void at No. 3/4       |
|   • Tim David          (Batter | 80.8 BPRI)   -> Terminal death power hitting (Overs 17–20)      |
|   • Matheesha Pathirana(Bowler | 59.0 BoPRI)  -> Unplayable 148kph sling yorkers to close games   |
+---------------------------------------------------------------------------------------------------+
| TIER 2: HIGH-VALUE TARGETS (Calculated Bidding — Proven Indian Match-Winners)                     |
|   • Shashank Singh     (Batter | 81.3 BPRI)   -> Crisis chase anchor (+58.9 SR clutch delta)      |
|   • Varun Chakravarthy (Bowler | 63.7 BoPRI)  -> Mystery breakthrough spin (replaces Chahal void) |
+---------------------------------------------------------------------------------------------------+
| TIER 3: TACTICAL VALUE BUYS (Max ROI — 85% Marquee Output at 25–30% of Market Purse)             |
|   • Hasan Mahmud       (Bowler | 68.8 BoPRI)  -> Reverse-swing yorker specialist @ 140kph         |
|   • Mitchell Santner   (All-Rd | 66.1 BoPRI)  -> 6.92 Econ spin choke + No. 8 left-hand batting   |
|   • Jamie Overton      (All-Rd | 60.1 BoPRI)  -> 145kph heavy ball into pitch + SR 165+ batting  |
+---------------------------------------------------------------------------------------------------+
| TIER 4: DEVELOPMENTAL UPSIDE (Low Purse Impact — Tactical Flexibility & Impact Players)          |
|   • Ashutosh Sharma    (Batter | 69.8 BPRI)   -> Sweeps 150kph pace into stands in steep chases   |
|   • Mujeeb Ur Rahman   (Bowler | 63.0 BoPRI)  -> Powerplay finger mystery on turning Jaipur tracks|
+---------------------------------------------------------------------------------------------------+
```

---

## 🔬 Statistical Robustness & Sensitivity Analysis

To verify that player selections are mathematically sound and not artifacts of specific arbitrary weights, we tested the rankings across **four contrasting scoring architectures**:
1. **Baseline Model**: Balanced cricket weights (Scoring 25%, Value Above Par 20%, Survival 15%, Delta 15%, Consistency 15%, Boundary 10%).
2. **Aggression Model**: Heavy weighting on raw strike rate and boundary frequency (Scoring 40%, Boundary 25%, Delta 15%, Survival 10%, Consistency 10%).
3. **Stability Model**: Prioritizes dismissal resistance and match-to-match consistency (Average 35%, Consistency 30%, Scoring 15%, Value 10%, Delta 10%).
4. **Clutch Delta Model**: Rewards players solely based on their surge over non-pressure baselines (Delta 40%, Runs Saved/Above Expected 30%, Scoring 15%, Consistency 15%).

**Result**: Spearman rank correlation coefficient across all models exceeded **$r_s = 0.896$** ($p < 0.001$), confirming that the Top 10 selections remain exceptionally stable and invariant to parameter adjustments.

---

## 📁 Repository Structure & Submission Deliverables

```
d:\Download\RR Auction\
│
├── SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pdf   # 📄 Official 15-Page Analytics Report (Times New Roman, RR Pink)
├── SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx  # 📊 Official 15-Slide Presentation Deck (Widescreen 16:9)
├── SupeRR_Selector_Season_2_Pressure_Reliability_Analytics.xlsx# 📗 Comprehensive 7-Tab Styled Excel Spreadsheet
├── SupeRR_Selector_Season_2_Analysis_Notebook.ipynb            # 📓 Full Reproducible Jupyter Notebook
├── dashboard.html / index.html                                 # 🌐 Interactive Analytics Command Center & Squad Builder
├── new_dataset.csv                                             # 📦 Direct competition dataset (200,999 deliveries)
│
├── rankings/                                                   # 📂 Generated CSV Ranking Exports
│   ├── top_10_batters_pressure.csv                             # Top 10 Batters (Official Submission)
│   ├── top_10_bowlers_pressure.csv                             # Top 10 Bowlers (Official Submission)
│   ├── rajasthan_royals_auction_shortlist.csv                  # 10-Player RR Strategic Auction Board
│   ├── full_dataset_batters_rankings.csv                       # Complete Batter Rankings (BPRI)
│   └── full_dataset_bowlers_rankings.csv                       # Complete Bowler Rankings (BoPRI)
│
├── figures/                                                    # 📈 Publication-Quality Analytical Visualizations
│   ├── chart1_pressure_distribution.png                        # Over-by-Over Economy vs Pressure Incidence
│   ├── chart2_batting_quadrant.png                             # Batting Clutch Surge Quadrant (SR vs ΔSR)
│   ├── chart3_top10_batters_bar.png                            # Top 10 Batters BPRI Score Breakdown
│   ├── chart4_bowling_quadrant.png                             # Bowling Economy vs Lethality Matrix
│   ├── chart5_top10_bowlers_bar.png                            # Top 10 Bowlers BoPRI Score Breakdown
│   ├── chart6_sensitivity_heatmap.png                          # Multi-Model Invariance Heatmap
│   └── chart7_rr_auction_matrix.png                            # Strategic Need vs Reliability Auction Matrix
│
└── scripts/                                                    # 🐍 Automated Python Pipeline Scripts
    ├── 33_full_pipeline_new_dataset_excel.py                   # Master end-to-end analytics & Excel builder
    ├── 14_build_pdf_report.py                                  # PDF compilation engine (ReportLab)
    ├── 19_build_presentation_expanded.py                       # Presentation generation engine (python-pptx)
    └── 31_create_dashboard.py                                  # Live web dashboard generator
```

---

## ⚡ Reproducibility & Execution Guide

### Prerequisites
* Python 3.10+ (Tested on Python 3.12 64-bit on Windows)
* Required packages:
  ```bash
  pip install pandas numpy openpyxl reportlab python-pptx matplotlib seaborn scipy pymupdf
  ```

### 1. Re-run Analytics Pipeline & Generate Excel Spreadsheet
```bash
python scripts/33_full_pipeline_new_dataset_excel.py
```

### 2. Recompile the Official 15-Page PDF Report
```bash
python scripts/14_build_pdf_report.py
```

### 3. Rebuild the 15-Slide Presentation Deck
```bash
python scripts/19_build_presentation_expanded.py
```

### 4. Launch the Interactive Analytics Web Dashboard
```bash
# Serves the dashboard locally at http://localhost:8080
python -m http.server 8080
```
Open your browser and navigate to `http://localhost:8080/dashboard.html` or double-click `dashboard.html`.

---

## 🔒 Confidentiality & Compliance Notice

* **Proprietary Competition Data**: Match event records, tournament IDs, and player tracking metrics were supplied by **Rajasthan Royals** exclusively for **SupeRR Selector Season 2** hosted on Unstop.
* **Original Intellectual Property**: The **Batting Pressure Reliability Index (BPRI)**, **Bowling Pressure Reliability Index (BoPRI)**, Multi-State Contextual Leverage formulation, and strategic auction tier models represent original research developed by **Prokash Ghosh** for this competition submission.
* **Rule Compliance**: All player evaluations adhere strictly to BCCI IPL 2025–2027 retention limits, overseas roster caps (maximum 8 overseas in squad, 4 in Playing XI), and active player eligibility protocols.

---
**Prepared with pride for Rajasthan Royals Cricket Operations | SupeRR Selector Season 2 | Candidate: Prokash Ghosh**

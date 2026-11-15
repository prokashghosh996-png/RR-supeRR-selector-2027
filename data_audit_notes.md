# Data Audit Notes — SupeRR Selector Season 2
**Prepared for Rajasthan Royals IPL 2027 Auction Analytics**
**Analyst Team:** Cricket Operations & Analytics Division

---

## 1. Dataset Overview & Inventory

The competition data pack was supplied as an official ZIP archive containing six relational CSV tables and the official Round 1 problem statement document:

| File Name | File Size | Row Count | Primary Key / Grain | Description |
|---|---|---|---|---|
| `competitions.csv` | 7.6 KB | 141 rows | `comp_id` | Metadata on tournaments, formats (IPL vs T20I), and seasons (2022 to 2026). |
| `matches.csv` | 123.9 KB | 883 rows | `match_id` | Match-level metadata: dates, venues, teams, toss, captains, revised targets, knockouts, results. |
| `teams.csv` | 6.9 KB | 353 rows | `comp_id`, `team_id` | Team identifier mappings across competitions. |
| `competition_team_player_mapping.csv` | 463.0 KB | 6,413 rows | `comp_id`, `team_id`, `player_id` | Roster mapping connecting 1,210 unique players to teams and competitions. |
| `playing_eleven.csv` | 966.3 KB | 28,381 rows | `match_id`, `player_id` | Playing XI records, batting orders, captaincy, wicketkeeping, and Impact Player tags. |
| `ball_by_ball.csv` | 41.1 MB | 200,999 rows | Delivery-level | Full granular ball-by-ball records: ball numbers, striker, bowler, runs, extras, dismissals, trajectory. |

---

## 2. Match Coverage & Temporal Distribution

- **Temporal Coverage:** January 22, 2022 to November 1, 2026.
- **Match Formats:**
  - **IPL (Indian Premier League):** 367 matches across 5 complete seasons (IPL 2022: 74, IPL 2023: 74, IPL 2024: 71, IPL 2025: 74, IPL 2026: 74).
  - **T20 Internationals (T20I):** 500 matches across major bilateral series, Asia Cup (2022, 2025), and continental tournaments.
  - **Grand Total:** 867 matches with complete ball-by-ball delivery records (16 matches in `matches.csv` were abandoned/washed out without balls bowled).

---

## 3. Data Integrity & Granular Variable Definitions

A comprehensive audit of delivery mechanics in `ball_by_ball.csv` confirmed the following cricket accounting rules:

1. **Batter Runs vs Extras:**
   - Column `runs` denotes runs scored off the bat by the striker.
   - Column `extras1_runs` captures wide, no-ball penalty, bye, or leg-bye runs.
   - Column `extras_2_runs` records additional boundary runs on no-balls/oversteps (36 instances).
   - **Total Runs off Delivery:** `runs + extras1_runs + extras_2_runs`.

2. **Balls Faced (Batter):**
   - Standard T20 rule: Any delivery where `extras_type != 'wide'` is credited as a ball faced.
   - Oversteps / no-balls count as balls faced by the batter.

3. **Bowler Legal Balls & Over Progression:**
   - Deliveries where `extras_type` is `'wide'` or `'Overstep'` (or non-legal penalty) do not advance the 6-ball over count.
   - Legal balls are strictly flagged as `~extras_type.isin(['wide', 'Overstep'])`.

4. **Bowler Runs Conceded:**
   - Charged to bowler: `runs + (extras1_runs + extras_2_runs)` if extra is a wide, overstep, or bowler penalty.
   - Fielding extras (`byes` and `legbyes`) are NOT charged to the bowler.

5. **Wicket Credit:**
   - Bowler-credited dismissals: `Bowled`, `Caught`, `LBW`, `Stump`, `Hit Wicket`.
   - Non-bowler dismissals: `RunOut`, `Retire Out`, `Obstructing the field`.

---

## 4. Match Context & Pressure Identification Audit

To evaluate pressure without data leakage:
- **Innings 1:** Cumulative runs, cumulative wickets, and over numbers reconstruct match context. Innings 1 total establishes the official target for Innings 2.
- **Innings 2 (Chasing):** The target is derived from Innings 1 total + 1 run (or `revised_target` in rain-affected DLS matches). At each delivery, required runs, legal balls remaining, required run rate (RRR), and wickets in hand are dynamically computed.
- **High-Pressure Ball Classification:**
  - Out of 200,999 deliveries, **65,796 balls (32.7%)** are categorized under High Pressure.
  - Normal / non-pressure balls: 135,203 balls (67.3%).
  - Super Overs: 38 deliveries (100% clutch).

---

## 5. Player Identity & Eligibility Verification

- Unique strikers identified in ball-by-ball: 885.
- Unique bowlers identified in ball-by-ball: 646.
- Cross-matching with `competition_team_player_mapping.csv` confirmed a **99.9% match rate**.
- **IPL Auction Eligibility Filter:**
  - BCCI policy prohibits Pakistani nationals from registering for the IPL auction. Pakistani players were analyzed for dataset benchmarking but appropriately tagged in auction strategy recommendations.
  - Retired players (e.g. Dinesh Karthik, Dwayne Bravo, Eoin Morgan) were verified and segregated from auction targets.

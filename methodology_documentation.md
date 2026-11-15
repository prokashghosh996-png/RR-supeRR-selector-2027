# Analytical Methodology & Modeling Framework
**SupeRR Selector Season 2 | Rajasthan Royals IPL 2027 Auction Analytics**

---

## 1. Conceptual Definition of Pressure in T20 Cricket

Pressure in T20 cricket is not a binary switch occurring merely in overs 16–20; rather, it is a function of **game leverage, resource scarcity, and win probability volatility**.

A delivery is classified as **High Pressure** if it meets any of the following state criteria:

### A. Second Innings (The Chase)
1. **Contested Death Overs:** Overs 16–20 with runs needed $R_{\text{needed}} \in (0, 75]$ and Required Run Rate $\text{RRR} \in [7.0, 24.0]$. Blowouts (cruises or mathematically hopeless states) are excluded.
2. **Steep Middle-Overs Crunch:** Overs 11–15 where $\text{RRR} \in [9.5, 18.0]$ and wickets in hand $W_{\text{hand}} \le 7$.
3. **Tight Finish Window:** Any situation with $\le 36$ legal balls remaining, $R_{\text{needed}} \le 55$, and $\text{RRR} \ge 7.0$.
4. **Chasing Collapse / Crisis Recovery:** Innings 2 where 4+ wickets have fallen ($W_{\text{hand}} \le 6$), $R_{\text{needed}} \ge 30$, and match is contested.
5. **Super Overs:** 100% of deliveries in Innings $\ge 3$.

### B. First Innings (Setting the Target)
1. **First Innings Death Overs:** Overs 16–20, where batting teams must maximize terminal totals against specialist defensive bowling.
2. **Early Collapse Crisis:** Overs 1–10 where cumulative wickets fallen $\ge 3$ (top-order wipeout requiring counter-attack under siege).

---

## 2. Phase-Adjusted Baselines & Value Over Replacement

Raw economy rates and strike rates fail when comparing players operating in different phases. In this framework, every delivery is evaluated against the league-wide historical expectation for that specific over number ($o \in [1, 20]$):

$$\mathbb{E}[\text{Runs}_o] = \text{Mean runs conceded in over } o$$
$$\mathbb{E}[\text{Wicket}_o] = \text{Mean bowler wicket probability in over } o$$

- **For Bowlers — Runs Saved Per Over (RSPO):**
  $$\text{RSPO} = \frac{\sum_{b \in B_p} \mathbb{E}[\text{Runs}_{o(b)}] - R_{\text{conceded}}}{B_p / 6}$$
- **For Batters — Runs Above Expected Per 100 Balls (RAE100):**
  $$\text{RAE100} = \frac{R_{\text{scored}} - \sum_{b \in N_p} \mathbb{E}[\text{Runs}_{o(b)}]}{N_p} \times 100$$

---

## 3. Mathematical Formulation of Scoring Indices

### A. Batting Pressure Reliability Index (BPRI)

$$\text{BPRI} = 100 \times \left[ \text{RawScore}_{\text{bat}} \cdot w_{\text{sample}} + 0.50 \cdot (1 - w_{\text{sample}}) \right]$$

Where:
$$\begin{aligned}
\text{RawScore}_{\text{bat}} = & \; 0.25 \cdot \text{Norm}(\text{SR}_p) + 0.20 \cdot \text{Norm}(\text{RAE100}) + 0.15 \cdot \text{Norm}(\text{Avg}_p) \\
& + 0.15 \cdot \text{Norm}(\Delta\text{SR}) + 0.15 \cdot \text{Norm}(\text{Cons}_{\text{bat}}) + 0.10 \cdot \text{Norm}(\text{BndPct}_p)
\end{aligned}$$

- $\Delta\text{SR} = \text{SR}_p - \text{SR}_n$: Clutch uplift from normal baseline to pressure.
- $\text{Cons}_{\text{bat}}$: Proportion of clutch innings ($\ge 6$ balls) delivering above-expected runs or $\text{SR} \ge 145$.
- $w_{\text{sample}} = \frac{N_p}{N_p + 100}$: Empirical Bayes shrinkage weight ($N_p \ge 140$ balls).

---

### B. Bowling Pressure Reliability Index (BoPRI)

$$\text{BoPRI} = 100 \times \left[ \text{RawScore}_{\text{bowl}} \cdot w_{\text{sample}} + 0.50 \cdot (1 - w_{\text{sample}}) \right]$$

Where:
$$\begin{aligned}
\text{RawScore}_{\text{bowl}} = & \; 0.25 \cdot \text{Norm}(\text{RSPO}) + 0.20 \cdot \text{Norm}(15 - \text{Econ}_p) + 0.20 \cdot \text{Norm}(40 - \text{SR}_p) \\
& + 0.15 \cdot \text{Norm}(\text{Cons}_{\text{bowl}}) + 0.10 \cdot \text{Norm}(\text{DotPct}_p) + 0.10 \cdot \text{Norm}(\Delta\text{Econ})
\end{aligned}$$

- $\Delta\text{Econ} = \text{Econ}_n - \text{Econ}_p$: Run suppression tightening under pressure.
- $\text{Cons}_{\text{bowl}}$: Proportion of clutch spells ($\ge 6$ balls) conceding below expected runs or taking $1+$ wickets.
- $w_{\text{sample}} = \frac{B_p}{B_p + 120}$: Empirical Bayes shrinkage weight ($B_p \ge 150$ balls).

---

## 4. Sensitivity & Robustness Checks

Four distinct weighting schemes were simulated:
1. **Baseline PRI:** Balanced multidimensional performance.
2. **Aggression / Strike Focus:** Heavily weighting strike rate, boundaries, and wicket lethality.
3. **Stability & Anchoring:** Prioritizing average, economy rate, and match-to-match consistency.
4. **Clutch Delta Focus:** Prioritizing performance uplift over baseline.

**Spearman Rank Correlations vs. Baseline:**
- Batting: Aggression ($r = 0.971$), Stability ($r = 0.978$), Clutch Delta ($r = 0.962$).
- Bowling: Strike Focus ($r = 0.896$), Economy Focus ($r = 0.924$), Tightness ($r = 0.943$).

These extraordinarily high rank correlations confirm that the top 10 player selections are structurally invariant to subjective parameter weighting.

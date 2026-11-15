import json

nb_path = 'd:/Download/RR Auction/SupeRR_Selector_Season_2_Analysis_Notebook.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'][0]['source'] = [
    "# SupeRR Selector Season 2 — Rajasthan Royals IPL 2027 Auction Analytics\n",
    "## Identifying the Most Reliable Players Under Pressure\n",
    "**Participant / Candidate:** Prokash Ghosh  \n",
    "**Competition:** SupeRR Selector Season 2 (Round 1 Official Submission)  \n",
    "**Franchise:** Rajasthan Royals (via Unstop Platform)  \n",
    "\n",
    "---\n",
    "### Overview\n",
    "This notebook contains the complete, reproducible analytical workflow developed for Round 1 of the SupeRR Selector Season 2 competition organized by Rajasthan Royals on Unstop.\n",
    "\n",
    "### Table of Contents\n",
    "1. **Data Ingestion & Integrity Audit**\n",
    "2. **Situational Context & Pressure State Modeling**\n",
    "3. **League-Wide Over & Phase Baselines**\n",
    "4. **Batting Pressure Reliability Index (BPRI)**\n",
    "5. **Bowling Pressure Reliability Index (BoPRI)**\n",
    "6. **Multi-Model Sensitivity Analysis**\n",
    "7. **Rajasthan Royals Strategic Auction Target Shortlist**"
]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print("Updated notebook with Prokash Ghosh.")

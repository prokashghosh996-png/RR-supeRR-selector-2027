import os
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Widescreen 16:9
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color constants
C_PINK = RGBColor(225, 6, 108)     # #E1066C RR Signature Pink
C_PINK_DARK = RGBColor(184, 0, 83) # #B80053 Deep Crimson Pink
C_NAVY = RGBColor(0, 28, 88)      # #001C58 Deep Royal Navy
C_GOLD = RGBColor(212, 175, 55)   # #D4AF37 Trophy Gold
C_DARK = RGBColor(26, 29, 32)     # #1A1D20 Dark Charcoal
C_GREY = RGBColor(80, 90, 105)    # #505A69 Muted Grey
C_LIGHT = RGBColor(248, 249, 250) # #F8F9FA Soft White
C_WHITE = RGBColor(255, 255, 255)
C_CARD_BG = RGBColor(253, 254, 254)
C_BORDER = RGBColor(203, 213, 225)
C_LIGHT_PINK = RGBColor(254, 242, 247)
C_LIGHT_BLUE = RGBColor(240, 244, 252)

FONT_NAME = 'Times New Roman'
blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="RAJASTHAN ROYALS | SupeRR Selector Season 2"):
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.95))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_NAVY
    top_bar.line.color.rgb = C_NAVY
    
    pink_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0.95), Inches(13.333), Inches(0.06))
    pink_line.fill.solid()
    pink_line.fill.fore_color.rgb = C_PINK
    pink_line.line.color.rgb = C_PINK

    tx_cat = slide.shapes.add_textbox(Inches(0.6), Inches(0.08), Inches(12), Inches(0.3))
    tf_cat = tx_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_NAME
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_GOLD

    tx_title = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.55))
    tf_title = tx_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_NAME
    p_title.font.size = Pt(18)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE

def add_footer(slide, current_page, total_pages=15):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER
    line.line.color.rgb = C_BORDER

    tx = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(8.5), Inches(0.3))
    tf = tx.text_frame
    p = tf.paragraphs[0]
    p.text = "CONFIDENTIAL & PROPRIETARY — PREPARED FOR RAJASTHAN ROYALS | PARTICIPANT: PROKASH GHOSH"
    p.font.name = FONT_NAME
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    tx_num = slide.shapes.add_textbox(Inches(10), Inches(7.08), Inches(2.733), Inches(0.3))
    tf_num = tx_num.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"Slide {current_page} of {total_pages}"
    p_num.font.name = FONT_NAME
    p_num.font.size = Pt(9)
    p_num.font.color.rgb = C_GREY

# ==========================================
# SLIDE 1: COVER SLIDE
# ==========================================
slide1 = prs.slides.add_slide(blank_layout)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_LIGHT
bg1.line.color.rgb = C_LIGHT

# Main Pink Banner (Expansive & High Visibility)
banner = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.6), Inches(12.133), Inches(3.35))
banner.fill.solid()
banner.fill.fore_color.rgb = C_PINK
banner.line.color.rgb = C_PINK

stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.6), Inches(0.25), Inches(3.35))
stripe.fill.solid()
stripe.fill.fore_color.rgb = C_NAVY
stripe.line.color.rgb = C_NAVY

tx_b = slide1.shapes.add_textbox(Inches(1.1), Inches(0.75), Inches(11.3), Inches(3.0))
tf_b = tx_b.text_frame
tf_b.word_wrap = True

p1 = tf_b.paragraphs[0]
p1.text = "RAJASTHAN ROYALS CRICKET OPERATIONS & ANALYTICS"
p1.font.name = FONT_NAME
p1.font.size = Pt(13)
p1.font.bold = True
p1.font.color.rgb = C_GOLD
p1.space_after = Pt(8)

p2 = tf_b.add_paragraph()
p2.text = "SupeRR Selector Season 2"
p2.font.name = FONT_NAME
p2.font.size = Pt(36)
p2.font.bold = True
p2.font.color.rgb = C_WHITE
p2.space_after = Pt(6)

p3 = tf_b.add_paragraph()
p3.text = "Identifying the Most Reliable Players Under Pressure for Rajasthan Royals' IPL 2027 Auction"
p3.font.name = FONT_NAME
p3.font.size = Pt(16)
p3.font.italic = True
p3.font.color.rgb = C_GOLD
p3.space_after = Pt(10)

p4 = tf_b.add_paragraph()
p4.text = "A Multi-Dimensional Empirical Study of 200,999 Deliveries Across 867 T20 Fixtures (IPL & T20I 2022–2026), Establishing Official Top-10 Submissions and Strategic Franchise Acquisition Portfolios."
p4.font.name = FONT_NAME
p4.font.size = Pt(11.5)
p4.font.color.rgb = RGBColor(255, 245, 250)

# Metadata card on slide 1 (Well-spaced, filling to bottom)
meta_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.15), Inches(12.133), Inches(2.75))
meta_box.fill.solid()
meta_box.fill.fore_color.rgb = C_WHITE
meta_box.line.color.rgb = C_BORDER
meta_box.line.width = Pt(1)

tx_meta = slide1.shapes.add_textbox(Inches(0.9), Inches(4.25), Inches(11.5), Inches(2.55))
tf_meta = tx_meta.text_frame
tf_meta.word_wrap = True

def add_meta_row(tf, label, val, is_first=False, val_color=C_DARK, is_bold=False):
    p = tf.paragraphs[0] if is_first else tf.add_paragraph()
    p.space_after = Pt(6)
    r1 = p.add_run()
    r1.text = f"{label:30s}: "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY

    r2 = p.add_run()
    r2.text = val
    r2.font.name = FONT_NAME
    r2.font.size = Pt(12)
    r2.font.bold = is_bold
    r2.font.color.rgb = val_color

add_meta_row(tf_meta, "Participant / Candidate", "Prokash Ghosh", is_first=True, val_color=C_PINK, is_bold=True)
add_meta_row(tf_meta, "Host Organization", "Rajasthan Royals (via Unstop Platform)")
add_meta_row(tf_meta, "Round 1 Challenge", "Identify the Most Reliable Players Under Pressure")
add_meta_row(tf_meta, "Dataset Examined", "367 IPL Matches (2022–2026) & 500 T20 Internationals (200,999 Deliveries)")
add_meta_row(tf_meta, "Methodological Indices", "Batting Pressure Reliability Index (BPRI) & Bowling Pressure Reliability Index (BoPRI)")
add_meta_row(tf_meta, "Submission Deliverables", "Official Top 10 Batters, Top 10 Bowlers & Integrated RR Auction Target Shortlist")

# ==========================================
# SLIDE 2: EXECUTIVE SUMMARY
# ==========================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "1. Executive Summary & Strategic Architecture")
add_footer(slide2, 2)

cards_data_s2 = [
    (
        "1. Phase Par Disparity & Baseline Normalization",
        "• Historical league economy accelerates from 6.86 rpo in Over 1 to 11.44 rpo in Over 20.\n"
        "• Comparing raw strike rate or economy across phases is mathematically invalid.\n"
        "• Our model measures performance strictly against over-specific historical par expectations,\n"
        "  properly rewarding death specialists conceding 9.5 rpo while penalizing middle-over leakage.",
        C_NAVY
    ),
    (
        "2. Quantifying Clutch Delta Uplift Under Fire",
        "• True pressure reliability requires elevating output when win probability is actively contested.\n"
        "• Top finishers Naman Dhir (+48.6 SR delta) and Shashank Singh (+58.9 SR delta) surge under stress.\n"
        "• Conversely, high-volume front-runners who pad stats in low-leverage situations are penalized.\n"
        "• Empirical Bayes shrinkage (K=100 balls) ensures small-sample flukes do not distort rankings.",
        C_PINK_DARK
    ),
    (
        "3. Run Suppression Dominance: Mystery Spin & Yorker Pace",
        "• Under extreme match pressure, run containment is governed by two elite bowling archetypes:\n"
        "  1. Mystery Finger/Wrist Spin (Sunil Narine: 5.99 Econ; Mitchell Santner: 6.92 Econ).\n"
        "  2. Deceptive Sling & Skid Yorker Pace (Hasan Mahmud: 11.9 SR; Jasprit Bumrah: 7.36 Econ).\n"
        "• These bowlers create defensive fortresses by exceeding 40% dot-ball rates in death overs.",
        C_NAVY
    ),
    (
        "4. Actionable Rajasthan Royals IPL 2027 Auction Playbook",
        "• Addresses RR's historic tactical gaps: death over finishing and restrictive middle-overs spin.\n"
        "• Balances marquee franchise bids (Tim David, Bumrah) with high-ROI value steals.\n"
        "• Unveils hidden gems: Shashank Singh (middle crunch), Hasan Mahmud (death yorkers),\n"
        "  Mitchell Santner (Jaipur conditions fit), and Jamie Overton (145kph pace + lower order hitting).",
        C_PINK_DARK
    )
]

for idx, (title, desc, col) in enumerate(cards_data_s2):
    left = Inches(0.6 + (idx % 2) * 6.15)
    top = Inches(1.15 + (idx // 2) * 2.85)
    
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.95), Inches(2.72))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    accent = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.14), Inches(2.72))
    accent.fill.solid()
    accent.fill.fore_color.rgb = col
    accent.line.color.rgb = col

    tx = slide2.shapes.add_textbox(left + Inches(0.28), top + Inches(0.18), Inches(5.5), Inches(2.35))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_NAME
    p.font.size = Pt(14.5)
    p.font.bold = True
    p.font.color.rgb = col
    p.space_after = Pt(8)
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_NAME
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_DARK

# ==========================================
# SLIDE 3: DATA PACK OVERVIEW & AUDIT
# ==========================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "2. Data Pack Overview & Quality Audit")
add_footer(slide3, 3)

rows_s3 = [
    ["ball_by_ball.csv", "200,999", "Delivery-level match records across 867 fixtures", "Primary event log; situational state reconstruction"],
    ["matches.csv", "883", "Match metadata, DLS targets, playoff tags, results", "Contextual chase target derivation & playoff leverage"],
    ["competitions.csv", "141", "Format tags (IPL vs T20I) & seasons (2022 to 2026)", "Competition quality weighting (IPL = 1.2x weighting)"],
    ["playing_eleven.csv", "28,381", "Lineup appearances, batting orders, Impact Players", "Role identification & tactical usage validation"],
    ["competition_team_player_mapping.csv", "6,413", "1,210 unique player-team-competition records", "Roster mapping & IPL eligibility verification"],
    ["teams.csv", "353", "Team IDs and franchise associations", "Franchise structure & tournament linkage"]
]

table_shape_s3 = slide3.shapes.add_table(7, 4, Inches(0.6), Inches(1.15), Inches(12.133), Inches(2.95))
table_s3 = table_shape_s3.table
table_s3.columns[0].width = Inches(2.8)
table_s3.columns[1].width = Inches(1.2)
table_s3.columns[2].width = Inches(4.2)
table_s3.columns[3].width = Inches(3.933)

headers_s3 = ["Table Name", "Records", "Key Features & Content", "Analytical Purpose in Study"]
for col_idx, h_text in enumerate(headers_s3):
    cell = table_s3.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.text = h_text
    p = cell.text_frame.paragraphs[0]
    p.font.name = FONT_NAME
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

for row_idx, r_data in enumerate(rows_s3, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s3.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_DARK
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY

# Bottom Two Cards (Filling from 4.25 to 6.85)
card_s3_left = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.30), Inches(5.95), Inches(2.55))
card_s3_left.fill.solid()
card_s3_left.fill.fore_color.rgb = C_WHITE
card_s3_left.line.color.rgb = C_BORDER

tx_s3_l = slide3.shapes.add_textbox(Inches(0.85), Inches(4.40), Inches(5.5), Inches(2.35))
tf_s3_l = tx_s3_l.text_frame
tf_s3_l.word_wrap = True

p_l_title = tf_s3_l.paragraphs[0]
p_l_title.text = "Cricket Accounting & Data Cleansing Protocols"
p_l_title.font.name = FONT_NAME
p_l_title.font.size = Pt(13)
p_l_title.font.bold = True
p_l_title.font.color.rgb = C_NAVY
p_l_title.space_after = Pt(4)

p_l_body = tf_s3_l.add_paragraph()
p_l_body.text = (
    "• Balls Faced Definition: Excludes extras_type == 'wide'; includes overstep no-balls.\n"
    "• Bowler Runs Conceded: Excludes fielding extras (byes/leg-byes); includes off-bat runs + wides + no-balls.\n"
    "• Wicket Attribution: Strictly bowler dismissals (Bowled, Caught, LBW, Stumped, Hit Wicket).\n"
    "• Chase State Engine: Dynamically tracked cumulative scores, wickets in hand, balls remaining, and RRR."
)
p_l_body.font.name = FONT_NAME
p_l_body.font.size = Pt(11)
p_l_body.font.color.rgb = C_DARK

card_s3_right = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), Inches(4.30), Inches(5.95), Inches(2.55))
card_s3_right.fill.solid()
card_s3_right.fill.fore_color.rgb = C_WHITE
card_s3_right.line.color.rgb = C_BORDER

tx_s3_r = slide3.shapes.add_textbox(Inches(7.03), Inches(4.40), Inches(5.5), Inches(2.35))
tf_s3_r = tx_s3_r.text_frame
tf_s3_r.word_wrap = True

p_r_title = tf_s3_r.paragraphs[0]
p_r_title.text = "Dataset Scope, Limitations & Auction Eligibility"
p_r_title.font.name = FONT_NAME
p_r_title.font.size = Pt(13)
p_r_title.font.bold = True
p_r_title.font.color.rgb = C_PINK_DARK
p_r_title.space_after = Pt(4)

p_r_body = tf_s3_r.add_paragraph()
p_r_body.text = (
    "• Competition Hierarchy: IPL matches receive 1.2x competitive weight due to extreme bowling depth.\n"
    "• Auction Eligibility Filter: BCCI regulations prohibit Pakistani players from IPL auctions;\n"
    "  they are documented for completeness but excluded from RR's actionable shortlist.\n"
    "• Retired Veterans: Players retired from IPL active rosters (e.g. Karthik, Bravo) are segregated.\n"
    "• Sample Thresholds: Min 100 balls for batters and 120 balls for bowlers to qualify for leaderboards."
)
p_r_body.font.name = FONT_NAME
p_r_body.font.size = Pt(11)
p_r_body.font.color.rgb = C_DARK

# ==========================================
# SLIDE 4: DEFINING PRESSURE
# ==========================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "3. Defining Pressure: Quantitative Match Leverage")
add_footer(slide4, 4)

# Left Philosophy Box (Full Height: 1.15 to 6.85)
card_s4_l = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.15), Inches(4.8), Inches(5.70))
card_s4_l.fill.solid()
card_s4_l.fill.fore_color.rgb = C_WHITE
card_s4_l.line.color.rgb = C_BORDER

tx_s4_l = slide4.shapes.add_textbox(Inches(0.85), Inches(1.30), Inches(4.3), Inches(5.40))
tf_s4_l = tx_s4_l.text_frame
tf_s4_l.word_wrap = True

p_s4_t = tf_s4_l.paragraphs[0]
p_s4_t.text = "Leverage State Philosophy"
p_s4_t.font.name = FONT_NAME
p_s4_t.font.size = Pt(16)
p_s4_t.font.bold = True
p_s4_t.font.color.rgb = C_NAVY
p_s4_t.space_after = Pt(6)

p_s4_sub = tf_s4_l.add_paragraph()
p_s4_sub.text = "Why Match Context Overrides Raw Overs"
p_s4_sub.font.name = FONT_NAME
p_s4_sub.font.size = Pt(12)
p_s4_sub.font.bold = True
p_s4_sub.font.color.rgb = C_PINK_DARK
p_s4_sub.space_after = Pt(10)

p_s4_desc = tf_s4_l.add_paragraph()
p_s4_desc.text = (
    "A standard flaw in cricket analytics is treating all death-over deliveries as identical high-pressure events. "
    "Bowling in Over 19 when the batting team needs 75 runs with 2 wickets left is a low-leverage mop-up. "
    "Conversely, batting in Over 11 at 45/4 chasing 180 is high-crisis pressure.\n\n"
    "To isolate genuine pressure, our model classifies every delivery through an objective 7-State Match Leverage Matrix:\n\n"
    "1. Second-Innings Chase Dynamics: Tracks live required rate, balls remaining, and remaining wickets.\n"
    "2. First-Innings Par Acceleration: Captures terminal overs (16–20) and top-order powerplay collapses (<=30/3).\n"
    "3. Sudden-Death Situations: Super Overs where win probability swings 100% on a single delivery.\n\n"
    "Result: 65,796 deliveries (32.7% of the dataset) qualify as true pressure situations, eliminating garbage-time distortion."
)
p_s4_desc.font.name = FONT_NAME
p_s4_desc.font.size = Pt(11.5)
p_s4_desc.font.color.rgb = C_DARK

# Right Table (Full Height: 1.15 to 6.85)
table_shape_s4 = slide4.shapes.add_table(8, 3, Inches(5.6), Inches(1.15), Inches(7.133), Inches(5.70))
table_s4 = table_shape_s4.table
table_s4.columns[0].width = Inches(2.2)
table_s4.columns[1].width = Inches(2.3)
table_s4.columns[2].width = Inches(2.633)

headers_s4 = ["Match Context", "Situational Criteria & Thresholds", "Cricketing Rationale & Leverage Dynamics"]
for col_idx, h_text in enumerate(headers_s4):
    cell = table_s4.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.text = h_text
    p = cell.text_frame.paragraphs[0]
    p.font.name = FONT_NAME
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

rows_s4 = [
    ["Chasing: Death Crunch (Inn 2, Overs 16–20)", "Balls rem <= 30, Runs needed 1–75, RRR between 7.0 & 24.0", "Contest actively contested; each dot ball spikes RRR; boundary swings win prob by 20%."],
    ["Chasing: Steep Middle Crunch (Inn 2, Overs 11–15)", "RRR >= 9.5 to 18.0, Wickets in hand <= 7", "The chase is slipping away; batters cannot afford dots; bowlers have field-restriction support."],
    ["Chasing: Tight Finish Window (Inn 2, Final 36 Balls)", "Balls rem <= 36, Runs needed <= 55, RRR >= 7.0", "Game strictly on the line; one bad over seals defeat; direct psychological pressure."],
    ["Chasing: Collapse Crisis (Inn 2, 4+ Wkts Down)", "Wickets fallen >= 4, Runs needed >= 30, Balls rem >= 12", "Top order wiped out; specialist must rebuild while maintaining the required run rate."],
    ["First Innings: Death Overs (Inn 1, Overs 16–20)", "Over ID >= 16 (all deliveries in overs 16 to 20)", "Terminal scoring overs that dictate above-par totals; bowlers execute wide yorkers."],
    ["First Innings: Powerplay Crisis (Inn 1, Overs 1–10)", "Cumulative wickets fallen >= 3 inside first 10 overs", "Crisis stabilization: batting team faces sub-120 wipeout; bowling team hunts kill breakthroughs."],
    ["Super Overs (Clutch Pinnacle)", "All deliveries in Innings 3 or higher (tiebreaker)", "Sudden-death tiebreaker; maximum psychological and win-probability leverage."]
]

for row_idx, r_data in enumerate(rows_s4, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s4.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(10)
            p.font.color.rgb = C_DARK
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY

# ==========================================
# SLIDE 5: METHODOLOGY & SCORING FORMULATION
# ==========================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "4. Methodology & Reliability Scoring Formulation")
add_footer(slide5, 5)

# Left Column: Principles (Full Height: 1.15 to 6.85)
card_s5_l = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.15), Inches(4.8), Inches(5.70))
card_s5_l.fill.solid()
card_s5_l.fill.fore_color.rgb = C_WHITE
card_s5_l.line.color.rgb = C_BORDER

tx_s5_l = slide5.shapes.add_textbox(Inches(0.85), Inches(1.30), Inches(4.3), Inches(5.40))
tf_s5_l = tx_s5_l.text_frame
tf_s5_l.word_wrap = True

p_s5_t = tf_s5_l.paragraphs[0]
p_s5_t.text = "Mathematical Architecture"
p_s5_t.font.name = FONT_NAME
p_s5_t.font.size = Pt(16)
p_s5_t.font.bold = True
p_s5_t.font.color.rgb = C_NAVY
p_s5_t.space_after = Pt(6)

p_s5_desc = tf_s5_l.add_paragraph()
p_s5_desc.text = (
    "To eliminate subjective bias, player reliability is quantified via two composite index formulations: "
    "BPRI (Batting) and BoPRI (Bowling), grounded in three core statistical tenets:\n\n"
    "1. Over-by-Over Baseline Standardization:\n"
    "Every delivery is benchmarked against the league-wide expected scoring rate for that exact over number (Over 1 = 6.86 rpo; Over 20 = 11.44 rpo). "
    "Runs Above Expected (RAE) measures genuine value creation.\n\n"
    "2. Clutch Delta Uplift (&Delta;SR & &Delta;Econ):\n"
    "Substantial weighting is assigned to how much a player elevates above their own normal baseline:\n"
    "&Delta;SR = SR_pressure - SR_normal\n"
    "&Delta;Econ = Econ_normal - Econ_pressure\n\n"
    "3. Empirical Bayes Sample Shrinkage:\n"
    "To prevent small-sample anomalies from topping leaderboards, raw index scores regress to median (50.0) via:\n"
    "w_sample = N / (N + K)\n"
    "where K_bat = 100 balls and K_bowl = 120 balls."
)
p_s5_desc.font.name = FONT_NAME
p_s5_desc.font.size = Pt(11)
p_s5_desc.font.color.rgb = C_DARK

# Right Column: Formula Tables (Full Height: 1.15 to 6.85)
table_shape_s5 = slide5.shapes.add_table(14, 4, Inches(5.6), Inches(1.15), Inches(7.133), Inches(5.70))
table_s5 = table_shape_s5.table
table_s5.columns[0].width = Inches(2.3)
table_s5.columns[1].width = Inches(2.2)
table_s5.columns[2].width = Inches(0.9)
table_s5.columns[3].width = Inches(1.733)

headers_s5 = ["Component Metric", "Mathematical Formulation", "Weight", "Cricketing Objective"]
for col_idx, h_text in enumerate(headers_s5):
    cell = table_s5.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.text = h_text
    p = cell.text_frame.paragraphs[0]
    p.font.name = FONT_NAME
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

rows_s5 = [
    ["BPRI Composite (Batting)", "100 * [RawScore * w + 0.50 * (1-w)]", "100%", "Overall pressure batting index."],
    ["• Pressure Strike Rate", "(Runs_p / Balls_p) * 100", "25%", "Raw scoring velocity under fire."],
    ["• Runs Above Expected", "((Runs_p - E[Runs_over]) / Balls) * 100", "20%", "Value relative to over par expectation."],
    ["• Dismissal Resistance", "Runs_p / max(1, Dismissals_p)", "15%", "Crisis survival & anchoring depth."],
    ["• Clutch Delta Uplift", "SR_pressure - SR_normal", "15%", "Elevation over non-pressure baseline."],
    ["• Match Consistency Rate", "Innings with Runs>=E[Runs] or SR>=145", "15%", "Match-to-match probability of impact."],
    ["• Boundary Percentage", "((4s_p + 6s_p) / Balls_p) * 100", "10%", "Fence-finding against boundary riders."],
    ["BoPRI Composite (Bowling)", "100 * [RawScore * w + 0.50 * (1-w)]", "100%", "Overall pressure bowling index."],
    ["• Runs Saved Per Over", "(E[Runs_over] - Conceded) / (Balls/6)", "25%", "True run suppression vs phase par."],
    ["• Pressure Economy Rate", "Conceded / (Balls_p / 6)", "20%", "Absolute scoring containment."],
    ["• Bowling Strike Rate", "Balls_p / max(1, Wickets_p)", "20%", "Partnership-breaking frequency."],
    ["• Spell Consistency Rate", "Spells with Runs<=E[Runs] or Wkts>=1", "15%", "Reliability of spell execution."],
    ["• Dot Ball Percentage", "(Dots_p / Balls_p) * 100", "10%", "Dot generation to choke chases."]
]

for row_idx, r_data in enumerate(rows_s5, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s5.cell(row_idx, col_idx)
        cell.fill.solid()
        if "Composite" in r_data[0]:
            cell.fill.fore_color.rgb = C_LIGHT_PINK if "Batting" in r_data[0] else C_LIGHT_BLUE
        else:
            cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK
            if "Composite" in r_data[0] or col_idx == 0:
                p.font.bold = True
                if "Composite" in r_data[0]:
                    p.font.color.rgb = C_PINK_DARK if "Batting" in r_data[0] else C_NAVY

# ==========================================
# SLIDE 6: OFFICIAL TOP 10 BATTERS
# ==========================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "5. Official Top 10 Batters (Unstop Submission Dropdown)")
add_footer(slide6, 6)

top10_batters_data = [
    ["1", "Naman Dhir", "Top-Order / Middle Enforcer", "258", "195.7", "36.1", "+48.6 SR", "90.0%", "82.3"],
    ["2", "Shashank Singh", "Clutch Finisher / Crisis Anchor", "361", "182.5", "47.1", "+58.9 SR", "72.7%", "81.3"],
    ["3", "Tim David", "Elite Death Finisher & Power Hitter", "758", "188.8", "34.1", "+29.2 SR", "78.4%", "80.8"],
    ["4", "Suryakumar Yadav", "360° Specialist Middle Anchor", "678", "183.0", "33.5", "+22.0 SR", "71.4%", "76.6"],
    ["5", "Rishabh Pant", "Clutch Wicketkeeper-Batter (LHB)", "380", "172.4", "31.2", "+42.3 SR", "80.0%", "75.2"],
    ["6", "Andre Russell", "Explosive Death Finisher / Pace AR", "513", "180.3", "28.0", "+30.8 SR", "63.6%", "73.7"],
    ["7", "Jos Buttler", "Elite Opening Anchor & Finisher", "337", "182.2", "25.6", "+30.4 SR", "81.5%", "72.9"],
    ["8", "David Miller", "Proven Chase Finisher (LHB)", "838", "163.4", "33.4", "+40.7 SR", "67.9%", "72.9"],
    ["9", "Heinrich Klaasen", "Spin Enforcer / Death Destroyer", "717", "175.0", "35.9", "+16.7 SR", "68.2%", "72.1"],
    ["10", "Rinku Singh", "High-Efficiency Left-Hand Finisher", "836", "166.0", "33.9", "+38.2 SR", "57.9%", "72.1"]
]

table_shape_s6 = slide6.shapes.add_table(11, 9, Inches(0.6), Inches(1.15), Inches(12.133), Inches(4.30))
table_s6 = table_shape_s6.table
col_w_s6 = [Inches(0.6), Inches(2.1), Inches(2.733), Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.2)]
for i, w in enumerate(col_w_s6):
    table_s6.columns[i].width = w

headers_s6 = ["Rank", "Player Name", "Primary Role", "Balls", "SR (p)", "Avg (p)", "Clutch Delta", "Consistency", "BPRI Score"]
for col_idx, h_text in enumerate(headers_s6):
    cell = table_s6.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.text = h_text
    p = cell.text_frame.paragraphs[0]
    p.font.name = FONT_NAME
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    if col_idx in [0, 3, 4, 5, 6, 7, 8]:
        p.alignment = PP_ALIGN.CENTER

for row_idx, r_data in enumerate(top10_batters_data, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s6.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(11)
            p.font.color.rgb = C_DARK
            if col_idx in [0, 3, 4, 5, 6, 7, 8]:
                p.alignment = PP_ALIGN.CENTER
            if col_idx == 1:
                p.font.bold = True
                p.font.color.rgb = C_NAVY
            if col_idx == 8:
                p.font.bold = True
                p.font.color.rgb = C_PINK_DARK

# Bottom Takeaway Card (Filling from 5.55 to 6.90)
takeaway_s6 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.55), Inches(12.133), Inches(1.35))
takeaway_s6.fill.solid()
takeaway_s6.fill.fore_color.rgb = C_WHITE
takeaway_s6.line.color.rgb = C_BORDER

tx_t6 = slide6.shapes.add_textbox(Inches(0.85), Inches(5.62), Inches(11.6), Inches(1.20))
tf_t6 = tx_t6.text_frame
tf_t6.word_wrap = True

p_t6 = tf_t6.paragraphs[0]
p_t6.text = "Official Unstop Batting Selections — Analytical Verification & Strategic Takeaways:"
p_t6.font.name = FONT_NAME
p_t6.font.size = Pt(12)
p_t6.font.bold = True
p_t6.font.color.rgb = C_NAVY
p_t6.space_after = Pt(3)

p_t6_desc = tf_t6.add_paragraph()
p_t6_desc.text = (
    "• Naman Dhir (Rank 1, BPRI 82.3) and Shashank Singh (Rank 2, BPRI 81.3) demonstrate extraordinary clutch elevation (+48.6 and +58.9 SR deltas).\n"
    "• Tim David (Rank 3, BPRI 80.8) provides elite death power striking (188.8 SR, 758 balls), while Rishabh Pant (+42.3 delta) offers unique left-hand crisis counter-attacking.\n"
    "• All 10 selected batters are active, auction-eligible targets directly selectable in the Unstop Round 1 dropdown list."
)
p_t6_desc.font.name = FONT_NAME
p_t6_desc.font.size = Pt(11)
p_t6_desc.font.color.rgb = C_DARK

# ==========================================
# SLIDE 7: OFFICIAL TOP 10 BOWLERS
# ==========================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "6. Official Top 10 Bowlers (Unstop Submission Dropdown)")
add_footer(slide7, 7)

top10_bowlers_data = [
    ["1", "Sunil Narine", "Mystery Off-Spinner / Choke Artist", "461", "5.99", "14.9", "+2.52 rpo", "43.1%", "73.8"],
    ["2", "Hasan Mahmud", "Skid-Pace Death Yorker Specialist", "166", "6.83", "11.9", "+2.30 rpo", "44.5%", "68.8"],
    ["3", "Mitchell Santner", "Left-Arm Orthodox Spin Squeezer", "519", "6.92", "15.3", "+1.78 rpo", "38.6%", "66.1"],
    ["4", "Rashid Khan", "World-Class Leg-Spin Enforcer", "1044", "7.41", "13.2", "+1.22 rpo", "40.8%", "64.3"],
    ["5", "Jasprit Bumrah", "Generational Death & Powerplay Fast", "662", "7.36", "14.7", "+2.12 rpo", "41.2%", "64.0"],
    ["6", "Varun Chakravarthy", "Mystery Leg-Cutter Specialist", "697", "7.50", "12.9", "+1.12 rpo", "42.3%", "63.7"],
    ["7", "Mujeeb Ur Rahman", "Powerplay & Middle Mystery Spinner", "215", "6.95", "14.3", "+1.78 rpo", "40.6%", "63.0"],
    ["8", "Mahedi Hasan", "Economical Powerplay Off-Spinner", "230", "6.83", "19.2", "+1.72 rpo", "37.9%", "61.5"],
    ["9", "Jamie Overton", "Hit-the-Deck Express Pacer (145k)", "204", "8.29", "9.7", "+1.07 rpo", "35.7%", "60.1"],
    ["10", "Sikandar Raza", "Veteran Finger-Spin Squeezer", "340", "6.76", "22.7", "+1.64 rpo", "38.2%", "59.2"]
]

table_shape_s7 = slide7.shapes.add_table(11, 9, Inches(0.6), Inches(1.15), Inches(12.133), Inches(4.30))
table_s7 = table_shape_s7.table
col_w_s7 = [Inches(0.6), Inches(2.1), Inches(2.733), Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.1), Inches(1.2)]
for i, w in enumerate(col_w_s7):
    table_s7.columns[i].width = w

headers_s7 = ["Rank", "Bowler Name", "Primary Role", "Balls", "Econ (p)", "SR (p)", "Runs Saved", "Dot Ball %", "BoPRI Score"]
for col_idx, h_text in enumerate(headers_s7):
    cell = table_s7.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.text = h_text
    p = cell.text_frame.paragraphs[0]
    p.font.name = FONT_NAME
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    if col_idx in [0, 3, 4, 5, 6, 7, 8]:
        p.alignment = PP_ALIGN.CENTER

for row_idx, r_data in enumerate(top10_bowlers_data, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s7.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(11)
            p.font.color.rgb = C_DARK
            if col_idx in [0, 3, 4, 5, 6, 7, 8]:
                p.alignment = PP_ALIGN.CENTER
            if col_idx == 1:
                p.font.bold = True
                p.font.color.rgb = C_NAVY
            if col_idx == 8:
                p.font.bold = True
                p.font.color.rgb = C_PINK_DARK

# Bottom Takeaway Card (Filling from 5.55 to 6.90)
takeaway_s7 = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.55), Inches(12.133), Inches(1.35))
takeaway_s7.fill.solid()
takeaway_s7.fill.fore_color.rgb = C_WHITE
takeaway_s7.line.color.rgb = C_BORDER

tx_t7 = slide7.shapes.add_textbox(Inches(0.85), Inches(5.62), Inches(11.6), Inches(1.20))
tf_t7 = tx_t7.text_frame
tf_t7.word_wrap = True

p_t7 = tf_t7.paragraphs[0]
p_t7.text = "Official Unstop Bowling Selections — Analytical Verification & Strategic Takeaways:"
p_t7.font.name = FONT_NAME
p_t7.font.size = Pt(12)
p_t7.font.bold = True
p_t7.font.color.rgb = C_NAVY
p_t7.space_after = Pt(3)

p_t7_desc = tf_t7.add_paragraph()
p_t7_desc.text = (
    "• Sunil Narine (Rank 1, BoPRI 73.8) stands peerless with a 5.99 economy rate and +2.52 runs saved per over under pressure.\n"
    "• Hasan Mahmud (Rank 2, BoPRI 68.8) is the premier death yorker revelation (11.9 strike rate, 44.5% dot balls), while Mitchell Santner (6.92 Econ) is RR's ideal Jaipur spin fit.\n"
    "• Note: Matheesha Pathirana ranks #11 overall but #7 in strike bowling (11.9 SR, 50 pressure wickets); highlighted as RR's primary overseas pace target."
)
p_t7_desc.font.name = FONT_NAME
p_t7_desc.font.size = Pt(11)
p_t7_desc.font.color.rgb = C_DARK

# Helper for 3-Card Profiles (Full Height: 1.15 to 6.85)
def add_three_profile_cards(slide, cards_info):
    for idx, (rank, name, role, bpri, stats, strength, risk, rr_fit, col) in enumerate(cards_info):
        left = Inches(0.6 + idx * 4.12)
        top = Inches(1.15)
        width = Inches(3.90)
        height = Inches(5.70)
        
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(1.05))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = col
        header_box.line.color.rgb = col
        
        tx_h = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.06), width - Inches(0.3), Inches(0.92))
        tf_h = tx_h.text_frame
        tf_h.word_wrap = True
        
        p_rk = tf_h.paragraphs[0]
        p_rk.text = f"RANK {rank} | {name.upper()}"
        p_rk.font.name = FONT_NAME
        p_rk.font.size = Pt(17)
        p_rk.font.bold = True
        p_rk.font.color.rgb = C_WHITE
        p_rk.space_after = Pt(2)
        
        p_role = tf_h.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_NAME
        p_role.font.size = Pt(11.5)
        p_role.font.italic = True
        p_role.font.color.rgb = C_GOLD
        
        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(1.15), width - Inches(0.4), height - Inches(1.25))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p_score = tf.paragraphs[0]
        p_score.text = f"Reliability Score: {bpri}"
        p_score.font.name = FONT_NAME
        p_score.font.size = Pt(15)
        p_score.font.bold = True
        p_score.font.color.rgb = col
        p_score.space_after = Pt(10)
        
        p_stats = tf.add_paragraph()
        r1 = p_stats.add_run()
        r1.text = "Key Pressure Metrics:\n"
        r1.font.bold = True
        r1.font.size = Pt(12.5)
        r1.font.color.rgb = C_NAVY
        r2 = p_stats.add_run()
        r2.text = stats
        r2.font.size = Pt(12)
        r2.font.color.rgb = C_DARK
        p_stats.space_after = Pt(10)
        
        p_str = tf.add_paragraph()
        r3 = p_str.add_run()
        r3.text = "Analytical Strength:\n"
        r3.font.bold = True
        r3.font.size = Pt(12.5)
        r3.font.color.rgb = C_NAVY
        r4 = p_str.add_run()
        r4.text = strength
        r4.font.size = Pt(12)
        r4.font.color.rgb = C_DARK
        p_str.space_after = Pt(10)
        
        p_risk = tf.add_paragraph()
        r5 = p_risk.add_run()
        r5.text = "Limitation / Risk:\n"
        r5.font.bold = True
        r5.font.size = Pt(12.5)
        r5.font.color.rgb = C_NAVY
        r6 = p_risk.add_run()
        r6.text = risk
        r6.font.size = Pt(12)
        r6.font.color.rgb = C_DARK
        p_risk.space_after = Pt(10)
        
        p_fit = tf.add_paragraph()
        r7 = p_fit.add_run()
        r7.text = "RR Tactical Fit (IPL 2027):\n"
        r7.font.bold = True
        r7.font.size = Pt(13)
        r7.font.color.rgb = C_PINK_DARK
        r8 = p_fit.add_run()
        r8.text = rr_fit
        r8.font.size = Pt(12)
        r8.font.bold = True
        r8.font.color.rgb = C_DARK

# ==========================================
# SLIDE 8: BATTERS 1 TO 3
# ==========================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "7. In-Depth Profiles: Primary Batting Targets (1 to 3)")
add_footer(slide8, 8)

batters_1_3 = [
    (
        1, "Naman Dhir", "Top-Order / Middle Aggressor (RHB)", "BPRI 82.3 (Rank 1)",
        "• 258 pressure balls | 505 runs\n• 195.7 SR | 36.1 Avg | +48.6 SR Delta\n• 90.0% Consistency Rate",
        "Fearless boundary striking against high-pace hard lengths; creates instantaneous momentum without consuming dot balls.",
        "Young domestic sample size; occasionally vulnerable to elite wrist-spin early in the innings.",
        "Solves RR's middle-overs intent void at No. 3 or 4. Allows Samson to anchor while Dhir dismantles opposition bowling.",
        C_PINK_DARK
    ),
    (
        2, "Shashank Singh", "Clutch Finisher / Crisis Anchor (RHB)", "BPRI 81.3 (Rank 2)",
        "• 361 pressure balls | 659 runs\n• 182.5 SR | 47.1 Avg | +58.9 SR Delta\n• 72.7% Consistency Rate",
        "Master of steep run chases; possesses the highest clutch delta (+58.9 SR) in the entire dataset with 47.1 average.",
        "Late career breakout (32 years old); requires a clearly defined lower-order role (No. 6 or 7).",
        "The ultimate Indian crisis finisher RR has lacked. Pairs with Dhruv Jurel and Hetmyer to form an elite chase closing unit.",
        C_PINK_DARK
    ),
    (
        3, "Tim David", "Elite Death Finisher & Power Hitter", "BPRI 80.8 (Rank 3)",
        "• 758 pressure balls | 1,431 runs\n• 188.8 SR | 34.1 Avg | +29.2 SR Delta\n• 78.4% Consistency Rate",
        "Tremendous raw power; 27.4% boundary percentage in death overs; routinely clears 85m Jaipur boundaries.",
        "High auction valuation; occasionally susceptible to wide outside-off yorker traps.",
        "Marquee overseas finisher. Provides RR with proven capability to chase 60 off the final 4 overs at Sawai Mansingh Stadium.",
        C_NAVY
    )
]
add_three_profile_cards(slide8, batters_1_3)

# ==========================================
# SLIDE 9: BATTERS 4 TO 6
# ==========================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "8. In-Depth Profiles: Core Middle-Order Batters (4 to 6)")
add_footer(slide9, 9)

batters_4_6 = [
    (
        4, "Suryakumar Yadav", "360° Specialist Middle Anchor", "BPRI 76.6 (Rank 4)",
        "• 678 pressure balls | 1,241 runs\n• 183.0 SR | 33.5 Avg | +22.0 SR Delta\n• 71.4% Consistency Rate",
        "Effortless field manipulation; sweeps express pace behind square; neutralizes all bowling variations.",
        "High retention probability by MI; commands premium budget if available in mega-auction.",
        "Franchise anchor blueprint. Disarms opposition tactical plans and dictates tempo in high-leverage chases.",
        C_NAVY
    ),
    (
        5, "Rishabh Pant", "Clutch Wicketkeeper-Batter (LHB)", "BPRI 75.2 (Rank 5)",
        "• 380 pressure balls | 655 runs\n• 172.4 SR | 31.2 Avg | +42.3 SR Delta\n• 80.0% Consistency Rate",
        "Unique left-handed match-winner; counter-attacks top-order collapses with audacious boundary striking.",
        "High-risk shot selection creates variance; significant purse allocation required.",
        "Brings elite left-handed middle-order balance, neutralizes leg-spin in Jaipur, and relieves Samson of keeping duties.",
        C_PINK_DARK
    ),
    (
        6, "Andre Russell", "Explosive Death Finisher / Pace AR", "BPRI 73.7 (Rank 6)",
        "• 513 pressure balls | 925 runs\n• 180.3 SR | 28.0 Avg | +30.8 SR Delta\n• 63.6% Consistency Rate",
        "Unrivaled muscle power; strikes at 200+ against death pace; bowls high-impact heavy-ball overs.",
        "Injury and workload management required; higher dot-ball percentage prior to acceleration.",
        "Game-changing power asset. Capable of winning 2 to 3 unwinnable matches per season single-handedly.",
        C_NAVY
    )
]
add_three_profile_cards(slide9, batters_4_6)

# ==========================================
# SLIDE 10: BOWLERS 1 TO 4 (2x2 Grid)
# ==========================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "9. In-Depth Profiles: Primary Bowling Targets (1 to 4)")
add_footer(slide10, 10)

bowlers_1_4 = [
    (
        1, "Sunil Narine", "Mystery Off-Spinner / Choke Artist", "BoPRI 73.8",
        "461 balls | 31 wkts | 5.99 Econ | 14.9 SR | +2.52 Runs Saved/Ov",
        "Peerless economy under pressure (5.99 rpo); batters cannot read his carrom ball seam variations under lights.",
        "Long-term KKR affiliation; veteran age bracket.",
        "The gold standard for run suppression. Bowls Over 18/19 with field up and maintains sub-6.0 economy.",
        C_NAVY
    ),
    (
        2, "Hasan Mahmud", "Skid-Pace Death Yorker Specialist", "BoPRI 68.8",
        "166 balls | 14 wkts | 6.83 Econ | 11.9 SR | +2.30 Runs Saved/Ov",
        "Executes reverse-swinging yorkers at high pace; skids under the bat with low trajectory in terminal overs.",
        "Relatively modest IPL exposure; international bilateral dominance.",
        "Top-Priority Value Steal for RR: Highly affordable overseas death bowler who perfectly complements Sandeep Sharma.",
        C_PINK_DARK
    ),
    (
        3, "Mitchell Santner", "Left-Arm Orthodox Spin Squeezer", "BoPRI 66.1",
        "519 balls | 34 wkts | 6.92 Econ | 15.3 SR | +1.78 Runs Saved/Ov",
        "Flawless trajectory and pace variance; denies batters boundary elevation; provides lower-order batting depth.",
        "Lacks express mystery turn; relies on discipline and arm balls.",
        "Tactical Fit of the Century: Under-utilized in auctions; gives RR 4 miserly overs and reliable runs at No. 8.",
        C_NAVY
    ),
    (
        4, "Rashid Khan", "World-Class Leg-Spin Enforcer", "BoPRI 64.3",
        "1044 balls | 79 wkts | 7.41 Econ | 13.2 SR | +1.22 Runs Saved/Ov",
        "High arm speed (98 kph) makes googly unpickable; takes 79 pressure wickets when opposition requires 10+ rpo.",
        "Top-tier auction retention asset; commands maximum budget.",
        "Generational T20 match-winner; transforms middle overs into an impenetrable defensive fortress.",
        C_GOLD
    )
]

for idx, (rank, name, role, bopri, stats, strength, risk, rr_fit, col) in enumerate(bowlers_1_4):
    left = Inches(0.6 + (idx % 2) * 6.15)
    top = Inches(1.15 + (idx // 2) * 2.85)
    width = Inches(5.95)
    height = Inches(2.72)
    
    card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    accent = slide10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.14), height)
    accent.fill.solid()
    accent.fill.fore_color.rgb = col
    accent.line.color.rgb = col
    
    tx = slide10.shapes.add_textbox(left + Inches(0.25), top + Inches(0.10), width - Inches(0.35), height - Inches(0.18))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = f"RANK {rank} | {name.upper()} ({bopri})"
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(15.5)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    p_t.space_after = Pt(4)
    
    p_r = tf.add_paragraph()
    p_r.text = f"{role}\nKey Metrics: {stats}"
    p_r.font.name = FONT_NAME
    p_r.font.size = Pt(12)
    p_r.font.bold = True
    p_r.font.color.rgb = C_NAVY
    p_r.space_after = Pt(4)
    
    p_s = tf.add_paragraph()
    p_s.text = f"Analytical Strength: {strength}"
    p_s.font.name = FONT_NAME
    p_s.font.size = Pt(11.5)
    p_s.font.color.rgb = C_DARK
    p_s.space_after = Pt(4)
    
    p_f = tf.add_paragraph()
    p_f.text = f"RR Tactical Fit: {rr_fit}"
    p_f.font.name = FONT_NAME
    p_f.font.size = Pt(12)
    p_f.font.bold = True
    p_f.font.color.rgb = C_PINK_DARK

# ==========================================
# SLIDE 11: SPECIALIST PACE & MYSTERY SPIN (5, 6, 9 + PATHIRANA)
# ==========================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "10. In-Depth Profiles: Specialist Pace & Mystery Spin")
add_footer(slide11, 11)

bowlers_5_6_9 = [
    (
        5, "Jasprit Bumrah", "Generational Fast Bowler", "BoPRI 64.0 (Rank 5)",
        "• 662 balls | 45 wkts\n• 7.36 Econ | 14.7 SR\n• +2.12 Runs Saved/Ov",
        "Hyperextension release creates lethal dipping yorkers and hostile bouncers; impossible to hit in Over 19.",
        "Guaranteed Mumbai Indians retention; unattainable in open auction without mega-auction release.",
        "The gold benchmark against whom all RR pace bowling targets are evaluated.",
        C_NAVY
    ),
    (
        6, "Varun Chakravarthy", "Mystery Leg-Cutter Specialist", "BoPRI 63.7 (Rank 6)",
        "• 697 balls | 54 wkts\n• 7.50 Econ | 12.9 SR\n• 42.3% Dot Ball Rate",
        "High-release mystery spin that darts both ways; takes crucial middle-overs wickets to break partnerships.",
        "Requires pristine grip conditions; heavy dew can reduce second-innings spin bite.",
        "Primary domestic spin target to replace the wicket-taking impact of Yuzvendra Chahal.",
        C_PINK_DARK
    ),
    (
        9, "Jamie Overton", "Hit-the-Deck Express Pacer (145k)", "BoPRI 60.1 (Rank 9)",
        "• 204 balls | 21 wkts\n• 8.29 Econ | 9.7 SR\n• SR 165+ Lower-Order Bat",
        "Pounds the pitch with heavy length at 145kph; boasts a remarkable 9.7 balls-per-wicket strike rate.",
        "Can concede boundaries if batters anticipate the short-pitched enforcer strategy.",
        "High-Value Pace Allrounder: Solves RR's search for an overseas pace all-rounder bowling death overs.",
        C_NAVY
    )
]

for idx, (rank, name, role, bopri, stats, strength, risk, rr_fit, col) in enumerate(bowlers_5_6_9):
    left = Inches(0.6 + idx * 4.12)
    top = Inches(1.15)
    width = Inches(3.90)
    height = Inches(4.30)
    
    card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    header_box = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(1.05))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = col
    header_box.line.color.rgb = col
    
    tx_h = slide11.shapes.add_textbox(left + Inches(0.15), top + Inches(0.06), width - Inches(0.3), Inches(0.92))
    tf_h = tx_h.text_frame
    tf_h.word_wrap = True
    
    p_rk = tf_h.paragraphs[0]
    p_rk.text = f"RANK {rank} | {name.upper()}"
    p_rk.font.name = FONT_NAME
    p_rk.font.size = Pt(16.5)
    p_rk.font.bold = True
    p_rk.font.color.rgb = C_WHITE
    p_rk.space_after = Pt(2)
    
    p_role = tf_h.add_paragraph()
    p_role.text = role
    p_role.font.name = FONT_NAME
    p_role.font.size = Pt(11.5)
    p_role.font.italic = True
    p_role.font.color.rgb = C_GOLD
    
    tx = slide11.shapes.add_textbox(left + Inches(0.18), top + Inches(1.15), width - Inches(0.36), height - Inches(1.25))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_score = tf.paragraphs[0]
    p_score.text = f"Reliability Rating: {bopri}"
    p_score.font.name = FONT_NAME
    p_score.font.size = Pt(14)
    p_score.font.bold = True
    p_score.font.color.rgb = col
    p_score.space_after = Pt(8)
    
    p_stats = tf.add_paragraph()
    r1 = p_stats.add_run()
    r1.text = "Pressure Stats:\n"
    r1.font.bold = True
    r1.font.size = Pt(12)
    r1.font.color.rgb = C_NAVY
    r2 = p_stats.add_run()
    r2.text = stats
    r2.font.size = Pt(12)
    r2.font.color.rgb = C_DARK
    p_stats.space_after = Pt(8)
    
    p_str = tf.add_paragraph()
    r3 = p_str.add_run()
    r3.text = "Key Analytical Strength:\n"
    r3.font.bold = True
    r3.font.size = Pt(12)
    r3.font.color.rgb = C_NAVY
    r4 = p_str.add_run()
    r4.text = strength
    r4.font.size = Pt(12)
    r4.font.color.rgb = C_DARK
    p_str.space_after = Pt(8)
    
    p_fit = tf.add_paragraph()
    r5 = p_fit.add_run()
    r5.text = "RR Tactical Fit:\n"
    r5.font.bold = True
    r5.font.size = Pt(12.5)
    r5.font.color.rgb = C_PINK_DARK
    r6 = p_fit.add_run()
    r6.text = rr_fit
    r6.font.size = Pt(12)
    r6.font.bold = True
    r6.font.color.rgb = C_DARK

# Bottom Card: Matheesha Pathirana & Honorable Mentions (Filling from 5.55 to 6.90)
card_s11_bot = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.55), Inches(12.133), Inches(1.35))
card_s11_bot.fill.solid()
card_s11_bot.fill.fore_color.rgb = C_WHITE
card_s11_bot.line.color.rgb = C_BORDER

tx_s11_b = slide11.shapes.add_textbox(Inches(0.85), Inches(5.62), Inches(11.6), Inches(1.20))
tf_s11_b = tx_s11_b.text_frame
tf_s11_b.word_wrap = True

p_b_t = tf_s11_b.paragraphs[0]
p_b_t.text = "Marquee Pace Target Highlight: Matheesha Pathirana (Rank 11 Overall | Rank 7 Strike Bowling)"
p_b_t.font.name = FONT_NAME
p_b_t.font.size = Pt(13.5)
p_b_t.font.bold = True
p_b_t.font.color.rgb = C_PINK_DARK
p_b_t.space_after = Pt(3)

p_b_d = tf_s11_b.add_paragraph()
p_b_d.text = (
    "• 596 pressure balls | 50 wickets | 11.9 strike rate | 81.0% consistency. Extreme slinging angle makes 148kph yorkers unplayable.\n"
    "• While early-spell wides slightly inflate his economy (8.95), his pure strike weapon rating is elite. Primary overseas fast-bowler target for RR.\n"
    "• Honorable Mentions: Mujeeb Ur Rahman (Rank 7, 6.95 Econ), Mahedi Hasan (Rank 8, 6.83 Econ), Sikandar Raza (Rank 10, 6.76 Econ)."
)
p_b_d.font.name = FONT_NAME
p_b_d.font.size = Pt(11.5)
p_b_d.font.color.rgb = C_DARK

# ==========================================
# SLIDE 12: COMPARATIVE CLUTCH ANALYTICS
# ==========================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "11. Comparative Clutch Analytics & Delta Uplift")
add_footer(slide12, 12)

# Left: Batting Quadrant (Image + Text Card, 1.15 to 6.85)
chart2_path = "figures/chart2_batting_quadrant.png"
if os.path.exists(chart2_path):
    slide12.shapes.add_picture(chart2_path, Inches(0.6), Inches(1.15), Inches(5.95), Inches(3.90))

card_s12_l = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.15), Inches(5.95), Inches(1.70))
card_s12_l.fill.solid()
card_s12_l.fill.fore_color.rgb = C_WHITE
card_s12_l.line.color.rgb = C_BORDER

tx_s12_l = slide12.shapes.add_textbox(Inches(0.8), Inches(5.22), Inches(5.55), Inches(1.55))
tf_s12_l = tx_s12_l.text_frame
tf_s12_l.word_wrap = True

p_12_lt = tf_s12_l.paragraphs[0]
p_12_lt.text = "Batting Quadrant Analysis: The Clutch Surge"
p_12_lt.font.name = FONT_NAME
p_12_lt.font.size = Pt(12)
p_12_lt.font.bold = True
p_12_lt.font.color.rgb = C_PINK_DARK
p_12_lt.space_after = Pt(3)

p_12_ld = tf_s12_l.add_paragraph()
p_12_ld.text = (
    "• Top-Right Quadrant: Elite Clutch performers who elevate above baseline under pressure.\n"
    "• Naman Dhir (+48.6 SR) and Shashank Singh (+58.9 SR) anchor the extreme upper tier.\n"
    "• Front-runners who pad stats in low-leverage phases suffer negative deltas and fall away."
)
p_12_ld.font.name = FONT_NAME
p_12_ld.font.size = Pt(10.5)
p_12_ld.font.color.rgb = C_DARK

# Right: Bowling Quadrant (Image + Text Card, 1.15 to 6.85)
chart4_path = "figures/chart4_bowling_quadrant.png"
if os.path.exists(chart4_path):
    slide12.shapes.add_picture(chart4_path, Inches(6.78), Inches(1.15), Inches(5.95), Inches(3.90))

card_s12_r = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), Inches(5.15), Inches(5.95), Inches(1.70))
card_s12_r.fill.solid()
card_s12_r.fill.fore_color.rgb = C_WHITE
card_s12_r.line.color.rgb = C_BORDER

tx_s12_r = slide12.shapes.add_textbox(Inches(6.98), Inches(5.22), Inches(5.55), Inches(1.55))
tf_s12_r = tx_s12_r.text_frame
tf_s12_r.word_wrap = True

p_12_rt = tf_s12_r.paragraphs[0]
p_12_rt.text = "Bowling Quadrant Analysis: Run Savers vs Strikers"
p_12_rt.font.name = FONT_NAME
p_12_rt.font.size = Pt(12)
p_12_rt.font.bold = True
p_12_rt.font.color.rgb = C_NAVY
p_12_rt.space_after = Pt(3)

p_12_rd = tf_s12_r.add_paragraph()
p_12_rd.text = (
    "• Top-Right Quadrant: Elite combination of run suppression (positive runs saved) & lethal strike rates.\n"
    "• Narine (+2.52 Runs Saved) and Hasan Mahmud (+2.30 Runs Saved, 11.9 SR) dominate the quadrant.\n"
    "• Pathirana stands out as the supreme strike weapon with 50 pressure wickets."
)
p_12_rd.font.name = FONT_NAME
p_12_rd.font.size = Pt(10.5)
p_12_rd.font.color.rgb = C_DARK

# ==========================================
# SLIDE 13: STATISTICAL ROBUSTNESS & SENSITIVITY
# ==========================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "12. Statistical Robustness & Multi-Model Sensitivity")
add_footer(slide13, 13)

# Left Column: Heatmap Image + Analysis Card (1.15 to 6.85)
chart6_path = "figures/chart6_sensitivity_heatmap.png"
if os.path.exists(chart6_path):
    slide13.shapes.add_picture(chart6_path, Inches(0.6), Inches(1.15), Inches(5.60), Inches(3.90))

card_s13_l = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.15), Inches(5.60), Inches(1.70))
card_s13_l.fill.solid()
card_s13_l.fill.fore_color.rgb = C_WHITE
card_s13_l.line.color.rgb = C_BORDER

tx_s13_l = slide13.shapes.add_textbox(Inches(0.8), Inches(5.22), Inches(5.20), Inches(1.55))
tf_s13_l = tx_s13_l.text_frame
tf_s13_l.word_wrap = True

p_13_lt = tf_s13_l.paragraphs[0]
p_13_lt.text = "Mathematical Invariance: Spearman Correlation > 0.896"
p_13_lt.font.name = FONT_NAME
p_13_lt.font.size = Pt(11.5)
p_13_lt.font.bold = True
p_13_lt.font.color.rgb = C_NAVY
p_13_lt.space_after = Pt(2)

p_13_ld = tf_s13_l.add_paragraph()
p_13_ld.text = (
    "• Across 4 contrasting weight architectures (Baseline, Aggression, Stability, Clutch Delta),\n"
    "  Spearman rank correlation remains > 0.962 for batting and > 0.896 for bowling.\n"
    "• Demonstrates mathematical stability: top selections do not collapse under altered weights."
)
p_13_ld.font.name = FONT_NAME
p_13_ld.font.size = Pt(10)
p_13_ld.font.color.rgb = C_DARK

# Right Column: Multi-Model Rank Comparison Table (1.15 to 6.85)
table_shape_s13 = slide13.shapes.add_table(7, 6, Inches(6.45), Inches(1.15), Inches(6.283), Inches(5.70))
table_s13 = table_shape_s13.table
col_w_s13 = [Inches(1.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(1.283)]
for i, w in enumerate(col_w_s13):
    table_s13.columns[i].width = w

headers_s13 = ["Player", "Base", "Aggr", "Stab", "Delta", "Sensitivity & Disclosure Notes"]
for col_idx, h_text in enumerate(headers_s13):
    cell = table_s13.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.text = h_text
    p = cell.text_frame.paragraphs[0]
    p.font.name = FONT_NAME
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    if col_idx in [1, 2, 3, 4]:
        p.alignment = PP_ALIGN.CENTER

rows_s13 = [
    ["Naman Dhir", "1", "2", "2", "2", "Invariant; ranks Top 2 across all models due to 195.7 SR and 90% consistency."],
    ["Shashank Singh", "2", "5", "1", "1", "Ranks #1 in Stability & Delta models due to 47.1 Avg and +58.9 SR surge."],
    ["Tim David", "3", "1", "3", "4", "Becomes #1 under Aggression due to huge volume (758 balls) and 188.8 SR."],
    ["Heinrich Klaasen", "9", "11", "9", "25", "Disclosure: Sensitive to Delta weight because baseline normal SR is already elite."],
    ["Sunil Narine", "1", "1", "1", "1", "Undisputed #1 bowler across all four models (5.99 Econ, 2.52 Runs Saved)."],
    ["Matheesha Pathirana", "11", "7", "19", "16", "Disclosure: Jumps to Top 7 under Strike Focus (11.9 SR), but dips under pure economy."]
]

for row_idx, r_data in enumerate(rows_s13, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s13.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_DARK
            if col_idx in [1, 2, 3, 4]:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_NAVY

# ==========================================
# SLIDE 14: RR IPL 2027 STRATEGIC AUCTION PLAYBOOK
# ==========================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "13. Rajasthan Royals IPL 2027 Strategic Auction Playbook")
add_footer(slide14, 14)

# Left Column: Auction Matrix Image + Core Strategy Card (1.15 to 6.85)
chart7_path = "figures/chart7_rr_auction_matrix.png"
if os.path.exists(chart7_path):
    slide14.shapes.add_picture(chart7_path, Inches(0.6), Inches(1.15), Inches(5.60), Inches(3.90))

card_s14_l = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.15), Inches(5.60), Inches(1.70))
card_s14_l.fill.solid()
card_s14_l.fill.fore_color.rgb = C_WHITE
card_s14_l.line.color.rgb = C_BORDER

tx_s14_l = slide14.shapes.add_textbox(Inches(0.8), Inches(5.22), Inches(5.20), Inches(1.55))
tf_s14_l = tx_s14_l.text_frame
tf_s14_l.word_wrap = True

p_14_lt = tf_s14_l.paragraphs[0]
p_14_lt.text = "Franchise Portfolio Acquisition Strategy"
p_14_lt.font.name = FONT_NAME
p_14_lt.font.size = Pt(11.5)
p_14_lt.font.bold = True
p_14_lt.font.color.rgb = C_PINK_DARK
p_14_lt.space_after = Pt(2)

p_14_ld = tf_s14_l.add_paragraph()
p_14_ld.text = (
    "• Solves RR's Historical Tactical Deficits: Death over boundary-hitting & middle spin choke.\n"
    "• Capitalizes on Market Asymmetry: Casual franchises overpay for marquee names in bidding wars;\n"
    "  RR acquires elite pressure performance at 30% of cost via Hasan Mahmud, Santner & Overton."
)
p_14_ld.font.name = FONT_NAME
p_14_ld.font.size = Pt(10)
p_14_ld.font.color.rgb = C_DARK

# Right Column: 4-Tier Auction Portfolio Table (1.15 to 6.85)
table_shape_s14 = slide14.shapes.add_table(5, 4, Inches(6.45), Inches(1.15), Inches(6.283), Inches(5.70))
table_s14 = table_shape_s14.table
col_w_s14 = [Inches(1.45), Inches(1.65), Inches(1.70), Inches(1.483)]
for i, w in enumerate(col_w_s14):
    table_s14.columns[i].width = w

headers_s14 = ["Auction Strategy Tier", "Target Players", "Tactical Role in RR Squad", "Financial & Purse Rationale"]
for col_idx, h_text in enumerate(headers_s14):
    cell = table_s14.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    cell.margin_left = Inches(0.06)
    cell.margin_right = Inches(0.06)
    cell.margin_top = Inches(0.06)
    cell.margin_bottom = Inches(0.06)
    cell.text = h_text
    for p in cell.text_frame.paragraphs:
        p.font.name = FONT_NAME
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

rows_s14 = [
    [
        "Tier 1: Primary Core Targets (Aggressive)",
        "• Naman Dhir\n• Tim David\n• M. Pathirana",
        "Solves chronic weaknesses: middle intent (Dhir), terminal death hitting (David), and unplayable sling pace (Pathirana).",
        "High-impact match-winners worth 15–25% purse allocation; guaranteed Starting XI fixtures."
    ],
    [
        "Tier 2: High-Value Targets (Calculated)",
        "• Shashank Singh\n• V. Chakravarthy",
        "Shashank anchors crisis run chases; Varun provides mystery wicket-taking to fill Chahal/Ashwin void.",
        "Proven Indian match-winners; commands competitive bidding while saving overseas slots."
    ],
    [
        "Tier 3: Tactical Value Buys (Max ROI)",
        "• Hasan Mahmud\n• Mitchell Santner\n• Jamie Overton",
        "Hasan provides reverse-swing yorkers; Santner delivers 6.92 Econ & batting depth; Overton hits 145kph + SR 165+ bat.",
        "Steal Targets: Often fly under radar; deliver 85% of marquee output at 25-30% of auction purse."
    ],
    [
        "Tier 4: Developmental Upside (Low Purse)",
        "• Ashutosh Sharma\n• Mujeeb Ur Rahman",
        "Ashutosh sweeps express pace into stands; Mujeeb locks down Powerplays on turning Jaipur wickets.",
        "High-upside targets under 3-5 Crore; ideal Impact Player candidates offering tactical flexibility."
    ]
]

for row_idx, r_data in enumerate(rows_s14, 1):
    for col_idx, val in enumerate(r_data):
        cell = table_s14.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 1 else C_LIGHT
        cell.margin_left = Inches(0.06)
        cell.margin_right = Inches(0.06)
        cell.margin_top = Inches(0.06)
        cell.margin_bottom = Inches(0.06)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_NAME
            p.font.size = Pt(10)
            p.font.color.rgb = C_DARK
            if col_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_PINK_DARK
            elif col_idx == 1:
                p.font.bold = True
                p.font.color.rgb = C_NAVY
                p.space_after = Pt(2)

# ==========================================
# SLIDE 15: CONCLUSION & UNSTOP CHECKLIST
# ==========================================
slide15 = prs.slides.add_slide(blank_layout)
add_header(slide15, "14. Conclusion & Unstop Submission Checklist")
add_footer(slide15, 15)

# Top Summary Banner (1.15 to 2.50)
top_s15 = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.15), Inches(12.133), Inches(1.40))
top_s15.fill.solid()
top_s15.fill.fore_color.rgb = C_WHITE
top_s15.line.color.rgb = C_BORDER

tx_top_15 = slide15.shapes.add_textbox(Inches(0.85), Inches(1.22), Inches(11.6), Inches(1.25))
tf_top_15 = tx_top_15.text_frame
tf_top_15.word_wrap = True

p_15_t = tf_top_15.paragraphs[0]
p_15_t.text = "Analytical Synthesis & Final Strategic Recommendation for Rajasthan Royals"
p_15_t.font.name = FONT_NAME
p_15_t.font.size = Pt(13.5)
p_15_t.font.bold = True
p_15_t.font.color.rgb = C_NAVY
p_15_t.space_after = Pt(3)

p_15_d = tf_top_15.add_paragraph()
p_15_d.text = (
    "By synthesizing state leverage dynamics, over-adjusted par expectations, and empirical Bayes shrinkage across 200,999 deliveries, "
    "this dossier successfully isolates genuine pressure reliability from noise. For Rajasthan Royals, adopting an evidence-based acquisition portfolio "
    "anchored by Naman Dhir, Shashank Singh, Tim David, Hasan Mahmud, and Mitchell Santner delivers maximum tactical impact, squad balance, and purse efficiency."
)
p_15_d.font.name = FONT_NAME
p_15_d.font.size = Pt(11)
p_15_d.font.color.rgb = C_DARK

# Bottom-Left: Official Checklist (2.70 to 6.85)
card_s15_bl = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(2.70), Inches(6.8), Inches(4.15))
card_s15_bl.fill.solid()
card_s15_bl.fill.fore_color.rgb = C_WHITE
card_s15_bl.line.color.rgb = C_BORDER

tx_s15_bl = slide15.shapes.add_textbox(Inches(0.85), Inches(2.80), Inches(6.3), Inches(3.95))
tf_s15_bl = tx_s15_bl.text_frame
tf_s15_bl.word_wrap = True

p_chk_t = tf_s15_bl.paragraphs[0]
p_chk_t.text = "Unstop Round 1 Dropdown Submission Checklist"
p_chk_t.font.name = FONT_NAME
p_chk_t.font.size = Pt(13)
p_chk_t.font.bold = True
p_chk_t.font.color.rgb = C_PINK_DARK
p_chk_t.space_after = Pt(6)

checklist_items = [
    ("Top 10 Batters (Unstop)", "1. Naman Dhir, 2. Shashank Singh, 3. Tim David, 4. Suryakumar Yadav, 5. Rishabh Pant, 6. Andre Russell, 7. Jos Buttler, 8. David Miller, 9. Heinrich Klaasen, 10. Rinku Singh."),
    ("Top 10 Bowlers (Unstop)", "1. Sunil Narine, 2. Hasan Mahmud, 3. Mitchell Santner, 4. Rashid Khan, 5. Jasprit Bumrah, 6. Varun Chakravarthy, 7. Mujeeb Ur Rahman, 8. Mahedi Hasan, 9. Jamie Overton, 10. Sikandar Raza."),
    ("Methodology Report", "15-page comprehensive analytics dossier formatted in Times New Roman & RR Pink palette."),
    ("Player Verification", "Zero duplicates; 100% active and auction-eligible player selections verified against BCCI rules."),
    ("Full Reproducibility", "End-to-end Python scripts, rankings CSV exports, and Jupyter Notebook persisted in workspace.")
]

for label, desc in checklist_items:
    p_item = tf_s15_bl.add_paragraph()
    p_item.space_after = Pt(4)
    r1 = p_item.add_run()
    r1.text = f"[PASS] {label}: "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY
    
    r2 = p_item.add_run()
    r2.text = desc
    r2.font.name = FONT_NAME
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_DARK

# Bottom-Right: Sources & Formal Sign-Off (2.70 to 6.85)
card_s15_br = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.6), Inches(2.70), Inches(5.133), Inches(4.15))
card_s15_br.fill.solid()
card_s15_br.fill.fore_color.rgb = C_WHITE
card_s15_br.line.color.rgb = C_BORDER

tx_s15_br = slide15.shapes.add_textbox(Inches(7.85), Inches(2.80), Inches(4.65), Inches(3.95))
tf_s15_br = tx_s15_br.text_frame
tf_s15_br.word_wrap = True

p_src_t = tf_s15_br.paragraphs[0]
p_src_t.text = "References & Methodological Foundation"
p_src_t.font.name = FONT_NAME
p_src_t.font.size = Pt(13)
p_src_t.font.bold = True
p_src_t.font.color.rgb = C_NAVY
p_src_t.space_after = Pt(6)

p_src_d = tf_s15_br.add_paragraph()
p_src_d.text = (
    "1. BCCI / IPL Official Rules: Retention guidelines & auction eligibility criteria.\n"
    "2. ESPNcricinfo & Cricbuzz: Domestic T20 records for role classification.\n"
    "3. Leverage Index Principles: Adapted from Tango et al. (The Book) & Win Probability Added in T20.\n"
    "4. Empirical Bayes Shrinkage: Efron & Morris (1975) athletic rate normalization."
)
p_src_d.font.name = FONT_NAME
p_src_d.font.size = Pt(10.5)
p_src_d.font.color.rgb = C_DARK
p_src_d.space_after = Pt(10)

p_sign_t = tf_s15_br.add_paragraph()
p_sign_t.text = "Candidate & Submission Certification:"
p_sign_t.font.name = FONT_NAME
p_sign_t.font.size = Pt(11)
p_sign_t.font.bold = True
p_sign_t.font.color.rgb = C_PINK_DARK
p_sign_t.space_after = Pt(2)

p_sign_d = tf_s15_br.add_paragraph()
p_sign_d.text = (
    "Participant: Prokash Ghosh\n"
    "Competition: SupeRR Selector Season 2 | Round 1\n"
    "Host: Rajasthan Royals Cricket Operations\n"
    "Status: Official Final Deliverable — Verified & Complete"
)
p_sign_d.font.name = FONT_NAME
p_sign_d.font.size = Pt(10.5)
p_sign_d.font.bold = True
p_sign_d.font.color.rgb = C_NAVY

pptx_out = "d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx"
prs.save(pptx_out)
print(f"EXPANDED POWERPOINT PRESENTATION SAVED SUCCESSFULLY AT: {pptx_out}")

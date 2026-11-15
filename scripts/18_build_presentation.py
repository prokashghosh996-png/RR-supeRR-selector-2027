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
C_NAVY = RGBColor(0, 28, 88)      # #001C58 Deep Royal Navy
C_GOLD = RGBColor(212, 175, 55)   # #D4AF37 Trophy Gold
C_DARK = RGBColor(26, 29, 32)     # #1A1D20 Dark Charcoal
C_GREY = RGBColor(90, 100, 114)   # #5A6472 Muted Grey
C_LIGHT = RGBColor(248, 249, 250) # #F8F9FA Soft White
C_WHITE = RGBColor(255, 255, 255)
C_CARD_BG = RGBColor(253, 254, 254)
C_BORDER = RGBColor(203, 213, 225)

FONT_NAME = 'Times New Roman'

blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="RAJASTHAN ROYALS | SupeRR Selector Season 2"):
    # Header bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.95))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_NAVY
    top_bar.line.color.rgb = C_NAVY
    
    # Pink accent line
    pink_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0.95), Inches(13.333), Inches(0.06))
    pink_line.fill.solid()
    pink_line.fill.fore_color.rgb = C_PINK
    pink_line.line.color.rgb = C_PINK

    # Header category text
    tx_cat = slide.shapes.add_textbox(Inches(0.6), Inches(0.08), Inches(12), Inches(0.3))
    tf_cat = tx_cat.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = FONT_NAME
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_GOLD

    # Header main title
    tx_title = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.5))
    tf_title = tx_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_NAME
    p_title.font.size = Pt(17)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE

def add_footer(slide, current_page, total_pages=15):
    # Bottom line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER
    line.line.color.rgb = C_BORDER

    # Footer text
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(7.08), Inches(8), Inches(0.3))
    tf = tx.text_frame
    p = tf.paragraphs[0]
    p.text = "CONFIDENTIAL & PROPRIETARY — PREPARED FOR RAJASTHAN ROYALS | PARTICIPANT: PROKASH GHOSH"
    p.font.name = FONT_NAME
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = C_NAVY

    # Slide number
    tx_num = slide.shapes.add_textbox(Inches(10), Inches(7.08), Inches(2.733), Inches(0.3))
    tf_num = tx_num.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"Slide {current_page} of {total_pages}"
    p_num.font.name = FONT_NAME
    p_num.font.size = Pt(8.5)
    p_num.font.color.rgb = C_GREY

# ==========================================
# SLIDE 1: COVER SLIDE
# ==========================================
slide1 = prs.slides.add_slide(blank_layout)

# Background
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_LIGHT
bg1.line.color.rgb = C_LIGHT

# Main Pink Banner
banner = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(3.3))
banner.fill.solid()
banner.fill.fore_color.rgb = C_PINK
banner.line.color.rgb = C_PINK

# Banner Navy left stripe
stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.2), Inches(3.3))
stripe.fill.solid()
stripe.fill.fore_color.rgb = C_NAVY
stripe.line.color.rgb = C_NAVY

# Banner text
tx_b = slide1.shapes.add_textbox(Inches(1.2), Inches(0.95), Inches(11.0), Inches(2.9))
tf_b = tx_b.text_frame
tf_b.word_wrap = True

p1 = tf_b.paragraphs[0]
p1.text = "RAJASTHAN ROYALS CRICKET OPERATIONS & ANALYTICS"
p1.font.name = FONT_NAME
p1.font.size = Pt(12)
p1.font.bold = True
p1.font.color.rgb = C_GOLD
p1.space_after = Pt(8)

p2 = tf_b.add_paragraph()
p2.text = "SupeRR Selector Season 2"
p2.font.name = FONT_NAME
p2.font.size = Pt(32)
p2.font.bold = True
p2.font.color.rgb = C_WHITE
p2.space_after = Pt(6)

p3 = tf_b.add_paragraph()
p3.text = "Identifying the Most Reliable Players Under Pressure for Rajasthan Royals' IPL 2027 Auction"
p3.font.name = FONT_NAME
p3.font.size = Pt(14)
p3.font.italic = True
p3.font.color.rgb = C_GOLD
p3.space_after = Pt(10)

p4 = tf_b.add_paragraph()
p4.text = "A Multi-Dimensional Empirical Study of 200,999 Deliveries Across 867 T20 Fixtures (IPL & T20I 2022–2026), Establishing Official Top-10 Submissions and Strategic Franchise Acquisition Portfolios."
p4.font.name = FONT_NAME
p4.font.size = Pt(10)
p4.font.color.rgb = RGBColor(255, 240, 245)

# Metadata card on slide 1
meta_box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.35), Inches(11.733), Inches(2.45))
meta_box.fill.solid()
meta_box.fill.fore_color.rgb = C_WHITE
meta_box.line.color.rgb = C_BORDER
meta_box.line.width = Pt(1)

tx_meta = slide1.shapes.add_textbox(Inches(1.1), Inches(4.5), Inches(11.1), Inches(2.1))
tf_meta = tx_meta.text_frame
tf_meta.word_wrap = True

def add_meta_row(tf, label, val, is_first=False, val_color=C_DARK, is_bold=False):
    p = tf.paragraphs[0] if is_first else tf.add_paragraph()
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = f"{label:28s}: "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY

    r2 = p.add_run()
    r2.text = val
    r2.font.name = FONT_NAME
    r2.font.size = Pt(10)
    r2.font.bold = is_bold
    r2.font.color.rgb = val_color

add_meta_row(tf_meta, "Participant / Candidate", "Prokash Ghosh", is_first=True, val_color=C_PINK, is_bold=True)
add_meta_row(tf_meta, "Host Organization", "Rajasthan Royals (via Unstop Platform)")
add_meta_row(tf_meta, "Round 1 Challenge", "Identify the Most Reliable Players Under Pressure")
add_meta_row(tf_meta, "Dataset Examined", "367 IPL Matches (2022–2026) & 500 T20 Internationals (200,999 Deliveries)")
add_meta_row(tf_meta, "Submission Deliverables", "Official Top 10 Batters, Top 10 Bowlers & Integrated RR Auction Target Shortlist")
add_meta_row(tf_meta, "Date of Submission", "November 2026")


# ==========================================
# SLIDE 2: EXECUTIVE SUMMARY
# ==========================================
slide2 = prs.slides.add_slide(blank_layout)
add_header(slide2, "1. Executive Summary & Strategic Architecture")
add_footer(slide2, 2)

# 4 Key Takeaway Cards
cards_data_s2 = [
    ("1. Over-Adjusted Baselines", "League economy accelerates from 6.86 rpo in Over 1 to 11.44 rpo in Over 20. Raw economy or strike rate is heavily misleading without phase normalization.", C_NAVY),
    ("2. Quantifying Clutch Delta", "True reliability requires elevating under fire. Top finishers Naman Dhir (+48.6 SR) and Shashank Singh (+58.9 SR) explode when the game is strictly on the line.", C_PINK),
    ("3. Run Suppression Dominance", "Run suppression under pressure is led by mystery spin (Sunil Narine: 5.99 Econ, Mitchell Santner: 6.92 Econ) and skidding death yorker pace (Hasan Mahmud: 11.9 SR).", C_NAVY),
    ("4. Actionable RR Strategy", "Provides Rajasthan Royals with an optimized auction acquisition portfolio balancing marquee stars with high-ROI value steals (Hasan Mahmud, Santner, Overton).", C_PINK)
]

for idx, (title, desc, col) in enumerate(cards_data_s2):
    left = Inches(0.6 + (idx % 2) * 6.2)
    top = Inches(1.2 + (idx // 2) * 2.7)
    
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.9), Inches(2.45))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    # Left accent line
    accent = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.12), Inches(2.45))
    accent.fill.solid()
    accent.fill.fore_color.rgb = col
    accent.line.color.rgb = col

    tx = slide2.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.4), Inches(2.0))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_NAME
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = col
    p.space_after = Pt(8)
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_NAME
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = C_DARK


# ==========================================
# SLIDE 3: DATA PACK OVERVIEW & INTEGRITY AUDIT
# ==========================================
slide3 = prs.slides.add_slide(blank_layout)
add_header(slide3, "2. Data Pack Overview & Quality Audit")
add_footer(slide3, 3)

rows_s3 = [
    ["ball_by_ball.csv", "200,999", "Delivery-level match records across 867 fixtures", "Primary event log; situational reconstruction"],
    ["matches.csv", "883", "Match metadata, DLS targets, playoff tags, results", "Contextual chase target derivation"],
    ["competitions.csv", "141", "Format tags (IPL vs T20I) & seasons (2022 to 2026)", "Competition quality weighting (IPL = 1.2x)"],
    ["playing_eleven.csv", "28,381", "Lineup appearances, batting orders, Impact Players", "Role identification & usage validation"],
    ["competition_team_player_mapping.csv", "6,413", "1,210 unique player-team-competition records", "Roster mapping & IPL eligibility verification"],
    ["teams.csv", "353", "Team IDs and franchise associations", "Franchise structure & tournament linkage"]
]

# Create table
table_shape = slide3.shapes.add_table(7, 4, Inches(0.6), Inches(1.3), Inches(12.133), Inches(4.5))
table = table_shape.table
table.columns[0].width = Inches(3.0)
table.columns[1].width = Inches(1.3)
table.columns[2].width = Inches(4.2)
table.columns[3].width = Inches(3.633)

headers_s3 = ["Table Name", "Records", "Core Feature Scope", "Analytical Purpose in Study"]
for c_idx, h in enumerate(headers_s3):
    cell = table.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_NAME
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

for r_idx, row in enumerate(rows_s3):
    for c_idx, val in enumerate(row):
        cell = table.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 0 else C_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_NAVY if c_idx == 0 else C_DARK
        p.font.bold = (c_idx == 0)

# Notes below table
tx_s3_note = slide3.shapes.add_textbox(Inches(0.6), Inches(6.0), Inches(12.133), Inches(0.9))
tf_s3 = tx_s3_note.text_frame
p_n = tf_s3.paragraphs[0]
p_n.text = "Data Integrity Highlights: Deliveries where extras_type is 'wide' are excluded from batter balls faced. Bowler runs conceded include off-bat runs plus wides, oversteps, and penalty runs (fielding byes/leg-byes excluded). Bowler wickets include Bowled, Caught, LBW, Stumped, and Hit Wicket."
p_n.font.name = FONT_NAME
p_n.font.size = Pt(9)
p_n.font.italic = True
p_n.font.color.rgb = C_GREY


# ==========================================
# SLIDE 4: DEFINING PRESSURE
# ==========================================
slide4 = prs.slides.add_slide(blank_layout)
add_header(slide4, "3. Defining Pressure: Quantitative Match Leverage")
add_footer(slide4, 4)

# Left text box
tx_s4 = slide4.shapes.add_textbox(Inches(0.6), Inches(1.2), Inches(6.2), Inches(5.6))
tf_s4 = tx_s4.text_frame
tf_s4.word_wrap = True

p = tf_s4.paragraphs[0]
p.text = "Objective Match-State Leverage Criteria"
p.font.name = FONT_NAME
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_PINK
p.space_after = Pt(8)

def add_bullet_point(tf, bold_txt, norm_txt):
    p = tf.add_paragraph()
    p.space_after = Pt(6)
    r1 = p.add_run()
    r1.text = "• " + bold_txt + ": "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY
    
    r2 = p.add_run()
    r2.text = norm_txt
    r2.font.name = FONT_NAME
    r2.font.size = Pt(9)
    r2.font.color.rgb = C_DARK

add_bullet_point(tf_s4, "Chasing Death Crunch (Overs 16–20)", "Balls left <= 30, Runs needed between 1 and 75, RRR between 7.0 and 24.0. Contested match states where single balls trigger 20%+ win probability swings.")
add_bullet_point(tf_s4, "Steep Middle Crunch (Overs 11–15)", "RRR >= 9.5 to 18.0, Wickets in hand <= 7. Scoring must accelerate against boundary protection fields.")
add_bullet_point(tf_s4, "Tight Finish Window (Final 36 Balls)", "Balls remaining <= 36, Runs needed <= 55, RRR >= 7.0. Immediate game-on-the-line execution.")
add_bullet_point(tf_s4, "Collapse Crisis (4+ Wickets Down)", "Innings 2 where 4+ wickets have fallen and 30+ runs are needed.")
add_bullet_point(tf_s4, "1st Innings Death & Powerplay Collapse", "All deliveries in Overs 16–20, or losing 3+ wickets inside the first 10 overs.")
add_bullet_point(tf_s4, "Super Overs", "100% of deliveries in tiebreakers (maximum leverage).")

# Right image: Chart 1
chart1_img = "figures/chart1_pressure_distribution.png"
if os.path.exists(chart1_img):
    slide4.shapes.add_picture(chart1_img, Inches(7.0), Inches(1.5), Inches(5.7), Inches(4.5))


# ==========================================
# SLIDE 5: METHODOLOGY & SCORING ARCHITECTURE
# ==========================================
slide5 = prs.slides.add_slide(blank_layout)
add_header(slide5, "4. Methodology & Reliability Scoring Formulation")
add_footer(slide5, 5)

# Two boxes: Batting BPRI & Bowling BoPRI
box_bat = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.5))
box_bat.fill.solid()
box_bat.fill.fore_color.rgb = C_WHITE
box_bat.line.color.rgb = C_BORDER

# Header inside bat box
h_bat = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.3), Inches(5.9), Inches(0.6))
h_bat.fill.solid()
h_bat.fill.fore_color.rgb = C_PINK
h_bat.line.color.rgb = C_PINK
p = h_bat.text_frame.paragraphs[0]
p.text = "BATTING PRESSURE RELIABILITY INDEX (BPRI)"
p.font.name = FONT_NAME
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_WHITE

tx_b = slide5.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.6))
tf_b = tx_b.text_frame
tf_b.word_wrap = True

p_f1 = tf_b.paragraphs[0]
p_f1.text = "BPRI = 100 × [RawScore × w_sample + 0.50 × (1 − w_sample)]"
p_f1.font.name = FONT_NAME
p_f1.font.size = Pt(9.5)
p_f1.font.bold = True
p_f1.font.color.rgb = C_NAVY
p_f1.space_after = Pt(8)

def add_metric_desc(tf, name, wt, desc):
    p = tf.add_paragraph()
    p.space_after = Pt(4)
    r1 = p.add_run()
    r1.text = f"• {name} ({wt}): "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY
    r2 = p.add_run()
    r2.text = desc
    r2.font.name = FONT_NAME
    r2.font.size = Pt(8)
    r2.font.color.rgb = C_DARK

add_metric_desc(tf_b, "Pressure Strike Rate (SR_p)", "25%", "Scoring velocity under high-pressure states.")
add_metric_desc(tf_b, "Runs Above Expected (RAE100)", "20%", "Runs scored relative to specific over par baseline.")
add_metric_desc(tf_b, "Batting Average under Pressure", "15%", "Runs per dismissal; crisis survival resistance.")
add_metric_desc(tf_b, "Clutch Delta (ΔSR)", "15%", "Uplift over normal non-pressure scoring baseline.")
add_metric_desc(tf_b, "Match-to-Match Consistency", "15%", "% innings delivering positive match impact.")
add_metric_desc(tf_b, "Boundary Percentage", "10%", "(Fours + Sixes) / Pressure balls faced.")
add_metric_desc(tf_b, "Empirical Bayes Shrinkage", "N/(N+100)", "Regresses small samples toward league median.")

# Bowling Box
box_bowl = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.3), Inches(5.9), Inches(5.5))
box_bowl.fill.solid()
box_bowl.fill.fore_color.rgb = C_WHITE
box_bowl.line.color.rgb = C_BORDER

h_bowl = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.3), Inches(5.9), Inches(0.6))
h_bowl.fill.solid()
h_bowl.fill.fore_color.rgb = C_NAVY
h_bowl.line.color.rgb = C_NAVY
p = h_bowl.text_frame.paragraphs[0]
p.text = "BOWLING PRESSURE RELIABILITY INDEX (BoPRI)"
p.font.name = FONT_NAME
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_WHITE

tx_bw = slide5.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.5), Inches(4.6))
tf_bw = tx_bw.text_frame
tf_bw.word_wrap = True

p_f2 = tf_bw.paragraphs[0]
p_f2.text = "BoPRI = 100 × [RawScore × w_sample + 0.50 × (1 − w_sample)]"
p_f2.font.name = FONT_NAME
p_f2.font.size = Pt(9.5)
p_f2.font.bold = True
p_f2.font.color.rgb = C_PINK
p_f2.space_after = Pt(8)

add_metric_desc(tf_bw, "Runs Saved Per Over (RSPO)", "25%", "Runs prevented relative to phase par expectation.")
add_metric_desc(tf_bw, "Pressure Economy Rate", "20%", "Absolute run containment under pressure.")
add_metric_desc(tf_bw, "Bowling Strike Rate (Balls/Wkt)", "20%", "Breakthrough frequency to break dangerous stands.")
add_metric_desc(tf_bw, "Spell Consistency Rate", "15%", "% clutch spells conceding below par or taking 1+ wkts.")
add_metric_desc(tf_bw, "Dot Ball Percentage", "10%", "Dot generation to choke opposition required rates.")
add_metric_desc(tf_bw, "Economy Delta (ΔEcon)", "10%", "Capacity to tighten up under pressure.")
add_metric_desc(tf_bw, "Empirical Bayes Shrinkage", "B/(B+120)", "Shrinks raw scores toward median to avoid flukes.")


# ==========================================
# SLIDE 6: TOP 10 BATTERS (UNSTOP DROPDOWN)
# ==========================================
slide6 = prs.slides.add_slide(blank_layout)
add_header(slide6, "5. Official Top 10 Batters (Unstop Submission Dropdown)")
add_footer(slide6, 6)

bat_t10_data = [
    ["1", "Naman Dhir", "Top/Middle Enforcer", "258", "195.7", "36.1", "+48.6 SR", "82.3", "High"],
    ["2", "Shashank Singh", "Clutch Finisher / Anchor", "361", "182.5", "47.1", "+58.9 SR", "81.3", "Very High"],
    ["3", "Tim David", "Death Finisher / Power Hitter", "758", "188.8", "34.1", "+29.2 SR", "80.8", "Elite"],
    ["4", "Suryakumar Yadav", "360° Specialist Middle Anchor", "678", "183.0", "33.5", "+22.0 SR", "76.6", "Elite"],
    ["5", "Rishabh Pant", "Clutch Wicketkeeper (LHB)", "380", "172.4", "31.2", "+42.3 SR", "75.2", "Very High"],
    ["6", "Andre Russell", "Explosive Finisher / Pace AR", "513", "180.3", "28.0", "+30.8 SR", "73.7", "Very High"],
    ["7", "Jos Buttler", "Elite Anchor & Finisher", "337", "182.2", "25.6", "+30.4 SR", "72.9", "Very High"],
    ["8", "David Miller", "Proven Chase Finisher (LHB)", "838", "163.4", "33.4", "+40.7 SR", "72.9", "Elite"],
    ["9", "Heinrich Klaasen", "Spin Destroyer / Middle Enforcer", "717", "175.0", "35.9", "+16.7 SR", "72.1", "Elite"],
    ["10", "Rinku Singh", "High-Efficiency Finisher (LHB)", "836", "166.0", "33.9", "+38.2 SR", "72.1", "Elite"]
]

t_bat_shape = slide6.shapes.add_table(11, 9, Inches(0.6), Inches(1.3), Inches(12.133), Inches(5.2))
t_bat = t_bat_shape.table
widths_b = [Inches(0.6), Inches(2.2), Inches(2.7), Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.333)]
for c_idx, w in enumerate(widths_b):
    t_bat.columns[c_idx].width = w

headers_bat = ["Rank", "Player Name", "Primary T20 Role", "Balls", "Pressure SR", "Average", "Delta", "BPRI", "Confidence"]
for c_idx, h in enumerate(headers_bat):
    cell = t_bat.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_NAME
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3, 4, 5, 6, 7, 8] else PP_ALIGN.LEFT

for r_idx, row in enumerate(bat_t10_data):
    for c_idx, val in enumerate(row):
        cell = t_bat.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 0 else C_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(9)
        p.font.color.rgb = C_PINK if c_idx == 7 else C_DARK
        p.font.bold = (c_idx in [1, 7])
        p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3, 4, 5, 6, 7, 8] else PP_ALIGN.LEFT


# ==========================================
# SLIDE 7: TOP 10 BOWLERS (UNSTOP DROPDOWN)
# ==========================================
slide7 = prs.slides.add_slide(blank_layout)
add_header(slide7, "6. Official Top 10 Bowlers (Unstop Submission Dropdown)")
add_footer(slide7, 7)

bowl_t10_data = [
    ["1", "Sunil Narine", "Mystery Off-Spin (Multi-Phase)", "461", "5.99", "14.9", "+2.52 rpo", "73.8", "Elite"],
    ["2", "Hasan Mahmud", "Right-Arm Fast (Death Yorker)", "166", "6.83", "11.9", "+2.30 rpo", "68.8", "High"],
    ["3", "Mitchell Santner", "Left-Arm Orthodox (Middle/Death)", "519", "6.92", "15.3", "+1.78 rpo", "66.1", "Elite"],
    ["4", "Rashid Khan", "Leg-Spin Wicket Enforcer", "1044", "7.41", "13.2", "+1.22 rpo", "64.3", "Elite"],
    ["5", "Jasprit Bumrah", "Generational Pace (Yorker King)", "662", "7.36", "14.7", "+2.12 rpo", "64.0", "Elite"],
    ["6", "Varun Chakravarthy", "Mystery Leg-Cutter Specialist", "697", "7.50", "12.9", "+1.12 rpo", "63.7", "Elite"],
    ["7", "Mujeeb Ur Rahman", "Powerplay & Death Carrom Spin", "215", "6.95", "14.3", "+1.78 rpo", "63.0", "High"],
    ["8", "Mahedi Hasan", "Defensive Off-Spin Squeezer", "230", "6.83", "19.2", "+1.72 rpo", "61.5", "High"],
    ["9", "Jamie Overton", "Heavy-Ball Express (145k) / AR", "204", "8.29", "9.7", "+1.07 rpo", "60.1", "High"],
    ["10", "Sikandar Raza", "Veteran Finger-Spin Squeezer", "340", "6.76", "22.7", "+1.64 rpo", "59.2", "Very High"]
]

t_bw_shape = slide7.shapes.add_table(11, 9, Inches(0.6), Inches(1.3), Inches(12.133), Inches(5.2))
t_bw = t_bw_shape.table
widths_bw = [Inches(0.6), Inches(2.2), Inches(2.7), Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.333)]
for c_idx, w in enumerate(widths_bw):
    t_bw.columns[c_idx].width = w

headers_bowl = ["Rank", "Bowler Name", "Primary Discipline & Phase", "Balls", "Economy", "Strike Rate", "Runs Saved", "BoPRI", "Confidence"]
for c_idx, h in enumerate(headers_bowl):
    cell = t_bw.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_NAME
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3, 4, 5, 6, 7, 8] else PP_ALIGN.LEFT

for r_idx, row in enumerate(bowl_t10_data):
    for c_idx, val in enumerate(row):
        cell = t_bw.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 0 else C_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(9)
        p.font.color.rgb = C_PINK if c_idx == 7 else C_DARK
        p.font.bold = (c_idx in [1, 7])
        p.alignment = PP_ALIGN.CENTER if c_idx in [0, 3, 4, 5, 6, 7, 8] else PP_ALIGN.LEFT


# ==========================================
# SLIDE 8: BATTING PROFILES (1 TO 3)
# ==========================================
slide8 = prs.slides.add_slide(blank_layout)
add_header(slide8, "7. In-Depth Profiles: Primary Batting Targets (1 to 3)")
add_footer(slide8, 8)

def render_profile_card_ppt(slide, left_in, top_in, width_in, height_in, rank, name, role, score_lbl, score_val, stats, strength, rr_fit, col):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left_in), Inches(top_in), Inches(width_in), Inches(0.45))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = col
    top_bar.line.color.rgb = col
    
    p_h = top_bar.text_frame.paragraphs[0]
    p_h.text = f"RANK {rank}: {name.upper()}  |  {score_lbl}: {score_val:.1f}"
    p_h.font.name = FONT_NAME
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = C_WHITE

    tx = slide.shapes.add_textbox(Inches(left_in + 0.15), Inches(top_in + 0.5), Inches(width_in - 0.3), Inches(height_in - 0.6))
    tf = tx.text_frame
    tf.word_wrap = True

    def add_p(tf, lbl, val):
        p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
        p.space_after = Pt(4)
        r1 = p.add_run()
        r1.text = lbl + ": "
        r1.font.name = FONT_NAME
        r1.font.size = Pt(9)
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = val
        r2.font.name = FONT_NAME
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = C_DARK

    add_p(tf, "Role", role)
    add_p(tf, "Key Metrics", stats)
    add_p(tf, "Analytical Strength", strength)
    add_p(tf, "RR 2027 Squad Fit", rr_fit)

render_profile_card_ppt(
    slide8, 0.6, 1.3, 3.8, 5.5, 1, "Naman Dhir", "Top/Middle Enforcer (RHB)", "BPRI", 82.3,
    "258 balls | 505 runs | 195.7 SR | 36.1 Avg | +48.6 SR Delta | 90% Consistency",
    "Fearless boundary striking against high-pace hard lengths; ignites momentum from Ball 1.",
    "Fills RR's critical No. 3 or 4 slot; provides middle-overs acceleration without dropping strike rate.",
    C_PINK
)
render_profile_card_ppt(
    slide8, 4.75, 1.3, 3.8, 5.5, 2, "Shashank Singh", "Clutch Finisher / Crisis Anchor", "BPRI", 81.3,
    "361 balls | 659 runs | 182.5 SR | 47.1 Avg | +58.9 SR Delta | 72.7% Consistency",
    "Extraordinary situational awareness in steep run chases; highest clutch delta in dataset.",
    "The ultimate Indian crisis finisher RR has historically lacked; pairs with Jurel and Hetmyer.",
    C_PINK
)
render_profile_card_ppt(
    slide8, 8.9, 1.3, 3.8, 5.5, 3, "Tim David", "Death Finisher & Power Hitter", "BPRI", 80.8,
    "758 balls | 1,431 runs | 188.8 SR | 34.1 Avg | +38.3 Runs Above Expected/100b",
    "Supreme boundary conversion (27.4% boundary pct) in overs 18–20; clears huge boundaries.",
    "Primary overseas target for RR death hitting; gives Rajasthan unmatched late fire-power.",
    C_NAVY
)


# ==========================================
# SLIDE 9: BATTING PROFILES (4 TO 6)
# ==========================================
slide9 = prs.slides.add_slide(blank_layout)
add_header(slide9, "8. In-Depth Profiles: Core Middle-Order Batters (4 to 6)")
add_footer(slide9, 9)

render_profile_card_ppt(
    slide9, 0.6, 1.3, 3.8, 5.5, 4, "Suryakumar Yadav", "360° Specialist Middle Anchor", "BPRI", 76.6,
    "678 balls | 1,241 runs | 183.0 SR | 33.5 Avg | +38.6 Runs Above Expected/100b",
    "Total field manipulation; sweeps express pace behind square and scores freely vs all varieties.",
    "Franchise anchor who completely disarms opposition bowling plans in high-leverage chases.",
    C_NAVY
)
render_profile_card_ppt(
    slide9, 4.75, 1.3, 3.8, 5.5, 5, "Rishabh Pant", "Clutch Wicketkeeper-Batter (LHB)", "BPRI", 75.2,
    "380 balls | 655 runs | 172.4 SR | 31.2 Avg | +42.3 SR Delta | 80% Consistency",
    "Unique left-handed match-winner who thrives under chaos; counter-attacks early collapses.",
    "World-class left-handed counter-attacking balance; takes keeping workload off Samson.",
    C_PINK
)
render_profile_card_ppt(
    slide9, 8.9, 1.3, 3.8, 5.5, 6, "Andre Russell", "Explosive Finisher / Pace All-Rounder", "BPRI", 73.7,
    "513 balls | 925 runs | 180.3 SR | 28.0 Avg | +31.9 Runs Above Expected/100b",
    "Unrivaled raw power; strikes at 200+ against death pace and bowls high-impact heavy-ball overs.",
    "High-impact game changer; wins 2 to 3 unwinnable fixtures per season single-handedly.",
    C_NAVY
)


# ==========================================
# SLIDE 10: BOWLING PROFILES (1 TO 4)
# ==========================================
slide10 = prs.slides.add_slide(blank_layout)
add_header(slide10, "9. In-Depth Profiles: Primary Bowling Targets (1 to 4)")
add_footer(slide10, 10)

render_profile_card_ppt(
    slide10, 0.6, 1.3, 2.85, 5.5, 1, "Sunil Narine", "Mystery Off-Spinner", "BoPRI", 73.8,
    "461 balls | 31 wkts | 5.99 Econ | 14.9 SR | +2.52 Runs Saved/Ov",
    "Peerless economy rate under pressure; impossible-to-read carrom ball.",
    "The gold standard for T20 run suppression. Bowls Over 18/19 sub-6.0.",
    C_NAVY
)
render_profile_card_ppt(
    slide10, 3.65, 1.3, 2.85, 5.5, 2, "Hasan Mahmud", "Death Yorker Specialist", "BoPRI", 68.8,
    "166 balls | 14 wkts | 6.83 Econ | 11.9 SR | +2.30 Runs Saved/Ov",
    "Nails searing reverse-swing yorkers; skids with low trajectory.",
    "High-Priority Overseas Value Steal: Perfect partner for Sandeep.",
    C_PINK
)
render_profile_card_ppt(
    slide10, 6.7, 1.3, 2.85, 5.5, 3, "Mitchell Santner", "Left-Arm Orthodox Squeezer", "BoPRI", 66.1,
    "519 balls | 34 wkts | 6.92 Econ | 15.3 SR | +1.78 Runs Saved/Ov",
    "Flawless trajectory control and speed variance; adds No. 8 batting.",
    "Tactical Steal: Gives RR 4 miserly overs plus vital batting depth.",
    C_NAVY
)
render_profile_card_ppt(
    slide10, 9.75, 1.3, 2.85, 5.5, 4, "Rashid Khan", "Leg-Spin Wicket Enforcer", "BoPRI", 64.3,
    "1044 balls | 79 wkts | 7.41 Econ | 13.2 SR | +1.22 Runs Saved/Ov",
    "Fast arm speed (100kph) makes googly lethal in steep chases.",
    "Generational match-winner; transforms middle overs into a fortress.",
    C_GOLD
)


# ==========================================
# SLIDE 11: BOWLING PROFILES (5 TO 8 / PATHIRANA)
# ==========================================
slide11 = prs.slides.add_slide(blank_layout)
add_header(slide11, "10. In-Depth Profiles: Specialist Pace & Mystery Spin")
add_footer(slide11, 11)

render_profile_card_ppt(
    slide11, 0.6, 1.3, 2.85, 5.5, 5, "Jasprit Bumrah", "Generational Fast Bowler", "BoPRI", 64.0,
    "662 balls | 45 wkts | 7.36 Econ | 14.7 SR | +2.12 Runs Saved/Ov",
    "Hyperextension release creates dipping yorkers; locks down Over 19.",
    "The gold standard pace benchmark for RR talent acquisition.",
    C_NAVY
)
render_profile_card_ppt(
    slide11, 3.65, 1.3, 2.85, 5.5, 6, "Varun Chakravarthy", "Mystery Leg-Cutter", "BoPRI", 63.7,
    "697 balls | 54 wkts | 7.50 Econ | 12.9 SR | 42.3% Dot Ball Rate",
    "High-release mystery spin that grips and darts both ways.",
    "Primary domestic spin target to replace the wicket void of Chahal.",
    C_PINK
)
render_profile_card_ppt(
    slide11, 6.7, 1.3, 2.85, 5.5, 9, "Jamie Overton", "Heavy-Ball Express (145k)", "BoPRI", 60.1,
    "204 balls | 21 wkts | 8.29 Econ | 9.7 SR | +1.07 Runs Saved/Ov",
    "Pounds pitch with 145kph hard length; bats at SR 165+ in death.",
    "Overseas Pace All-Rounder Steal: Solves RR's middle/death balance.",
    C_NAVY
)
render_profile_card_ppt(
    slide11, 9.75, 1.3, 2.85, 5.5, 11, "M. Pathirana", "Sling Yorker Demolisher", "BoPRI", 59.0,
    "596 balls | 50 wkts | 8.95 Econ | 11.9 SR | +1.46 Runs Saved/Ov",
    "148kph slinging angle makes full yorkers unplayable; 50 clutch wkts.",
    "Marquee Death Specialist: Top strike weapon alongside Sandeep.",
    C_PINK
)


# ==========================================
# SLIDE 12: COMPARATIVE CLUTCH ANALYTICS
# ==========================================
slide12 = prs.slides.add_slide(blank_layout)
add_header(slide12, "11. Comparative Clutch Analytics & Delta Uplift")
add_footer(slide12, 12)

chart2_img = "figures/chart2_batting_quadrant.png"
if os.path.exists(chart2_img):
    slide12.shapes.add_picture(chart2_img, Inches(0.6), Inches(1.3), Inches(5.9), Inches(5.4))

chart4_img = "figures/chart4_bowling_quadrant.png"
if os.path.exists(chart4_img):
    slide12.shapes.add_picture(chart4_img, Inches(6.8), Inches(1.3), Inches(5.9), Inches(5.4))


# ==========================================
# SLIDE 13: STATISTICAL ROBUSTNESS & SENSITIVITY
# ==========================================
slide13 = prs.slides.add_slide(blank_layout)
add_header(slide13, "12. Statistical Robustness & Multi-Model Sensitivity")
add_footer(slide13, 13)

# Heatmap picture
chart6_img = "figures/chart6_sensitivity_heatmap.png"
if os.path.exists(chart6_img):
    slide13.shapes.add_picture(chart6_img, Inches(0.6), Inches(1.3), Inches(6.2), Inches(5.4))

# Text commentary on right
tx_s13 = slide13.shapes.add_textbox(Inches(7.1), Inches(1.3), Inches(5.6), Inches(5.4))
tf_s13 = tx_s13.text_frame
tf_s13.word_wrap = True

p = tf_s13.paragraphs[0]
p.text = "Mathematical Proof of Model Stability"
p.font.name = FONT_NAME
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_PINK
p.space_after = Pt(8)

add_bullet_point(tf_s13, "4 Distinct Scoring Schemes Tested", "Simulated Baseline, Aggression (Strike/Wickets focus), Stability (Economy/Avg focus), and Clutch Delta (Uplift focus).")
add_bullet_point(tf_s13, "Extraordinary Rank Invariance", "Spearman rank correlations exceed 0.962 for batting and 0.896 for bowling, confirming selections are not artifacts of subjective weights.")
add_bullet_point(tf_s13, "Sunil Narine & Naman Dhir Invariance", "Sunil Narine remains undisputed #1 bowler across all 4 models; Naman Dhir remains top 2 across all 4 models.")
add_bullet_point(tf_s13, "Disclosure: Heinrich Klaasen", "Drops under Clutch Delta weighting because his normal non-pressure strike rate is already elite (158+), resulting in a smaller delta.")
add_bullet_point(tf_s13, "Disclosure: Matheesha Pathirana", "Rises to #7 under Strike Focus (11.9 SR, 50 wickets), but dips under pure economy due to death over baseline runs.")


# ==========================================
# SLIDE 14: RAJASTHAN ROYALS AUCTION STRATEGY
# ==========================================
slide14 = prs.slides.add_slide(blank_layout)
add_header(slide14, "13. Rajasthan Royals IPL 2027 Strategic Auction Playbook")
add_footer(slide14, 14)

chart7_img = "figures/chart7_rr_auction_matrix.png"
if os.path.exists(chart7_img):
    slide14.shapes.add_picture(chart7_img, Inches(0.6), Inches(1.3), Inches(6.5), Inches(5.4))

# Strategy Table on Right
t_strat_shape = slide14.shapes.add_table(5, 2, Inches(7.3), Inches(1.3), Inches(5.4), Inches(5.4))
t_strat = t_strat_shape.table
t_strat.columns[0].width = Inches(2.2)
t_strat.columns[1].width = Inches(3.2)

strat_rows = [
    ["Tier 1: Primary Targets\n(15–25% Purse)", "Naman Dhir (Intent)\nTim David (Death Hit)\nMatheesha Pathirana (Sling)"],
    ["Tier 2: High-Value Targets\n(Calculated Pursuit)", "Shashank Singh (Crisis Finisher)\nVarun Chakravarthy (Mystery)"],
    ["Tier 3: Tactical Value Buys\n(High ROI Steals)", "Hasan Mahmud (Yorkers)\nMitchell Santner (Squeeze/Bat)\nJamie Overton (145k All-Rounder)"],
    ["Tier 4: Developmental\n(Low Purse / Impact)", "Ashutosh Sharma (Slogger)\nMujeeb Ur Rahman (PP Spin)"]
]

headers_strat = ["Auction Tier", "Recommended Targets & Rationale"]
for c_idx, h in enumerate(headers_strat):
    cell = t_strat.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = C_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_NAME
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

for r_idx, row in enumerate(strat_rows):
    for c_idx, val in enumerate(row):
        cell = t_strat.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 0 else C_LIGHT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_NAME
        p.font.size = Pt(9)
        p.font.color.rgb = C_PINK if c_idx == 0 else C_DARK
        p.font.bold = (c_idx == 0)


# ==========================================
# SLIDE 15: CONCLUSION & CHECKLIST
# ==========================================
slide15 = prs.slides.add_slide(blank_layout)
add_header(slide15, "14. Conclusion & Unstop Submission Checklist")
add_footer(slide15, 15)

tx_s15 = slide15.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12.133), Inches(5.5))
tf_s15 = tx_s15.text_frame
tf_s15.word_wrap = True

p_c = tf_s15.paragraphs[0]
p_c.text = "Pre-Submission Verification Checklist for Prokash Ghosh"
p_c.font.name = FONT_NAME
p_c.font.size = Pt(14)
p_c.font.bold = True
p_c.font.color.rgb = C_PINK
p_c.space_after = Pt(10)

def add_check_item(tf, item_num, title, detail):
    p = tf.add_paragraph()
    p.space_after = Pt(8)
    r1 = p.add_run()
    r1.text = f"[✓] {item_num}. {title}: "
    r1.font.name = FONT_NAME
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r1.font.color.rgb = C_NAVY

    r2 = p.add_run()
    r2.text = detail
    r2.font.name = FONT_NAME
    r2.font.size = Pt(10)
    r2.font.color.rgb = C_DARK

add_check_item(tf_s15, "01", "Top 10 Batters Dropdown", "Select in exact rank order: 1. Naman Dhir, 2. Shashank Singh, 3. Tim David, 4. Suryakumar Yadav, 5. Rishabh Pant, 6. Andre Russell, 7. Jos Buttler, 8. David Miller, 9. Heinrich Klaasen, 10. Rinku Singh.")
add_check_item(tf_s15, "02", "Top 10 Bowlers Dropdown", "Select in exact rank order: 1. Sunil Narine, 2. Hasan Mahmud, 3. Mitchell Santner, 4. Rashid Khan, 5. Jasprit Bumrah, 6. Varun Chakravarthy, 7. Mujeeb Ur Rahman, 8. Mahedi Hasan, 9. Jamie Overton, 10. Sikandar Raza.")
add_check_item(tf_s15, "03", "Methodology Report PDF", "Upload 'SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pdf' under Round 1 Methodology Report.")
add_check_item(tf_s15, "04", "Presentation Deck", "PowerPoint deck 'SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx' generated for executive franchise pitch.")
add_check_item(tf_s15, "05", "Reproducibility", "Supporting analysis scripts, rankings CSVs, and Jupyter Notebook persisted in workspace.")

# Sign-off box
p_sign = tf_s15.add_paragraph()
p_sign.space_before = Pt(16)
r_s = p_sign.add_run()
r_s.text = "Candidate: Prokash Ghosh  |  Role: Cricket Analytics & Scouting  |  Status: Official Submission Ready"
r_s.font.name = FONT_NAME
r_s.font.size = Pt(11)
r_s.font.bold = True
r_s.font.color.rgb = C_PINK

ppt_path = "d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx"
prs.save(ppt_path)
print(f"POWERPOINT PRESENTATION SAVED SUCCESSFULLY AT: {ppt_path}")

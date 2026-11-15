import re

with open('d:/Download/RR Auction/scripts/19_build_presentation_expanded.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update add_three_profile_cards for Slides 8 & 9
old_profile_func = """def add_three_profile_cards(slide, cards_info):
    for idx, (rank, name, role, bpri, stats, strength, risk, rr_fit, col) in enumerate(cards_info):
        left = Inches(0.6 + idx * 4.12)
        top = Inches(1.15)
        width = Inches(3.90)
        height = Inches(5.70)
        
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_WHITE
        card.line.color.rgb = C_BORDER
        
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.95))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = col
        header_box.line.color.rgb = col
        
        tx_h = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.08), width - Inches(0.3), Inches(0.80))
        tf_h = tx_h.text_frame
        tf_h.word_wrap = True
        
        p_rk = tf_h.paragraphs[0]
        p_rk.text = f"RANK {rank} | {name.upper()}"
        p_rk.font.name = FONT_NAME
        p_rk.font.size = Pt(15)
        p_rk.font.bold = True
        p_rk.font.color.rgb = C_WHITE
        
        p_role = tf_h.add_paragraph()
        p_role.text = role
        p_role.font.name = FONT_NAME
        p_role.font.size = Pt(10.5)
        p_role.font.italic = True
        p_role.font.color.rgb = C_GOLD
        
        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(1.05), width - Inches(0.4), height - Inches(1.15))
        tf = tx.text_frame
        tf.word_wrap = True
        
        p_score = tf.paragraphs[0]
        p_score.text = f"Reliability Score: {bpri}"
        p_score.font.name = FONT_NAME
        p_score.font.size = Pt(13)
        p_score.font.bold = True
        p_score.font.color.rgb = col
        p_score.space_after = Pt(6)
        
        p_stats = tf.add_paragraph()
        p_stats.text = f"Key Pressure Stats:\\n{stats}"
        p_stats.font.name = FONT_NAME
        p_stats.font.size = Pt(10.5)
        p_stats.font.color.rgb = C_DARK
        p_stats.space_after = Pt(6)
        
        p_str = tf.add_paragraph()
        p_str.text = f"Analytical Strength:\\n{strength}"
        p_str.font.name = FONT_NAME
        p_str.font.size = Pt(10.5)
        p_str.font.color.rgb = C_DARK
        p_str.space_after = Pt(6)
        
        p_risk = tf.add_paragraph()
        p_risk.text = f"Limitation / Risk:\\n{risk}"
        p_risk.font.name = FONT_NAME
        p_risk.font.size = Pt(10.5)
        p_risk.font.color.rgb = C_DARK
        p_risk.space_after = Pt(6)
        
        p_fit = tf.add_paragraph()
        p_fit.text = f"RR Tactical Fit (IPL 2027):\\n{rr_fit}"
        p_fit.font.name = FONT_NAME
        p_fit.font.size = Pt(11)
        p_fit.font.bold = True
        p_fit.font.color.rgb = C_PINK_DARK"""

new_profile_func = """def add_three_profile_cards(slide, cards_info):
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
        r1.text = "Key Pressure Metrics:\\n"
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
        r3.text = "Analytical Strength:\\n"
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
        r5.text = "Limitation / Risk:\\n"
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
        r7.text = "RR Tactical Fit (IPL 2027):\\n"
        r7.font.bold = True
        r7.font.size = Pt(13)
        r7.font.color.rgb = C_PINK_DARK
        r8 = p_fit.add_run()
        r8.text = rr_fit
        r8.font.size = Pt(12)
        r8.font.bold = True
        r8.font.color.rgb = C_DARK"""

code = code.replace(old_profile_func, new_profile_func)

# 2. Update Slide 10 (Bowlers 1 to 4)
old_s10_loop = """for idx, (rank, name, role, bopri, stats, strength, risk, rr_fit, col) in enumerate(bowlers_1_4):
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
    
    tx = slide10.shapes.add_textbox(left + Inches(0.25), top + Inches(0.12), width - Inches(0.35), height - Inches(0.2))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_t = tf.paragraphs[0]
    p_t.text = f"RANK {rank} | {name.upper()} ({bopri})"
    p_t.font.name = FONT_NAME
    p_t.font.size = Pt(13.5)
    p_t.font.bold = True
    p_t.font.color.rgb = col
    p_t.space_after = Pt(2)
    
    p_r = tf.add_paragraph()
    p_r.text = f"{role} | {stats}"
    p_r.font.name = FONT_NAME
    p_r.font.size = Pt(10)
    p_r.font.bold = True
    p_r.font.color.rgb = C_DARK
    p_r.space_after = Pt(3)
    
    p_s = tf.add_paragraph()
    p_s.text = f"Strength: {strength}"
    p_s.font.name = FONT_NAME
    p_s.font.size = Pt(10)
    p_s.font.color.rgb = C_DARK
    p_s.space_after = Pt(2)
    
    p_f = tf.add_paragraph()
    p_f.text = f"RR Fit: {rr_fit}"
    p_f.font.name = FONT_NAME
    p_f.font.size = Pt(10.5)
    p_f.font.bold = True
    p_f.font.color.rgb = C_PINK_DARK"""

new_s10_loop = """for idx, (rank, name, role, bopri, stats, strength, risk, rr_fit, col) in enumerate(bowlers_1_4):
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
    p_r.text = f"{role}\\nKey Metrics: {stats}"
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
    p_f.font.color.rgb = C_PINK_DARK"""

code = code.replace(old_s10_loop, new_s10_loop)

# 3. Update Slide 11 (Bowlers 5, 6, 9 + Pathirana)
old_s11_loop = """for idx, (rank, name, role, bopri, stats, strength, risk, rr_fit, col) in enumerate(bowlers_5_6_9):
    left = Inches(0.6 + idx * 4.12)
    top = Inches(1.15)
    width = Inches(3.90)
    height = Inches(4.30)
    
    card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_BORDER
    
    header_box = slide11.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.85))
    header_box.fill.solid()
    header_box.fill.fore_color.rgb = col
    header_box.line.color.rgb = col
    
    tx_h = slide11.shapes.add_textbox(left + Inches(0.15), top + Inches(0.06), width - Inches(0.3), Inches(0.75))
    tf_h = tx_h.text_frame
    tf_h.word_wrap = True
    
    p_rk = tf_h.paragraphs[0]
    p_rk.text = f"RANK {rank} | {name.upper()}"
    p_rk.font.name = FONT_NAME
    p_rk.font.size = Pt(14)
    p_rk.font.bold = True
    p_rk.font.color.rgb = C_WHITE
    
    p_role = tf_h.add_paragraph()
    p_role.text = role
    p_role.font.name = FONT_NAME
    p_role.font.size = Pt(10)
    p_role.font.italic = True
    p_role.font.color.rgb = C_GOLD
    
    tx = slide11.shapes.add_textbox(left + Inches(0.18), top + Inches(0.95), width - Inches(0.36), height - Inches(1.05))
    tf = tx.text_frame
    tf.word_wrap = True
    
    p_score = tf.paragraphs[0]
    p_score.text = bopri
    p_score.font.name = FONT_NAME
    p_score.font.size = Pt(12)
    p_score.font.bold = True
    p_score.font.color.rgb = col
    p_score.space_after = Pt(4)
    
    p_stats = tf.add_paragraph()
    p_stats.text = f"Pressure Stats:\\n{stats}"
    p_stats.font.name = FONT_NAME
    p_stats.font.size = Pt(10)
    p_stats.font.color.rgb = C_DARK
    p_stats.space_after = Pt(4)
    
    p_str = tf.add_paragraph()
    p_str.text = f"Strength: {strength}"
    p_str.font.name = FONT_NAME
    p_str.font.size = Pt(10)
    p_str.font.color.rgb = C_DARK
    p_str.space_after = Pt(4)
    
    p_fit = tf.add_paragraph()
    p_fit.text = f"RR Fit: {rr_fit}"
    p_fit.font.name = FONT_NAME
    p_fit.font.size = Pt(10.5)
    p_fit.font.bold = True
    p_fit.font.color.rgb = C_PINK_DARK

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
p_b_t.font.size = Pt(12)
p_b_t.font.bold = True
p_b_t.font.color.rgb = C_PINK_DARK
p_b_t.space_after = Pt(2)

p_b_d = tf_s11_b.add_paragraph()
p_b_d.text = (
    "• 596 pressure balls | 50 wickets | 11.9 strike rate | 81.0% consistency. Extreme slinging angle makes 148kph yorkers unplayable.\\n"
    "• While early-spell wides slightly inflate his economy (8.95), his pure strike weapon rating is elite. Primary overseas fast-bowler target for RR.\\n"
    "• Honorable Mentions: Mujeeb Ur Rahman (Rank 7, 6.95 Econ), Mahedi Hasan (Rank 8, 6.83 Econ), Sikandar Raza (Rank 10, 6.76 Econ)."
)
p_b_d.font.name = FONT_NAME
p_b_d.font.size = Pt(10.5)
p_b_d.font.color.rgb = C_DARK"""

new_s11_loop = """for idx, (rank, name, role, bopri, stats, strength, risk, rr_fit, col) in enumerate(bowlers_5_6_9):
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
    r1.text = "Pressure Stats:\\n"
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
    r3.text = "Key Analytical Strength:\\n"
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
    r5.text = "RR Tactical Fit:\\n"
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
    "• 596 pressure balls | 50 wickets | 11.9 strike rate | 81.0% consistency. Extreme slinging angle makes 148kph yorkers unplayable.\\n"
    "• While early-spell wides slightly inflate his economy (8.95), his pure strike weapon rating is elite. Primary overseas fast-bowler target for RR.\\n"
    "• Honorable Mentions: Mujeeb Ur Rahman (Rank 7, 6.95 Econ), Mahedi Hasan (Rank 8, 6.83 Econ), Sikandar Raza (Rank 10, 6.76 Econ)."
)
p_b_d.font.name = FONT_NAME
p_b_d.font.size = Pt(11.5)
p_b_d.font.color.rgb = C_DARK"""

code = code.replace(old_s11_loop, new_s11_loop)

with open('d:/Download/RR Auction/scripts/19_build_presentation_expanded.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated Slides 8, 9, 10, 11 font sizes successfully!")

with open('d:/Download/RR Auction/scripts/20_build_pdf_report_expanded.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Page 12 addition
old_p12 = '''    story.append(Spacer(1, 6))

    chart4_path = "figures/chart4_bowling_quadrant.png"
    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=523, height=215))
    story.append(Paragraph(
        "<i>Figure 3: Bowling Clutch Quadrant. Right side represents run savers (positive runs saved vs over par); top area represents "
        "lethal wicket-takers (inverted strike rate: lower balls per wicket is higher). Top-right features Narine, Hasan Mahmud, and Santner.</i>",
        ParagraphStyle('Cap3', fontName='Times-Italic', fontSize=8, leading=10.5, textColor=c_grey)
    ))
    story.append(PageBreak())'''

new_p12 = '''    story.append(Spacer(1, 4))

    chart4_path = "figures/chart4_bowling_quadrant.png"
    if os.path.exists(chart4_path):
        story.append(Image(chart4_path, width=523, height=215))
    story.append(Paragraph(
        "<i>Figure 3: Bowling Clutch Quadrant. Right side represents run savers (positive runs saved vs over par); top area represents "
        "lethal wicket-takers (inverted strike rate: lower balls per wicket is higher). Top-right features Narine, Hasan Mahmud, and Santner.</i>",
        ParagraphStyle('Cap3', fontName='Times-Italic', fontSize=8, leading=10.5, textColor=c_grey)
    ))
    story.append(Spacer(1, 5))

    quad_summary = [
        [Paragraph("<b>QUADRANT ANALYTICAL SYNTHESIS & STRATEGIC DISCOVERY:</b><br/>"
                   "• <b>The Clutch Outliers (Top-Right):</b> Both charts clearly separate the true match-winners from the chasing pack. Naman Dhir (+48.6 SR) and Shashank Singh (+58.9 SR) form the elite batting cluster, while Sunil Narine (+2.52 Runs Saved) and Hasan Mahmud (11.9 SR) lead the bowling matrix.<br/>"
                   "• <b>The Frontrunner Penalty:</b> Players located in the bottom-left quadrant exhibit high raw statistics in low-leverage phases but regress significantly under pressure; our framework systematically filters these players out of RR's primary shortlist.", card_body)]
    ]
    t_quad = Table(quad_summary, colWidths=[523])
    t_quad.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FC')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('LINELEFT', (0,0), (0,-1), 4, c_navy),
        ('PADDING', (0,0), (-1,-1), 7)
    ]))
    story.append(t_quad)
    story.append(PageBreak())'''

code = code.replace(old_p12, new_p12)

# Page 15 addition
old_p15_refs = '''    story.append(Paragraph(p_sources, body_style))
    story.append(Spacer(1, 6))'''

new_p15_refs = '''    story.append(Paragraph(p_sources, body_style))
    story.append(Spacer(1, 6))

    summary_mandate = [
        [Paragraph("<b>FINAL STRATEGIC TAKEAWAY FOR RAJASTHAN ROYALS AUCTION TABLE:</b><br/>"
                   "1. <b>Prioritize Phase Par Normalization:</b> Raw statistics are misleading; value must be judged against phase-specific historical par.<br/>"
                   "2. <b>Exploit Domestic Valuation Gaps:</b> Secure Naman Dhir and Shashank Singh before rival franchises recognize their +50 SR clutch deltas.<br/>"
                   "3. <b>Build a Fortress at Sawai Mansingh:</b> Pair Mitchell Santner's restrictive spin (6.92 Econ) with Hasan Mahmud's reverse yorkers (11.9 SR) to control death overs in Jaipur.", card_body)]
    ]
    t_mandate = Table(summary_mandate, colWidths=[523])
    t_mandate.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FC')),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('LINELEFT', (0,0), (0,-1), 4, c_pink_dark),
        ('PADDING', (0,0), (-1,-1), 7)
    ]))
    story.append(t_mandate)
    story.append(Spacer(1, 6))'''

code = code.replace(old_p15_refs, new_p15_refs)

with open('d:/Download/RR Auction/scripts/20_build_pdf_report_expanded.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated Page 12 and Page 15 cleanly via python!')

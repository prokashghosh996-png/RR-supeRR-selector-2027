import pptx

prs = pptx.Presentation('d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx')

# Check Slide 14 Table Runs
slide14 = prs.slides[13]
print("=== SLIDE 14 TABLE RUN CHECK ===")
for s in slide14.shapes:
    if s.has_table:
        for r_i, row in enumerate(s.table.rows):
            for c_i, cell in enumerate(row.cells):
                for p_i, p in enumerate(cell.text_frame.paragraphs):
                    for run_i, run in enumerate(p.runs):
                        print(f"R{r_i} C{c_i} P{p_i} Run{run_i}: size={run.font.size.pt if run.font.size else None} font={run.font.name} bold={run.font.bold} text=\"{run.text}\"")

# Check Slide 8 & 9 Card Text Bottoms
for s_idx in [7, 8]:
    slide = prs.slides[s_idx]
    print(f"\n=== SLIDE {s_idx+1} TEXTBOX POSITIONS ===")
    for s_i, shape in enumerate(slide.shapes):
        t = shape.top.inches
        h = shape.height.inches
        b = t + h
        if shape.has_text_frame:
            first_words = shape.text_frame.text[:30].replace('\n', ' ')
            print(f"Shape {s_i} ({shape.name}): top={t:.2f}\" height={h:.2f}\" bottom={b:.2f}\" | text=\"{first_words}\"")

# Check Slide 11 Card Positions
slide11 = prs.slides[10]
print("\n=== SLIDE 11 POSITIONS ===")
for s_i, shape in enumerate(slide11.shapes):
    t = shape.top.inches
    h = shape.height.inches
    b = t + h
    if shape.has_text_frame:
        first_words = shape.text_frame.text[:30].replace('\n', ' ')
        print(f"Shape {s_i} ({shape.name}): top={t:.2f}\" height={h:.2f}\" bottom={b:.2f}\" | text=\"{first_words}\"")

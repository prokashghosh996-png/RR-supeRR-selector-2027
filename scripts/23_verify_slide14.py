import pptx

prs = pptx.Presentation('d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx')
slide = prs.slides[13] # slide 14 (0-indexed 13)
for shape in slide.shapes:
    if shape.has_table:
        tbl = shape.table
        print('Found table on Slide 14:', len(tbl.rows), 'rows,', len(tbl.columns), 'cols')
        for r_idx, row in enumerate(tbl.rows):
            for c_idx, cell in enumerate(row.cells):
                for p_idx, p in enumerate(cell.text_frame.paragraphs):
                    size = p.font.size.pt if p.font.size else 'None'
                    print(f'R{r_idx} C{c_idx} P{p_idx}: size={size} bold={p.font.bold} font={p.font.name} text="{p.text}"')

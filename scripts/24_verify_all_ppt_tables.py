import pptx

prs = pptx.Presentation('d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx')
for s_idx, slide in enumerate(prs.slides, 1):
    for shape in slide.shapes:
        if shape.has_table:
            tbl = shape.table
            mismatches = []
            for r_idx, row in enumerate(tbl.rows):
                for c_idx, cell in enumerate(row.cells):
                    sizes = set()
                    for p in cell.text_frame.paragraphs:
                        s = p.font.size.pt if p.font.size else None
                        sizes.add(s)
                    if len(sizes) > 1 or None in sizes:
                        mismatches.append((r_idx, c_idx, sizes))
            if mismatches:
                print(f'Slide {s_idx} table has mismatched/None font sizes: {mismatches}')
            else:
                print(f'Slide {s_idx} table is clean! All paragraphs have consistent explicit font sizes.')

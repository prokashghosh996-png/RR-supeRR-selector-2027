import pptx

prs = pptx.Presentation('d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pptx')
for slide_idx in [7, 8, 9, 10]: # Slides 8, 9, 10, 11 (0-indexed)
    slide = prs.slides[slide_idx]
    print(f'=== SLIDE {slide_idx+1} ===')
    for shape_idx, shape in enumerate(slide.shapes):
        if shape.has_text_frame:
            tf = shape.text_frame
            for p_idx, p in enumerate(tf.paragraphs):
                size = p.font.size.pt if p.font.size else (p.runs[0].font.size.pt if p.runs and p.runs[0].font.size else 'None')
                text_snippet = p.text[:40].replace('\n', ' ')
                if text_snippet:
                    print(f'  Shape {shape_idx} P{p_idx}: size={size} | text="{text_snippet}"')

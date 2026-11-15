import pymupdf

doc = pymupdf.open("d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pdf")
print(f"Total pages: {len(doc)}")

for i, page in enumerate(doc):
    text = page.get_text().strip()
    first_line = text.split('\n')[0] if text else "EMPTY"
    last_line = text.split('\n')[-1] if text else "EMPTY"
    word_count = len(text.split())
    print(f"Page {i+1:02d}: Words={word_count:4d} | Start: '{first_line[:40]}' | End: '{last_line[:40]}'")

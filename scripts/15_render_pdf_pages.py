import os
import pymupdf

pdf_path = "d:/Download/RR Auction/SupeRR_Selector_Season_2_RR_IPL_2027_Auction_Strategy.pdf"
out_dir = "d:/Download/RR Auction/pdf_pages"
os.makedirs(out_dir, exist_ok=True)

doc = pymupdf.open(pdf_path)
print(f"Total pages in PDF: {len(doc)}")

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=150)
    page_img_path = os.path.join(out_dir, f"page_{i+1:02d}.png")
    pix.save(page_img_path)
    print(f"Rendered Page {i+1} -> {page_img_path} ({pix.width}x{pix.height})")

print("All pages rendered successfully.")

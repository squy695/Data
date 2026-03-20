import fitz  # PyMuPDF

# Open the source PDF
doc = fitz.open("fig 3a uncut.pdf")

# Define crop margins as percentages of total height
top_margin = 0.15
bottom_margin = 0.12

for page in doc:
    rect = page.rect
    
    # Calculate new crop boundaries
    # x0, y0 (top-left) to x1, y1 (bottom-right)
    new_rect = fitz.Rect(
        rect.x0, 
        rect.y0 + rect.height * top_margin, 
        rect.x1, 
        rect.y1 - rect.height * bottom_margin
    )
    
    # Apply the crop box to the page
    page.set_cropbox(new_rect)

# Save the processed document
doc.save("fig_3_a.pdf")
doc.close()
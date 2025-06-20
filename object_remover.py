import fitz  # PyMuPDF
import io
import os
from PIL import Image

# === Step 1 & 2: Extract embedded images and reconstruct clean PDF ===
input_pdf = "document.pdf"
reconstructed_pdf = "reconstructed.pdf"
doc = fitz.open(input_pdf)
embedded_images = []

for page_index, page in enumerate(doc):
    images_in_page = page.get_images(full=True)
    for img_index, img in enumerate(images_in_page):
        xref = img[0]
        image_data = doc.extract_image(xref)
        image_bytes = image_data["image"]
        image_ext = image_data["ext"]
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        embedded_images.append((page_index, image))

# Sort images by page index and export to new PDF
if embedded_images:
    embedded_images.sort(key=lambda x: x[0])
    image_pages = [img for _, img in embedded_images]
    image_pages[0].save(reconstructed_pdf, save_all=True, append_images=image_pages[1:])
    print(f"Clean PDF rebuilt without vector objects: {reconstructed_pdf}")
else:
    print("No embedded images found to reconstruct the PDF.")

# === Step 3: Detect and neutralize vector shapes (e.g., overlaid boxes) ===
vector_output_dir = "vector_sanitized"
os.makedirs(vector_output_dir, exist_ok=True)
vector_cleaned_pdf = os.path.join(vector_output_dir, "document.pdf")

# Reopen original document to apply vector filtering
doc = fitz.open(input_pdf)

for page in doc:
    vector_shapes = page.get_drawings()
    for shape_obj in vector_shapes:
        fill_color = shape_obj.get("fill")
        if fill_color == (1, 1, 1):  # change the color if you want
            rect = shape_obj.get("rect")
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(fill=None, color=None)  # Transparent overlay
            shape.commit()

doc.save(vector_cleaned_pdf)
doc.close()

print(f"PDF with vector overlays neutralized saved as: {vector_cleaned_pdf}")


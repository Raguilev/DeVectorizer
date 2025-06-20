import os
import fitz  # PyMuPDF
import io
from PIL import Image

def devectorize_pdf(file_paths):
    output_dir = "devectorized"
    os.makedirs(output_dir, exist_ok=True)

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_clean.pdf")

        doc = fitz.open(file_path)
        image_pages = []

        for page in doc:
            images = page.get_images(full=True)
            for img in images:
                xref = img[0]
                img_data = doc.extract_image(xref)
                image = Image.open(io.BytesIO(img_data["image"])).convert("RGB")
                image_pages.append(image)

        if image_pages:
            image_pages[0].save(output_path, save_all=True, append_images=image_pages[1:])

        doc.close()
import os
import fitz  # PyMuPDF

def mark_vectors_in_pdf(file_paths):
    output_dir = os.path.join("results", "marked")
    os.makedirs(output_dir, exist_ok=True)

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(output_dir, f"{name}_marked.pdf")

        doc = fitz.open(file_path)
        for page in doc:
            drawings = page.get_drawings()
            for d in drawings:
                if d.get("fill") == (1, 1, 1):
                    rect = d.get("rect")
                    shape = page.new_shape()
                    shape.draw_rect(rect)
                    shape.finish(color=(1, 0, 0), width=1)
                    shape.commit()
        doc.save(output_path)
        doc.close()
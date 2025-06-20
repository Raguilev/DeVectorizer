import sys
import os
import fitz  # PyMuPDF
import io
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PIL import Image

class DeVectorizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeVectorizer PDF Tool")
        self.resize(500, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel("Drop PDF files here or use the button to browse.")
        self.label.setAlignment(Qt.AlignCenter)
        self.list_widget = QListWidget()
        self.select_button = QPushButton("Select PDF Files")
        self.mark_button = QPushButton("Mark Vectors")
        self.clean_button = QPushButton("Devectorize PDF")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.mark_button)
        self.layout.addWidget(self.clean_button)
        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.open_file_dialog)
        self.mark_button.clicked.connect(self.mark_vectors)
        self.clean_button.clicked.connect(self.devectorize)

        self.setAcceptDrops(True)

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        for file in files:
            self.add_file(file)

    def add_file(self, file_path):
        if file_path.lower().endswith('.pdf') and file_path not in [self.list_widget.item(i).text() for i in range(self.list_widget.count())]:
            self.list_widget.addItem(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            self.add_file(url.toLocalFile())

    def mark_vectors(self):
        output_dir = "marked"
        os.makedirs(output_dir, exist_ok=True)

        for i in range(self.list_widget.count()):
            file_path = self.list_widget.item(i).text()
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
                        shape.finish(color=(1, 0, 0), width=1)  # red border
                        shape.commit()
            doc.save(output_path)
            doc.close()

        QMessageBox.information(self, "Done", f"Marked PDFs saved in '{output_dir}'")

    def devectorize(self):
        output_dir = "devectorized"
        os.makedirs(output_dir, exist_ok=True)

        for i in range(self.list_widget.count()):
            file_path = self.list_widget.item(i).text()
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

        QMessageBox.information(self, "Done", f"Clean PDFs saved in '{output_dir}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeVectorizerApp()
    window.show()
    sys.exit(app.exec_())
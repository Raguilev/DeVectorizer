import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from functions.file_handler import add_file, get_selected_files
from functions.mark_vectors import mark_vectors_in_pdf
from functions.devectorize import devectorize_pdf

class MainWindow(QWidget):
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
        self.mark_button.clicked.connect(self.handle_mark_vectors)
        self.clean_button.clicked.connect(self.handle_devectorize)

        self.setAcceptDrops(True)

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        for file in files:
            add_file(self.list_widget, file)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            add_file(self.list_widget, url.toLocalFile())

    def handle_mark_vectors(self):
        files = get_selected_files(self.list_widget)
        if not files:
            QMessageBox.warning(self, "Warning", "No PDF files selected.")
            return
        mark_vectors_in_pdf(files)
        QMessageBox.information(self, "Done", "Marked PDFs saved in 'marked/' folder.")

    def handle_devectorize(self):
        files = get_selected_files(self.list_widget)
        if not files:
            QMessageBox.warning(self, "Warning", "No PDF files selected.")
            return
        devectorize_pdf(files)
        QMessageBox.information(self, "Done", "Clean PDFs saved in 'devectorized/' folder.")
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt
from functions.file_handler import add_file, get_selected_files, get_full_paths
from functions.mark_vectors import mark_vectors_in_pdf
from functions.devectorize import devectorize_pdf

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeVectorizer PDF Tool")
        self.resize(600, 450)

        self.layout = QVBoxLayout()
        self.label = QLabel("Drop PDF files here or use the button to browse.")
        self.label.setAlignment(Qt.AlignCenter)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.remove_selected_items)

        # Buttons in horizontal layout
        self.button_layout = QHBoxLayout()
        self.select_button = QPushButton("Select PDFs")
        self.mark_button = QPushButton("Mark Vectors")
        self.clean_button = QPushButton("Devectorize")
        self.button_layout.addWidget(self.select_button)
        self.button_layout.addWidget(self.mark_button)
        self.button_layout.addWidget(self.clean_button)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(self.button_layout)
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

    def remove_selected_items(self, _):
        for item in self.list_widget.selectedItems():
            self.list_widget.takeItem(self.list_widget.row(item))

    def handle_mark_vectors(self):
        files = get_full_paths(self.list_widget)
        if not files:
            QMessageBox.warning(self, "Warning", "No PDF files selected.")
            return
        QMessageBox.information(self, "Processing", "Marking vectors in selected files...")
        mark_vectors_in_pdf(files)
        QMessageBox.information(self, "Completed", "Marked PDFs saved in 'marked/' folder.")

    def handle_devectorize(self):
        files = get_full_paths(self.list_widget)
        if not files:
            QMessageBox.warning(self, "Warning", "No PDF files selected.")
            return
        QMessageBox.information(self, "Processing", "Devectorizing selected files...")
        devectorize_pdf(files)
        QMessageBox.information(self, "Completed", "Clean PDFs saved in 'devectorized/' folder.")
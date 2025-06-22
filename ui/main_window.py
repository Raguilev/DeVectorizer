import os
import webbrowser
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QMessageBox, QHBoxLayout, QListWidgetItem
)
from PyQt5.QtCore import Qt
from functions.file_handler import add_file, get_selected_files, clear_files
from functions.mark_vectors import mark_vectors_in_pdf
from functions.devectorize import devectorize_pdf

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeVectorizer PDF Tool")
        self.resize(600, 500)

        self.layout = QVBoxLayout()

        self.title = QLabel("<b> DeVectorizer PDF Tool</b>")
        self.title.setAlignment(Qt.AlignCenter)
        self.subtitle = QLabel("Drop PDF files here or use the button to browse.")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.list_widget = QListWidget()

        # Botones de la parte inferior
        self.bottom_layout = QHBoxLayout()

        self.mark_button = QPushButton("Mark Vectors")
        self.clean_button = QPushButton("Devectorize")

        self.add_button = QPushButton("➕")
        self.folder_button = QPushButton("📁")
        self.clear_button = QPushButton("❌")

        self.add_button.setFixedWidth(40)
        self.folder_button.setFixedWidth(40)
        self.clear_button.setFixedWidth(40)

        # Contenedor para los botones de acción
        self.bottom_layout.addWidget(self.mark_button)
        self.bottom_layout.addWidget(self.clean_button)
        self.bottom_layout.addStretch()
        self.bottom_layout.addWidget(self.add_button)
        self.bottom_layout.addWidget(self.folder_button)
        self.bottom_layout.addWidget(self.clear_button)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(self.bottom_layout)

        self.setLayout(self.layout)

        self.add_button.clicked.connect(self.open_file_dialog)
        self.folder_button.clicked.connect(self.open_results_folder)
        self.clear_button.clicked.connect(self.clear_file_list)
        self.mark_button.clicked.connect(self.handle_mark_vectors)
        self.clean_button.clicked.connect(self.handle_devectorize)

        self.setAcceptDrops(True)

    def open_file_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select PDF files", "", "PDF Files (*.pdf)")
        for file in files:
            add_file(self.list_widget, file)

    def open_results_folder(self):
        os.makedirs("results", exist_ok=True)
        webbrowser.open(os.path.abspath("results"))

    def clear_file_list(self):
        clear_files(self.list_widget)

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
        self.subtitle.setText("Processing request...")
        mark_vectors_in_pdf(files)
        self.subtitle.setText("Drop PDF files here or use the button to browse.")
        QMessageBox.information(self, "Done", "Marked PDFs saved in 'results/marked/' folder.")

    def handle_devectorize(self):
        files = get_selected_files(self.list_widget)
        if not files:
            QMessageBox.warning(self, "Warning", "No PDF files selected.")
            return
        self.subtitle.setText("Processing request...")
        devectorize_pdf(files)
        self.subtitle.setText("Drop PDF files here or use the button to browse.")
        QMessageBox.information(self, "Done", "Clean PDFs saved in 'results/devectorized/' folder.")
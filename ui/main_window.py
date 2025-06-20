import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
from functions.file_handler import add_file, get_selected_files
from functions.mark_vectors import mark_vectors_in_pdf
from functions.devectorize import devectorize_pdf

class WorkerSignals(QObject):
    finished = pyqtSignal(str)

class Worker(QRunnable):
    def __init__(self, func, files, callback):
        super().__init__()
        self.func = func
        self.files = files
        self.signals = WorkerSignals()
        self.signals.finished.connect(callback)

    @pyqtSlot()
    def run(self):
        self.func(self.files)
        self.signals.finished.emit("done")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ DeVectorizer PDF Tool")
        self.resize(520, 500)

        self.layout = QVBoxLayout()

        self.title = QLabel("<h2>✨ DeVectorizer PDF Tool</h2>")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        self.info = QLabel("Drop PDF files here or use the button to browse.")
        self.info.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info)

        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.remove_item)
        self.layout.addWidget(self.list_widget)

        button_layout = QHBoxLayout()
        self.select_button = QPushButton("Select PDFs")
        self.mark_button = QPushButton("Mark Vectors")
        self.clean_button = QPushButton("Devectorize")

        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.mark_button)
        button_layout.addWidget(self.clean_button)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

        self.select_button.clicked.connect(self.open_file_dialog)
        self.mark_button.clicked.connect(self.handle_mark_vectors)
        self.clean_button.clicked.connect(self.handle_devectorize)

        self.setAcceptDrops(True)
        self.threadpool = QThreadPool()

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

    def remove_item(self, pos):
        item = self.list_widget.itemAt(pos)
        if item:
            self.list_widget.takeItem(self.list_widget.row(item))

    def handle_mark_vectors(self):
        self.start_process(mark_vectors_in_pdf)

    def handle_devectorize(self):
        self.start_process(devectorize_pdf)

    def start_process(self, function):
        files = get_selected_files(self.list_widget)
        if not files:
            QMessageBox.warning(self, "Warning", "No PDF files selected.")
            return

        self.info.setText("Processing request...")
        worker = Worker(function, files, self.finish_process)
        self.threadpool.start(worker)

    def finish_process(self):
        self.info.setText("Drop PDF files here or use the button to browse.")
        QMessageBox.information(self, "Done", "Process completed successfully.")
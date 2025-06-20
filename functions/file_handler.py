from PyQt5.QtWidgets import QListWidget
import os

def add_file(list_widget: QListWidget, file_path: str):
    if file_path.lower().endswith(".pdf"):
        existing_files = [list_widget.item(i).text() for i in range(list_widget.count())]
        if file_path not in existing_files:
            list_widget.addItem(file_path)

def get_selected_files(list_widget: QListWidget):
    return [list_widget.item(i).text() for i in range(list_widget.count())]
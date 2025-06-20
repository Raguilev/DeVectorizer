from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt

import os

def add_file(list_widget: QListWidget, file_path: str):
    if file_path.lower().endswith(".pdf"):
        existing_files = [item.data(256) for item in list_widget.findItems("*", Qt.MatchWildcard)]
        if file_path not in existing_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(256, file_path)  # store full path internally
            list_widget.addItem(item)

def get_selected_files(list_widget: QListWidget):
    return [item.data(256) for item in list_widget.selectedItems()]

def get_full_paths(list_widget: QListWidget):
    return [list_widget.item(i).data(256) for i in range(list_widget.count())]
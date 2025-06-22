from PyQt5.QtWidgets import QListWidget, QListWidgetItem
import os

def add_file(list_widget: QListWidget, file_path: str):
    if file_path.lower().endswith(".pdf"):
        filenames = [list_widget.item(i).data(0) for i in range(list_widget.count())]
        if file_path not in filenames:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(0, file_path)
            list_widget.addItem(item)

def get_selected_files(list_widget: QListWidget):
    return [list_widget.item(i).data(0) for i in range(list_widget.count())]

def clear_files(list_widget: QListWidget):
    list_widget.clear()
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QCheckBox, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from pathlib import Path
from PyQt5 import uic
from PIL import Image

moduleDir = os.path.dirname(sys.modules[__name__].__file__)

class AppDemo(QMainWindow):
    def __init__(self, parent=None):
        super(AppDemo, self).__init__(parent)
        uiFile = '%s\\ui.ui' %moduleDir
        self.main_ui = uic.loadUi(uiFile, QWidget())

        self.listbox_view = ListBoxWidget(self)
        self.main_ui.verticalLayout_3.addWidget(self.listbox_view)
        self.listbox_view.itemClicked.connect(self.on_item_clicked)

        self.setCentralWidget(self.main_ui)
        self.setWindowTitle('Image Size Checker')

        self.main_ui.ori_w_button.valueChanged.connect(self.calculation)
        self.main_ui.ori_h_button.valueChanged.connect(self.calculation)
        self.main_ui.num_spinbox.valueChanged.connect(self.calculation)
        self.main_ui.op_sign_button.clicked.connect(self.on_button_clicked)

    def on_item_clicked(self):
        filepath = self.listbox_view.currentItem().text()
        dims = get_image_dimensions(filepath)
        if dims:
            self.main_ui.ori_w_button.setValue(float(dims[0]))
            self.main_ui.ori_h_button.setValue(float(dims[1]))
            print(dims)
    
    def calculation(self):
        num = self.main_ui.num_spinbox.value()
        ori_w = self.main_ui.ori_w_button.value()
        ori_h = self.main_ui.ori_h_button.value()
        new_w = 1
        new_h = 1
        if self.main_ui.op_sign_button.text() == "x":
            new_w = ori_w * num
            new_h = ori_h * num
        else:
            new_w = ori_w / num
            new_h = ori_h / num
        self.main_ui.new_w_button.setValue(new_w)
        self.main_ui.new_h_button.setValue(new_h)
    
    def on_button_clicked(self):
        if self.main_ui.op_sign_button.text() == "x":
            self.main_ui.op_sign_button.setText("/")
        else:
            self.main_ui.op_sign_button.setText("x")
        self.calculation()

def get_image_dimensions(file_path, cal_num=1, calmode="x"):
    valid_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
    _, ext = os.path.splitext(file_path)
    if ext.lower() in valid_extensions:
        with Image.open(file_path) as img:
            width, height = img.size
            return [width, height]
    else:
        return
            # if cal_mode == "x": #perform multiply operation
            # if cal_mode == "/": #perform divide operation

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        # self.resize(600, 600)
    

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            super().dropEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())

import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui



class TaskCard(QtWidgets.QWidget):

    def __init__(self, title: str, desc:str = ""):
        super().__init__()
        self.card = QtWidgets.QWidget()


        self.title = QtWidgets.QLabel(title)
        self.desc = QtWidgets.QLabel(desc)

        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.delete_btn = QtWidgets.QPushButton("Delete")

        self.layout = QtWidgets.QVBoxLayout(self.card)
        self.layout.addWidget(self.title)
    
    def display_card(self):

        return self.card

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.title_input = QtWidgets.QLineEdit(placeholderText="Enter Title")
        self.desc_input = QtWidgets.QTextEdit(placeholderText="Enter a Description")

        self.main_layout =QtWidgets.QHBoxLayout(self)

        self.left_layout = QtWidgets.QVBoxLayout()
        self.left_layout.addWidget(self.title_input)
        self.left_layout.addWidget(self.desc_input)
        self.left_layout.addWidget(self.button)

        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.addWidget(TaskCard(title="hello").display_card())

        self.button.clicked.connect(self.magic)
        
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)


    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
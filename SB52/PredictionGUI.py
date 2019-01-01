from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
import sys
from PyQt5.QtGui import QPixmap
real_score = [
	('qt1', 'eagles'),
	('qt2', 'eagles'),
	('qt3', 'eagles'),
	('qt4', 'eagles'),
	]

range_of_quarters = [
	('qt1',('134','609')),
	('qt2', ('617', '1149')),
	('half_time', ('1150', '1381')),
	('qt3', ('1382', '1773')),
	('qt4', ('1778', '2460'))
	]


class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Adding Image To Label"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300


        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("sb52.jpg"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("sb52.jpg")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
        self.setLayout(vbox)
        self.show()
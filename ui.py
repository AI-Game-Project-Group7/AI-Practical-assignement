import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QFont
from main import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.points = 0
        self.setGeometry(500, 200, 600, 500)
        self.setWindowTitle("Game demonstration")
        self.startscreen()
        self.show()

    def startscreen(self):
        self.label = QLabel("Choose a starting number", self)
        self.label.setGeometry(150, 100, 350, 50)
        self.label.setFont(QFont('Arial', 20))
        numbers = generate_randoms()
        for i in range(len(numbers)):
            self.button = QPushButton(str(numbers[i]), self)
            self.button.setGeometry(30+110*i, 250, 100, 40)



app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())








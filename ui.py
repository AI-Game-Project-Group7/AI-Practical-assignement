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
        self.label.setGeometry(150, 50, 350, 50)
        self.label.setFont(QFont('Arial', 20))
        numbers = generate_randoms()
        for i in range(len(numbers)):
            self.button = QPushButton(str(numbers[i]), self)
            self.button.setGeometry(30+110*i, 150, 100, 40)
        self.startbutton = QPushButton("Start", self)
        self.startbutton.setGeometry(200, 300, 200, 80)
        self.startbutton.clicked.connect(self.on_startbutton_click)

    def on_startbutton_click(self):
        pass

    def game_cycle(self):
        pass
    def endscreen(self):
        pass




app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())








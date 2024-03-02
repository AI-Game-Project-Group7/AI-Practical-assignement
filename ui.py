import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QStackedWidget
from PyQt5.QtGui import QFont
from main import *

points = 0
bankpoints = 0

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.points = 0
        self.bankpoints = 0
        self.stacked_widget = QStackedWidget(self)
        self.startscreen = StartScreen(self.stacked_widget)
        self.gamescreen = GameScreen(self.stacked_widget)
        self.endscreen = EndScreen(self.stacked_widget)
        self.stacked_widget.addWidget(self.startscreen)
        self.stacked_widget.addWidget(self.gamescreen)
        self.stacked_widget.addWidget(self.endscreen)
        self.setCentralWidget(self.stacked_widget)
        self.setGeometry(500, 200, 600, 500)
        self.setWindowTitle("Game demonstration")
        self.show()


# insert styles for the game starting screen here
class StartScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.label = QLabel("Choose a starting number", self)
        self.label.setGeometry(150, 50, 350, 50)
        self.label.setFont(QFont('Arial', 20))
        numbers = generate_randoms()
        for i in range(len(numbers)):
            self.button = QPushButton(str(numbers[i]), self)
            self.button.setGeometry(30 + 110 * i, 150, 100, 40)
        self.startbutton = QPushButton("Start", self)
        self.startbutton.setGeometry(200, 300, 200, 80)
        self.startbutton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))


# insert styles for the game main screen here
class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget


# insert styles for the game end screen here
class EndScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        label = QLabel("", self)
        if points % 2:
            label.setText("First player wins!")
        else:
            label.setText("Second player wins!")
        label.setGeometry(150, 50, 350, 50)
        label.setFont(QFont('Arial', 20))
        newgamebutton = QPushButton("New game", self)
        newgamebutton.setGeometry(200, 300, 200, 80)
        newgamebutton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())








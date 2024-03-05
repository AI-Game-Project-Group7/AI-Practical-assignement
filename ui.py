import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from main import *

points = 0
bankpoints = 0
num = 50000




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
        self.startbutton.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1)) # Insert a function that set "num" and update widget


# insert styles for the game main screen here
class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        '''Adding text about num, points, bankpoints and player currently playing. Needs to be updated every time there is a change'''
        # Num
        self.label = QLabel("number : " + str(num), self)
        self.label.setGeometry(150, 50, 350, 50)
        self.label.setFont(QFont('Arial', 20))

        # Points
        self.label = QLabel("points : " + str(points), self)
        self.label.setGeometry(150, 50 + 25, 350, 50)
        self.label.setFont(QFont('Arial', 20))

        # Bankpoints
        self.label = QLabel("bankpoints : " + str(bankpoints), self)
        self.label.setGeometry(150, 50 + 50, 350, 50)
        self.label.setFont(QFont('Arial', 20))

        # Player
        self.label = QLabel("player : " + str(1), self)
        self.label.setGeometry(150, 50 + 200, 350, 50)
        self.label.setFont(QFont('Arial', 20))
        

        # Choosing between dividing the number by its dividers  
        dividers = check_possible_divisors(num)
        for i in range(len(dividers)):
            self.button = QPushButton(str(dividers[i]), self)
            self.button.setGeometry(90 + 110 * i, 150, 100, 40)
            self.button.clicked.connect(lambda : divid_number(self, dividers[i]))


def divid_number(self, divider):
    global num
    global points
    global bankpoints
    num  = num / divider
    points, bankpoints = update_points(num, points, bankpoints)
    self.repaint()
    dividers = check_possible_divisors(num)
    if dividers == []:
        self.stacked_widget.setCurrentIndex(2)








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








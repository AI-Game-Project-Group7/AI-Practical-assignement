import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QStackedWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from main import *
from state import State

state = State(50000)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.points = 0
        self.bankpoints = 0
        self.stacked_widget = QStackedWidget(self)
        self.gamescreen = GameScreen(self.stacked_widget)
        self.startscreen = StartScreen(self.stacked_widget, self.gamescreen)
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
    def __init__(self, stacked_widget, gamescreen):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.gamescreen = gamescreen
        self.label = QLabel("Choose a starting number", self)
        self.label.setGeometry(150, 50, 350, 50)
        self.label.setFont(QFont('Arial', 20))
        self.chosen_number = 0
        self.numbers = generate_randoms()

        # Add 5 buttons with numbers to choose from
        for i in range(len(self.numbers)):
            self.button = QPushButton(str(self.numbers[i]), self)
            self.button.setGeometry(30 + 110 * i, 150, 100, 40)
            self.button.clicked.connect(lambda _, index=i: self.on_numbutton_click(index))

        self.startbutton = QPushButton("Start", self)
        self.startbutton.setGeometry(200, 300, 200, 80)
        self.startbutton.clicked.connect(self.on_startbutton_click)

    def on_numbutton_click(self, i):
        self.chosen_number = self.numbers[i]
        state.num = self.chosen_number
        print(self.chosen_number)

    def on_startbutton_click(self):
        if self.chosen_number:
            self.gamescreen.update_labels()
            self.stacked_widget.setCurrentIndex(1)
        else:
            #insert warning/error message here
            pass


# insert styles for the game main screen here
class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        '''Adding text about num, points, bankpoints and player currently playing. Needs to be updated every time there is a change'''
        # Num
        self.nlabel = QLabel("number : " + str(state.num), self)
        self.nlabel.setGeometry(150, 50, 350, 50)
        self.nlabel.setFont(QFont('Arial', 20))

        # Points
        self.plabel = QLabel("points : " + str(state.pts), self)
        self.plabel.setGeometry(150, 50 + 25, 350, 50)
        self.plabel.setFont(QFont('Arial', 20))

        # Bankpoints
        self.blabel = QLabel("bankpoints : " + str(state.bankpts), self)
        self.blabel.setGeometry(150, 50 + 50, 350, 50)
        self.blabel.setFont(QFont('Arial', 20))

        # Player
        self.label = QLabel("player : " + str(1), self)
        self.label.setGeometry(150, 50 + 200, 350, 50)
        self.label.setFont(QFont('Arial', 20))

    # updates values on labels
    def update_labels(self):
        self.nlabel.setText("number : " + str(state.num))
        self.plabel.setText("points : " + str(state.pts))
        self.blabel.setText("bankpoints : " + str(state.bankpts))

# this function is not needed
"""def divid_number(self, divider):
    global num
    global points
    global bankpoints
    num  = num / divider
    points, bankpoints = update_points(num, points, bankpoints)
    update_labels()
    dividers = check_possible_divisors(num)
    if dividers == []:
        self.stacked_widget.setCurrentIndex(2)"""








# insert styles for the game end screen here
class EndScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        label = QLabel("", self)
        if state.pts % 2:
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








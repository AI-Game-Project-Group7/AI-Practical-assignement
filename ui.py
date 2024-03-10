import sys
import time
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QStackedWidget
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

    def on_startbutton_click(self):
        if self.chosen_number:
            self.stacked_widget.setCurrentIndex(1)
            self.gamescreen.start()
        else:
            #insert warning/error message here
            pass


# insert styles for the game main screen here
class GameScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.running = True
        self.starts = "p"
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
        self.label = QLabel("player turn", self)
        self.label.setGeometry(150, 50 + 200, 350, 50)
        self.label.setFont(QFont('Arial', 20))

    def start(self):
        if self.starts == "p":
            self.player_move()
        else:
            self.computer_move()

    def player_move(self):
        self.label.setText("player turn")
        self.update_labels()
        self.update_divisors()

    def computer_move(self):
        node = choose_next_node(state.num, state.pts, state.bankpts)
        if not node:
            self.stacked_widget.setCurrentIndex(2)
            self.who_wins()
        else:
            state.num, state.pts, state.bankpts = node.num, node.pts, node.bankpts
            for db in self.divbuttons:
                db.deleteLater()
            self.player_move()

    def on_divbutton_clicked(self, divisor):
        state.num = state.num // divisor
        state.pts, state.bankpts = update_points(state.num, state.pts, state.bankpts)
        for db in self.divbuttons:
            db.deleteLater()
        self.update_labels()
        self.update_divisors()
        self.label.setText("computer turn")
        QTimer.singleShot(3000, self.computer_move)

    def update_divisors(self):
        self.divbuttons = []
        divisors = check_possible_divisors(state.num)
        if not divisors:
            QTimer.singleShot(3000, lambda: self.stacked_widget.setCurrentIndex(2))
            self.who_wins()

        for div in divisors:
            self.divbutton = QPushButton(str(div), self)
            self.divbutton.setGeometry(400, 50 + 50 * div, 80, 30)
            self.divbutton.clicked.connect(lambda _, index=div: self.on_divbutton_clicked(index))
            self.divbuttons.append(self.divbutton)
            self.divbutton.show()

    # updates values on labels
    def update_labels(self):
        self.nlabel.setText("number : " + str(state.num))
        self.plabel.setText("points : " + str(state.pts))
        self.blabel.setText("bankpoints : " + str(state.bankpts))



    def who_wins(self):
        print("Going through me !")
        label = QLabel("", self)

        if state.pts % 2:
            label.setText("Second player wins!")
        else:
            label.setText("First player wins!")
        label.setGeometry(150, 50, 350, 50)
        label.setFont(QFont('Arial', 20))

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




        newgamebutton = QPushButton("New game", self)
        newgamebutton.setGeometry(200, 300, 200, 80)
        newgamebutton.clicked.connect(lambda: self.newGame())
    

    def newGame(self):
        state.pts = 0
        self.stacked_widget.setCurrentIndex(0)


app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())








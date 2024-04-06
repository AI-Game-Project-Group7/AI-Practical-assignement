import sys
import time
from time import perf_counter
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QStackedWidget, QButtonGroup, QRadioButton
from PyQt5.QtGui import QFont, QIcon
from main import *
from state import State

state = State(50000)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget(self)
        self.endscreen = EndScreen(self.stacked_widget)
        self.gamescreen = GameScreen(self.stacked_widget)
        self.startscreen = StartScreen(self.stacked_widget, self.gamescreen)
        self.stacked_widget.addWidget(self.startscreen)
        self.stacked_widget.addWidget(self.gamescreen)
        self.stacked_widget.addWidget(self.endscreen)
        self.setCentralWidget(self.stacked_widget)
        self.setStyleSheet("background-color: lightgrey;")
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
        self.label2 = QLabel("Choose who goes first", self)
        self.label2.setGeometry(50, 220, 350, 50)
        self.label2.setFont(QFont('Arial', 16))
        self.rb1 = QRadioButton("User", self)
        self.rb1.move(60, 270)
        self.rb1.setFont(QFont('Arial', 12))
        self.rb2 = QRadioButton("Computer", self)
        self.rb2.move(130, 270)
        self.rb2.setFont(QFont('Arial', 12))
        self.group_firstmove = QButtonGroup(self)
        self.group_firstmove.addButton(self.rb1)
        self.group_firstmove.addButton(self.rb2)
        self.label3 = QLabel("Choose an algorithm", self)
        self.label3.setGeometry(50, 350, 350, 50)
        self.label3.setFont(QFont('Arial', 16))
        self.rb3 = QRadioButton("Minimax", self)
        self.rb3.move(60, 400)
        self.rb3.setFont(QFont('Arial', 12))
        self.rb4 = QRadioButton("Alpha-Beta", self)
        self.rb4.move(150, 400)
        self.rb4.setFont(QFont('Arial', 12))
        self.group_algorithm = QButtonGroup(self)
        self.group_algorithm.addButton(self.rb3)
        self.group_algorithm.addButton(self.rb4)
        self.startbutton = QPushButton("Start", self)
        self.startbutton.setGeometry(350, 300, 200, 80)
        self.startbutton.setFont(QFont('Arial', 25))
        self.startbutton.setStyleSheet("background-color: lightgreen;")
        self.startbutton.clicked.connect(self.on_startbutton_click)
        # two additional menus should be added: who goes first -
        # user or computer, and which algorithm is used - minimax or alpha beta
        self.init_dynamic_attributes()

    def init_dynamic_attributes(self):
        self.chosen_number = 0
        self.numbers = generate_randoms()
        self.buttons = []
        # Add 5 buttons with numbers to choose from
        for i in range(len(self.numbers)):
            self.button = QPushButton(str(self.numbers[i]), self)
            self.button.setFont(QFont('Arial', 16))
            self.button.setGeometry(30 + 110 * i, 150, 100, 40)
            self.button.setStyleSheet("background-color: yellow;"
                                      "border: 1px solid")
            self.buttons.append(self.button)
            self.button.clicked.connect(lambda _, index=i: self.on_numbutton_click(index))


    def on_numbutton_click(self, i):
        for button in self.buttons:
            button.setStyleSheet("background-color: yellow;")
        self.buttons[i].setStyleSheet("background-color: lightgreen;")
        self.chosen_number = self.numbers[i]
        state.num = self.chosen_number

    def on_startbutton_click(self):
        checked_firstmove = self.group_firstmove.checkedButton()
        checked_algorithm = self.group_algorithm.checkedButton()
        if self.chosen_number and checked_firstmove and checked_algorithm:
            gamescreen = self.stacked_widget.widget(1)
            gamescreen.starts = checked_firstmove.text()
            gamescreen.algorithm = checked_algorithm.text()
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
        self.algorithm = "Alpha-Beta"
        self.starts = "User"
        self.node = []
        
        '''Adding text about num, points, bankpoints and player currently playing.'''
        # Num
        self.nlabel = QLabel("number : " + str(state.num), self)
        self.nlabel.setGeometry(150, 50, 350, 50)
        self.nlabel.setFont(QFont('Arial', 20))

        # Points
        self.plabel = QLabel("points : " + str(state.pts), self)
        self.plabel.setGeometry(150, 100, 350, 50)
        self.plabel.setFont(QFont('Arial', 20))

        # Bankpoints
        self.blabel = QLabel("bankpoints : " + str(state.bankpts), self)
        self.blabel.setGeometry(150, 150, 350, 50)
        self.blabel.setFont(QFont('Arial', 20))

        # Player
        self.label = QLabel("user turn", self)
        self.label.setGeometry(150, 250, 350, 50)
        self.label.setFont(QFont('Arial', 20))

    def start(self):
        root = make_tree(state.num, state.pts, state.bankpts)
        if self.algorithm == "Alpha-Beta":
            self.node = alpha_beta(root, starts=self.starts)
        elif self.algorithm == "Minimax":
            self.node = minimax(root, True, starts=self.starts)
            #self.node = root
            #print_tree(root) For display


        if self.starts == "User":
            self.player_move()
        else:
            self.label.setText("computer turn")
            self.update_labels()
            self.update_divisors()
            QTimer.singleShot(3000, self.computer_move)
            #self.computer_move()


    def player_move(self):
        self.label.setText("user turn")
        self.update_labels()
        self.update_divisors()

    def computer_move(self):
        start = perf_counter()
        self.node = self.set_current_node()
        node = choose_next_node(self.node)
        stop = perf_counter()
        print(f"time: {stop - start} s")
        self.node = node
        if not node:
            self.stacked_widget.setCurrentIndex(2)
        else:
            state.num, state.pts, state.bankpts = node.num, node.pts, node.bankpts
            for db in self.divbuttons:
                db.deleteLater()
            self.player_move()

    def set_current_node(self):
        root = make_tree(state.num, state.pts, state.bankpts)
        if self.algorithm == "Alpha-Beta":
            node = alpha_beta(root, starts=self.starts)
        else:
            minimax(root, True, starts=self.starts)
            node = root
        return node

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
            self.who_wins()
            QTimer.singleShot(3000, lambda: self.stacked_widget.setCurrentIndex(2))
        else:
            for div in divisors:
                self.divbutton = QPushButton(str(div), self)
                self.divbutton.setGeometry(400, 50 + 50 * div, 80, 30)
                self.divbutton.setStyleSheet("background-color: yellow;")
                self.divbutton.clicked.connect(lambda _, index=div: self.on_divbutton_clicked(index))
                self.divbuttons.append(self.divbutton)
                self.divbutton.show()

    # updates values on labels
    def update_labels(self):
        self.nlabel.setText("number : " + str(state.num))
        self.plabel.setText("points : " + str(state.pts))
        self.blabel.setText("bankpoints : " + str(state.bankpts))



    def who_wins(self):
        endscreen = self.stacked_widget.widget(2)
        if (state.pts % 2) == 0:
            state.pts += state.bankpts
        else:
            state.pts -= state.bankpts
        if (state.pts % 2) != 0:
            if self.starts == "Computer":
                endscreen.qlabel.setText("Computer wins!")
            else:
                endscreen.qlabel.setText("User wins!")
        else:
            if self.starts == "Computer":
                endscreen.qlabel.setText("User wins!")
            else:
                endscreen.qlabel.setText("Computer wins!")
        endscreen.qlabel.setGeometry(150, 50, 350, 50)
        endscreen.qlabel.setFont(QFont('Arial', 20))


# insert styles for the game end screen here
class EndScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        newgamebutton = QPushButton("New game", self)
        newgamebutton.setGeometry(200, 230, 200, 80)
        newgamebutton.setFont(QFont('Arial', 25))
        newgamebutton.setStyleSheet("background-color: lightgreen;")
        newgamebutton.clicked.connect(lambda: self.newGame())
        quitbutton = QPushButton("Quit", self)
        quitbutton.setGeometry(200, 350, 200, 80)
        quitbutton.setFont(QFont('Arial', 25))
        quitbutton.setStyleSheet("background-color: red;")
        quitbutton.clicked.connect(lambda: sys.exit())

        self.qlabel = QLabel("", self)
    

    def newGame(self):
        state.pts = 0
        state.bankpts = 0
        startscreen = self.stacked_widget.widget(0)
        startscreen.init_dynamic_attributes()
        self.stacked_widget.setCurrentIndex(0)


app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())








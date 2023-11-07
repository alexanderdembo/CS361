from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QLabel, QWidget, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QSize, QBasicTimer, Qt
import time
import json
import sys
import random

WIN_WIDTH = 800
WIN_HEIGHT = 800


class Game(QApplication):

    def __init__(self):
        super().__init__([])

        # Initialize style and set window
        self.setStyle("Fusion")
        self.window = GameWindow()

        # Start application
        self.window.show()
        sys.exit(self.exec())


class GameWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Holder variables for countries
        self.country1 = "Country #1"
        self.country2 = "Country #2"
        self.initializeWindow()
        self.initializeButtons()
        self.initializeLayout()



    def initializeWindow(self):
        # Set title and size
        self.setWindowTitle('Dembo CS361 Portfolio Project: "Higher or Lower: Country Populations"')
        self.setFixedSize(QSize(WIN_WIDTH, WIN_HEIGHT))

        # Make central widget to display all widgets on
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

    def initializeButtons(self):
        # Initialize buttons
        self.creatorlabel = QLabel("Made by Alexander Dembo, (C) 2023, CS361")
        self.statsbutton = StatsButton()
        self.infobutton = InfoButton()
        self.scorelabel = ScoreLabel()
        lcountrybutton = CountryButton(self.country1)
        lcountrylabel = CountryLabel(self.country1)
        self.lcountrylabelandbutton = CountryLabelAndButton(lcountrylabel, lcountrybutton)
        rcountrybutton = CountryButton(self.country2)
        rcountrylabel = CountryLabel(self.country2)
        self.rcountrylabelandbutton = CountryLabelAndButton(rcountrylabel, rcountrybutton)
        self.playbutton = PlayButton()
        self.resetbutton = ResetButton()
        self.gamemanager = GameManager(self.statsbutton, self.scorelabel, self.infobutton, self.playbutton, self.resetbutton, self.lcountrylabelandbutton, self.creatorlabel, self.rcountrylabelandbutton)



    def initializeLayout(self):
        # Layout setup of central widget
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.statsbutton, 0, 0)
        gridlayout.addWidget(self.scorelabel, 0, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(self.infobutton, 0, 2)
        gridlayout.addWidget(self.lcountrylabelandbutton.getCountryLabel(), 1, 0, alignment=Qt.AlignCenter)
        gridlayout.addWidget(self.playbutton, 1, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(self.resetbutton, 1, 1, alignment=Qt.AlignCenter)
        gridlayout.addWidget(self.rcountrylabelandbutton.getCountryLabel(), 1, 2, alignment=Qt.AlignCenter)
        gridlayout.addWidget(self.lcountrylabelandbutton.getCountryButton(), 2, 0)
        gridlayout.addWidget(self.creatorlabel, 2, 1, alignment=Qt.AlignBottom)
        gridlayout.addWidget(self.rcountrylabelandbutton.getCountryButton(), 2, 2)

        # Set layout to the setup layout
        self.centralwidget.setLayout(gridlayout)

class StatsButton(QPushButton):

    def __init__(self):
        super().__init__("Stats")

        # Maintain scores, set on_click function
        self.clicked.connect(self.showStats)
        self._current_score = 0
        self._games = 0
        self._scores = []

    def showStats(self):
        # Show dialog box with stats
        info = QMessageBox()
        info.setWindowTitle("Stats")
        if self._games == 0:
            average = 0
        else:
            average = sum(self._scores) / self._games
        info.setText(f"Recent Score: {self._current_score}\nAverage Score: {average}")
        info.exec()

    def addScore(self, score):
        self._current_score = score
        self._scores.append(score)
        self._games += 1

class InfoButton(QPushButton):

    def __init__(self):
        super().__init__("Info")

        # Set on_click function
        self.clicked.connect(self.showInfo)

    def showInfo(self):
        # Show dialog box with how-to-play
        info = QMessageBox()
        info.setText("How to play: You are trying to guess which country has a higher population. Click the corresponding button to guess that that country has a higher "
                     "population than the other country. Timer is set to 10 seconds per guess")
        info.setWindowTitle("Info")
        info.exec()

class CountryLabel(QLabel):

    def __init__(self, countryname):
        super().__init__(countryname)

        self._country = countryname
        self.setHidden(True)

    def getCountry(self):
        return self._country

    def setCountry(self, countryname):
        self._country = countryname
        self.setText(self._country)

class CountryButton(QPushButton):

    def __init__(self, countryname):
        super().__init__(countryname)

        # Store country name and score label to update on guess, set on_click function
        self._country = countryname
        self.setHidden(True)

    def setCountry(self, countryname):
        self._country = countryname
        self.setText(self._country)

    def getCountry(self):
        return self._country


class ScoreLabel(QLabel):

    def __init__(self, score=0):
        super().__init__(f"Score: {score}")

        # Store score
        self._score = score

    def updateScore(self):
        # Increment the score, update the label
        self._score += 1
        self.setText(f"Score: {self._score}")

    def setScore(self, score):
        # Set the score
        self._score = score
        self.setText(f"Score: {self._score}")

    def getScore(self):
        # Return the score
        return self._score

class PlayButton(QPushButton):

    def __init__(self):
        super().__init__("Play")


class ResetButton(QPushButton):

    def __init__(self):
        super().__init__("Reset")
        self.setHidden(True)

class CountryLabelAndButton():

    def __init__(self, countrylabel, countrybutton):
        self._countrylabel = countrylabel
        self._countrybutton = countrybutton
        self._population = 0

    def setCountry(self, countryname, population):
        self._countrylabel.setCountry(countryname)
        self._countrybutton.setCountry(countryname)
        self._population = population

    def getCountryLabel(self):
        return self._countrylabel

    def getCountryButton(self):
        return self._countrybutton

    def show(self):
        self._countrylabel.setHidden(False)
        self._countrybutton.setHidden(False)

    def hide(self):
        self._countrylabel.setHidden(True)
        self._countrybutton.setHidden(True)

class GameManager():

    def __init__(self, statsbutton, scorelabel, infobutton, playbutton, resetbutton, lcountrylabelandbutton, creatorlabel, rcountrylabelandbutton):
        self.resetCountryList()
        self._statsbutton = statsbutton
        self._scorelabel = scorelabel
        self._infobutton = infobutton
        self._playbutton = playbutton
        self._playbutton.clicked.connect(self.play)
        self._resetbutton = resetbutton
        self._resetbutton.clicked.connect(self.reset)
        self._lcountrylabelandbutton = lcountrylabelandbutton
        self._rcountrylabelandbutton = rcountrylabelandbutton
        self._lcountrylabelandbutton.getCountryButton().clicked.connect(lambda: self.guessMade(self._lcountrylabelandbutton.getCountryButton()))
        self._rcountrylabelandbutton.getCountryButton().clicked.connect(lambda: self.guessMade(self._rcountrylabelandbutton.getCountryButton()))
        self._leftcountry = ""
        self._leftpopulation = 0
        self._rightcountry = ""
        self._rightpopulation = 0

    def play(self):
        # Hide play button
        self._playbutton.setHidden(True)

        self._leftcountry, self._leftpopulation = self.pickCountry(self._lcountrylabelandbutton)
        self._rightcountry, self._rightpopulation = self.pickCountry(self._rcountrylabelandbutton)

        # Show country widgets
        self._lcountrylabelandbutton.show()
        self._rcountrylabelandbutton.show()
        self._resetbutton.show()

    def reset(self):
        # Show play button
        self._playbutton.setHidden(False)

        # Hide country widgets
        self._lcountrylabelandbutton.hide()
        self._rcountrylabelandbutton.hide()
        self._resetbutton.setHidden(True)


        final_score = self._scorelabel.getScore()
        self._statsbutton.addScore(final_score)
        self._scorelabel.setScore(0)

        self.resetCountryList()

        self._statsbutton.showStats()

    def pickCountry(self, countrylabelandbutton):
        if self._numofcountries >= 1:
            rnum = random.randint(0, self._numofcountries - 1)
            countrydata = self._countries.pop(rnum)
            self._numofcountries -= 1
            countrylabelandbutton.setCountry(countrydata["country"], countrydata["population"])
            return countrydata["country"], countrydata["population"]

    def guessMade(self, button):
        guess = button.text()
        if self._leftcountry == guess:
            if self._leftpopulation > self._rightpopulation:
                self._scorelabel.updateScore()
                self._rightcountry, self._rightpopulation = self.pickCountry(self._rcountrylabelandbutton)
            else:
                self.reset()
        else:
            if self._rightpopulation > self._leftpopulation:
                self._scorelabel.updateScore()
                self._lcountrylabelandbutton.setCountry(self._rightcountry, self._rightpopulation)
                self._rightcountry, self._rightpopulation = self.pickCountry(self._rcountrylabelandbutton)
            else:
                self.reset()

    def resetCountryList(self):
        file = open('country-by-population.json')
        self._countries = json.load(file)
        self._numofcountries = len(self._countries)

if __name__ == "__main__":
    game = Game()

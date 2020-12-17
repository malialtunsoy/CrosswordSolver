from requests.api import delete
from scraping import Scraping
from crosswordSolver import CrosswordSolver
from nyTimesPuzzle import Connector
from newSolver import newSolver
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from crossword_gui import Ui_MainWindow
import json


class LUMOSCrosswordSolver:
    def __init__(self):
        self.cellNumberArray = []
        self.cellBlockArray = []
        self.cluesAcross = []
        self.cluesDown = []
        self.cellAnswerArray = []

        self.clues = {"across": {}, "down": {}}
        self.domains = {"across": {}, "down": {}}

    def run(self, demo):
        if demo:
            # GET CROSSWORD PUZZLE

            nyTimesConnector = Connector(
                "C:\Program Files (x86)/chromedriver.exe")
            nyTimesConnector.connectToPuzzle()
            self.cellNumberArray = nyTimesConnector.cellNumberArray
            self.cellBlockArray = nyTimesConnector.cellBlockArray
            self.cluesAcross = nyTimesConnector.cluesAcross
            self.cluesDown = nyTimesConnector.cluesDown
            self.cellAnswerArray = nyTimesConnector.cellAnswerArray
            self.setClues()
            print("===================\nWEB SCRAPING\n===================")
            webScrapper = Scraping(
                self.clues, self.cellAnswerArray, self.cellNumberArray)
            webScrapper.setDomains()
            print("===================\nSOLVING THE PUZZLE\n===================")
            puzzleSolver = newSolver(self.cellBlockArray, self.cellNumberArray,
                                     self.cluesDown, self.cluesAcross, webScrapper.domains)
        else:

            #with open('data.json', 'r') as fp:
            #    data = json.load(fp)
            with open('cellBlockArray.json', 'r') as fp:
                self.cellBlockArray = json.load(fp)
            with open('cellNumberArray.json', 'r') as fp:
                self.cellNumberArray = json.load(fp)
            with open('clueAcross.json', 'r') as fp:
                self.cluesAcross = json.load(fp)
            with open('cluesDown.json', 'r') as fp:
                self.cluesDown = json.load(fp)
            with open('answers.json', 'r') as fp:
                self.cellAnswerArray = json.load(fp)
            print("===================\nWEB SCRAPING\n===================")
            self.setClues()
            webScrapper = Scraping(self.clues, self.cellAnswerArray, self.cellNumberArray)
            webScrapper.setDomains()
            print("===================\nSOLVING THE PUZZLE\n===================")
            puzzleSolver = newSolver(self.cellBlockArray, self.cellNumberArray,self.cluesDown, self.cluesAcross, webScrapper.domains)

        # SAVE
        """
        with open('cellBlockArray.json', 'w') as fp:
            json.dump(self.cellBlockArray, fp,  indent=4)
        with open('cellNumberArray.json', 'w') as fp:
            json.dump(self.cellNumberArray, fp,  indent=4)
        with open('clueAcross.json', 'w') as fp:
            json.dump(self.cluesAcross, fp,  indent=4)
        with open('cluesDown.json', 'w') as fp:
            json.dump(self.cluesDown, fp,  indent=4)
        with open('data.json', 'w') as fp:
            json.dump(webScrapper.domains, fp,  indent=4)
        """
        # puzzleSolver = CrosswordSolver(self.cellBlockArray, self.cellNumberArray,self.cluesDown, self.cluesAcross, data)#webScrapper.domains)
        #puzzleSolver = newSolver(cellBlockArray, cellNumberArray,cluesDown, cluesAcross, webScrapper.domains)

        print("===================\nSOLUTION\n===================")
        for i in puzzleSolver.solvedPuzzle:
            print(i)
        # DRAW GUI
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow, self.cellNumberArray, self.cellBlockArray, self.cluesAcross,
                   self.cluesDown, self.cellAnswerArray, puzzleSolver.solvedPuzzle)
        MainWindow.show()
        sys.exit(app.exec_())

    def setClues(self):
        for across in self.cluesAcross:
            self.clues["across"][across[0]] = across[1]
        for down in self.cluesDown:
            self.clues["down"][down[0]] = down[1]


lumos = LUMOSCrosswordSolver()
lumos.run(True)

from requests.api import delete
from scraping import Scraping
from crosswordSolver import CrosswordSolver
from nyTimesPuzzle import Connector
from newSolver import newSolver
import json

class LUMOSCrosswordSolver:
    def __init__(self):
        self.cellNumberArray = []
        self.cellBlockArray = []
        self.cluesAcross = []
        self.cluesDown = []
        self.cellAnswerArray = []

        self.clues =  {"across": {}, "down":{}}
        self.domains =  {"across": {}, "down":{}}

    def run(self, ):
        #GET CROSSWORD PUZZLE
        """
        nyTimesConnector = Connector("C:\Program Files (x86)/chromedriver.exe")
        nyTimesConnector.connectToPuzzle()
        self.cellNumberArray = nyTimesConnector.cellNumberArray
        self.cellBlockArray = nyTimesConnector.cellBlockArray
        self.cluesAcross = nyTimesConnector.cluesAcross
        self.cluesDown = nyTimesConnector.cluesDown
        self.cellAnswerArray = nyTimesConnector.cellAnswerArray
        """
        self.setClues()

        #WEB SCRAPING AND SETTING DOMAINS
        print("===================\nWEB SCRAPING\n===================")
        #webScrapper = Scraping(self.clues, self.cellAnswerArray, self.cellNumberArray)
        #webScrapper.setDomains()
        #SOLVE THE PUZZLE
        print("===================\nSOLVING THE PUZZLE\n===================")
        
        with open('data.json', 'r') as fp:
            data = json.load(fp)
        with open('cellBlockArray.json', 'r') as fp:
            cellBlockArray = json.load(fp)
        with open('cellNumberArray.json', 'r') as fp:
            cellNumberArray = json.load(fp)
        with open('clueAcross.json', 'r') as fp:
            cluesAcross = json.load(fp)
        with open('cluesDown.json', 'r') as fp:
            cluesDown = json.load(fp)
        
        """
        with open('cellBlockArray.json', 'w') as fp:
            json.dump(self.cellBlockArray, fp,  indent=4)
        with open('cellNumberArray.json', 'w') as fp:
            json.dump(self.cellNumberArray, fp,  indent=4)
        with open('clueAcross.json', 'w') as fp:
            json.dump(self.cluesAcross, fp,  indent=4)
        with open('cluesDown.json', 'w') as fp:
            json.dump(self.cluesDown, fp,  indent=4)
        """
        #puzzleSolver = CrosswordSolver(self.cellBlockArray, self.cellNumberArray,self.cluesDown, self.cluesAcross, data)#webScrapper.domains)
        puzzleSolver = newSolver(cellBlockArray, cellNumberArray,cluesDown, cluesAcross, data)#webScrapper.domains)
        
        #DRAW GUI

    def setClues(self):
        for across in self.cluesAcross:
            self.clues["across"][across[0]] = across[1]
        for down in self.cluesDown:
            self.clues["down"][down[0]] = down[1]

lumos = LUMOSCrosswordSolver()
lumos.run()
#print(lumos.clues)

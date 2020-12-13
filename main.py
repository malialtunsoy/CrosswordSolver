from scraping import Scraping
from crosswordSolver import CrosswordSolver
from nyTimesPuzzle import Connector

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
        nyTimesConnector = Connector("C:\Program Files (x86)/chromedriver.exe")
        nyTimesConnector.connectToPuzzle()
        self.cellNumberArray = nyTimesConnector.cellNumberArray
        self.cellBlockArray = nyTimesConnector.cellBlockArray
        self.cluesAcross = nyTimesConnector.cluesAcross
        self.cluesDown = nyTimesConnector.cluesDown
        self.cellAnswerArray = nyTimesConnector.cellAnswerArray

        self.setClues()

        #WEB SCRAPING AND SETTING DOMAINS
        webScrapper = Scraping(self.clues)
        webScrapper.setDomains()
        print(webScrapper.domains)
        
        #SOLVE THE PUZZLE
        
        puzzleSolver = CrosswordSolver(self.cellBlockArray, self.cellNumberArray,self.cluesDown, self.cluesAcross, webScrapper.domains)
        
        #DRAW GUI

    def setClues(self):
        for across in self.cluesAcross:
            self.clues["down"][across[0]] = across[1]
        for down in self.cluesDown:
            self.clues["across"][down[0]] = down[1]

lumos = LUMOSCrosswordSolver()
lumos.run()
print(lumos.clues)
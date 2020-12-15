from getMerriamWebster import get_merriam_webster
from getMerriamWebster import combine_tokens
from searchWikipedia import searchWikipediaApi
from synonyms import searchSynonyms

class Scraping:
    def __init__(self, clues, answers, gridIndex):
        self.clues = clues
        self.domains = {"across": {}, "down":{}}
        self.answers = answers
        self.gridIndex = gridIndex

    def setDomains(self):
        for down in self.clues["down"]:
            self.domains["down"][down] = self.search(self.clues["down"][down])
        for across in self.clues["across"]:
            self.domains["across"][across] = self.search(self.clues["across"][across])
        #======================== CHEAT =============================
        #self.cheat()

    def getClueList(self, clue):
        clueList = [clue]
        return clueList

    def search(self, clue):
        domain = ""
        
        for toSearch in self.getClueList(clue):
            print("Google search for:", toSearch)
            try:
                domain = domain + self.getGoogle(toSearch)
            except:
                print("An exception occurred")
            
            print("Wikipedia search for:", toSearch)
            try:
                domain = domain + self.getWiki(toSearch)
            except:
                print("An exception occurred")
            
            print("Synonym search for:", toSearch)
            try:
                domain = domain + self.getSynonyms(toSearch)
            except:
                print("An exception occurred")
            
            print("Merriam Webster search for:", toSearch)
            try:
                domain = domain + self.getMerriam(toSearch)
            except:
                print("An exception occurred")
        

        return domain

    def getGoogle(self, toSearch):

        return "toSearch"

    def getWiki(self, toSearch):
        return searchWikipediaApi(toSearch)

    def getMerriam(self,toSearch):
        return get_merriam_webster(toSearch)

    def getSynonyms(self, toSearch):
        return searchSynonyms(toSearch)

    def cheat(self):
        for across in self.clues["across"]:
            if across in ["1","8"]:
                for row in range(0,5):
                    for col in range(0,5):
                        if self.gridIndex[row][col] == across:
                            answer = ""
                            for colIn in range(0,5):
                                if self.answers[row][colIn] != "-":
                                    answer = answer + self.answers[row][colIn]
                            self.domains["across"][across] = self.domains["across"][across] + " " + answer
                            #print(answer)

        for down in self.clues["down"]:
            if down in ["1","2","3","5"]:
                for row in range(0,5):
                    for col in range(0,5):
                        if self.gridIndex[row][col] == down:
                            answer = ""
                            for rowIn in range(0,5):
                                if self.answers[rowIn][col] != "-":
                                    answer = answer + self.answers[rowIn][col]
                            self.domains["down"][down] = self.domains["down"][down] + " " + answer
                            #print(answer)


"""
scraping = Scraping()
scraping.setDomains()
print(scraping.domains)
"""
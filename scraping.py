from getMerriamWebster import searchMerriamWebster
from searchWikipedia import searchWikipedia
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
        domain = set()
        wiki_set = set()
        synonym_set = set()
        merriam_set = set()
        toSearch = clue
        """
        print("Google search for:", toSearch)
        try:
            domain = domain + self.getGoogle(toSearch)
        except:
            print("An exception occurred")
        """
        print("Wikipedia search for:", toSearch)
        try:

            wiki_set = wiki_set | self.getWiki(toSearch)
        except:
            print("An exception occurred")
        
        print("Synonym search for:", toSearch)
        try:
            synonym_set = synonym_set | self.getSynonyms(toSearch)
        except:
            print("An exception occurred")
        
        print("Merriam Webster search for:", toSearch)
        try:
            merriam_set = merriam_set | self.getMerriam(toSearch)
        except:
            print("An exception occurred")
            
        domain = domain.union(wiki_set, synonym_set, merriam_set)
        return ' '.join(str(e) for e in domain) #''.join(str(e) for e in words)

    def getGoogle(self, toSearch):

        return "toSearch"

    def getWiki(self, toSearch):
        return searchWikipedia(toSearch)

    def getMerriam(self,toSearch):
        return searchMerriamWebster(toSearch)

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
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

    def search(self, clue):
        """
        This function searches clue on wikipedia, merriam webster and datamuse.
        Calls two functions, getWiki and getSynonyms. At the end of the function,
        it gets union of the returning sets from the functions so that duplicates
        are eliminated.
        Returns a text including all words that are found on web.
        """
        domain = set()
        wiki_set = set()
        synonym_set = set()
        toSearch = clue

        print("Wikipedia search for:", toSearch)
        try:
            wiki_set = wiki_set | self.getWiki(toSearch)
        except:
            print("An exception occurred")
        
        print("Synonym search from Datamuse and Merriam-Webster for:", toSearch)
        try:
            synonym_set = synonym_set | self.getSynonyms(toSearch)
        except:
            print("An exception occurred")
        
        domain = domain.union(wiki_set, synonym_set)
        return ' '.join(str(e) for e in domain) 

    def getWiki(self, toSearch):
        return searchWikipedia(toSearch)

    def getSynonyms(self, toSearch):
        return searchSynonyms(toSearch, self.clues["across"], self.clues["down"])

    def cheat(self):
        for across in self.clues["across"]:
            for row in range(0,5):
                for col in range(0,5):
                    if self.gridIndex[row][col] == across:
                        answer = ""
                        for colIn in range(0,5):
                            if self.answers[row][colIn] != "-":
                                answer = answer + self.answers[row][colIn]
                        self.domains["across"][across] = self.domains["across"][across] + " " + answer

        for down in self.clues["down"]:
            for row in range(0,5):
                for col in range(0,5):
                    if self.gridIndex[row][col] == down:
                        answer = ""
                        for rowIn in range(0,5):
                            if self.answers[rowIn][col] != "-":
                                answer = answer + self.answers[rowIn][col]
                        self.domains["down"][down] = self.domains["down"][down] + " " + answer
                            

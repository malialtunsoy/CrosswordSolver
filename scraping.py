class Scraping:
    def __init__(self, clues):
        self.clues = clues
        self.domains = {"across": {}, "down":{}}

    def setDomains(self):
        for down in self.clues["down"]:
            self.domains["down"][down] = self.search(self.clues["down"][down])
        for across in self.clues["across"]:
            self.domains["across"][across] = self.search(self.clues["across"][across])

    def getClueList(self, clue):
        clueList = [clue]
        return clueList

    def search(self, clue):
        domain = ""
        for toSearch in self.getClueList(clue):
            domain = domain + self.getGoogle(toSearch)
            domain = domain + self.getWiki(toSearch)

        return domain

    def getGoogle(self, toSearch):

        return "toSearch"

    def getWiki(self, toSearch):

        return "toSearch"

"""
scraping = Scraping()
scraping.setDomains()
print(scraping.domains)
"""
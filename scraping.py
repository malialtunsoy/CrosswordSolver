class Scraping:
    def __init__(self):
        self.clues = {"across": {'1': '"Brooklyn Nine-Nine" or "The King of Queens"','5': '"What happens to us while we are making other plans," per Allen Saunders','6': 'Enjoys Santa Monica, perhaps','7': '"It\'s all clear now"','8': 'Singer nicknamed the "Goddess of Pop"'}, "down":{'1': 'Partially melted snow','2': 'New employee','3': 'Result of a successful job interview','4': 'Director Anderson','6': '[not my mistake]'}}
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


scraping = Scraping()
scraping.setDomains()
print(scraping.domains)
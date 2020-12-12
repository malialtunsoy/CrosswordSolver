
class CrosswordSolver:
    def __init__(self, grid, numbers, downClues, acrossClues):
        self.grid = grid
        self.numbers = numbers
        self.downClues = downClues
        self.acrossClues = acrossClues

        self.lengthOfDownClues = []
        self.lengthOfAcrossClues = []
        self.wordLengthCalculator()

        self.downClueDomains = []
        self.acrossClueDomains = []
        self.webScrap()
        self.filterDomains()

        
    def wordLengthCalculator(self):
        #downClues
        for clue in self.downClues:
            clueNumber = clue[0]
            rowIndex = -1
            colIndex = -1
            counter = 0
            for row in self.numbers:
                if clueNumber in row:
                    rowIndex = counter
                counter = counter + 1
            colIndex = self.numbers[rowIndex].index(clueNumber)

            #count spaces
            wordLength = 0
            for row in self.grid[rowIndex:]:
                if row[colIndex] == "0":
                    wordLength = wordLength + 1
            self.lengthOfDownClues.append([clueNumber, wordLength])

            #acrossClues
        for clue in self.acrossClues:
            clueNumber = clue[0]
            rowIndex = -1
            colIndex = -1
            counter = 0
            for row in self.numbers:
                if clueNumber in row:
                    rowIndex = counter
                counter = counter + 1
            colIndex = self.numbers[rowIndex].index(clueNumber)

            #count spaces
            wordLength = 0
            for cell in self.grid[rowIndex][colIndex:]:
                if cell == "0":
                    wordLength = wordLength + 1
            self.lengthOfAcrossClues.append([clueNumber, wordLength])
    
    def webScrap(self):
        print("TODO")
        textFromWeb = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        self.acrossClueDomains = {"1":textFromWeb,"5":textFromWeb ,"6":textFromWeb ,"7":textFromWeb ,"8":textFromWeb}
        self.downClueDomains = {"1":textFromWeb,"2":textFromWeb ,"3":textFromWeb ,"4":textFromWeb ,"6":textFromWeb}

    def filterDomains(self):
        #downClues
        newDomain = []
        for clue in self.lengthOfDownClues:
            for word in self.downClueDomains[clue[0]].split():
                if len(word) == clue[1]:
                    newDomain.append(word)
            self.downClueDomains[clue[0]] = newDomain
            newDomain = []

         #acrossClues
        newDomain = []
        for clue in self.lengthOfAcrossClues:
            for word in self.acrossClueDomains[clue[0]].split():
                if len(word) == clue[1]:
                    newDomain.append(word)
            self.acrossClueDomains[clue[0]] = newDomain
            newDomain = []





grid = [["1","0","0","0","0"],["1","0","0","0","0"],["0","0","0","0","0"],["0","0","0","0","1"],["0","0","0","0","1"]]
numbers = [["-","1","2","3","4"],["-","5","-","-","-"],["6","-","-","-","-"],["7","-","-","-","-"],["8","-","-","-","-"]]
downClues = [['1', 'Partially melted snow'],['2', 'New employee'],['3', 'Result of a successful job interview'],['4', 'Director Anderson'],['6', '[not my mistake]']]
acrossClues = [['1', '"Brooklyn Nine-Nine" or "The King of Queens"'],['5', '"What happens to us while we are making other plans," per Allen Saunders'],['6', 'Enjoys Santa Monica, perhaps'],['7', '"It\'s all clear now"'],['8', 'Singer nicknamed the "Goddess of Pop"']]

sovler = CrosswordSolver(grid, numbers, downClues, acrossClues)

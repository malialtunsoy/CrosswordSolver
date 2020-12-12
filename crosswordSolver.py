
class CrosswordSolver:
    def __init__(self, grid, numbers, downClues, acrossClues):
        self.grid = grid
        self.numbers = numbers
        self.downClues = downClues
        self.acrossClues = acrossClues

        self.lengthOfDownClues = {}
        self.lengthOfAcrossClues = {}
        
        self.locationOfDownClues = {}
        self.locationOfAcrossClues = {}
        self.wordLengthCalculator()

        self.downClueDomains = {}
        self.acrossClueDomains = {}
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
            self.lengthOfDownClues[clueNumber] = wordLength
            self.locationOfDownClues[clueNumber] = {"start": {"row": rowIndex, "col": colIndex}, "end": {"row": rowIndex+wordLength-1, "col": colIndex}}

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
            self.lengthOfAcrossClues[clueNumber] = wordLength
            self.locationOfAcrossClues[clueNumber] = {"start": {"row": rowIndex, "col": colIndex}, "end": {"row": rowIndex, "col": colIndex+wordLength-1}}
    
    def webScrap(self):
        print("TODO")
        textFromWeb = "Lorem Ipsum is simply dummy offers text of the Henry's printing and typesetting industry. John' Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        self.acrossClueDomains = {"1":textFromWeb,"5":textFromWeb ,"6":textFromWeb ,"7":textFromWeb ,"8":textFromWeb}
        self.downClueDomains = {"1":textFromWeb,"2":textFromWeb ,"3":textFromWeb ,"4":textFromWeb ,"6":textFromWeb}

    def filterDomains(self):
        #downClues
        newDomain = []
        for clue in self.lengthOfDownClues:
            previousWord = ""
            for word in self.downClueDomains[clue].split():
                if (len(word) == self.lengthOfDownClues[clue]) and (word not in newDomain): #if word lenght is valid
                    newDomain.append(word.upper())
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfDownClues[clue]) and (prevPlusCur != word) and (prevPlusCur not in newDomain): #if two words next to each others total length is valid
                    newDomain.append(prevPlusCur.upper())
                previousWord = word
                if (len(word) == self.lengthOfDownClues[clue]+1) and (word[self.lengthOfDownClues[clue]] == "s") and (word not in newDomain): #if the word ends with "s"
                    newDomain.append(word[0:self.lengthOfDownClues[clue]].upper())
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfDownClues[clue]) and (word[0:word.index("'")] not in newDomain):
                    newDomain.append(word[0:word.index("'")].upper())
            self.downClueDomains[clue] = newDomain
            newDomain = []

        #acrossClues
        newDomain = []
        for clue in self.lengthOfAcrossClues:
            previousWord = ""
            for word in self.acrossClueDomains[clue].split():
                if (len(word) == self.lengthOfAcrossClues[clue]) and (word not in newDomain): #if word lenght is valid
                    newDomain.append(word.upper())
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfAcrossClues[clue]) and (prevPlusCur != word) and (prevPlusCur not in newDomain): #if two words next to each others total length is valid
                    newDomain.append(prevPlusCur.upper())
                previousWord = word
                if (len(word) == self.lengthOfAcrossClues[clue]+1) and (word[self.lengthOfAcrossClues[clue]] == "s") and (word not in newDomain): #if the word ends with "s"
                    newDomain.append(word[0:self.lengthOfAcrossClues[clue]].upper())
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfAcrossClues[clue]) and (word[0:word.index("'")] not in newDomain):
                    newDomain.append(word[0:word.index("'")].upper())
            self.acrossClueDomains[clue] = newDomain
            newDomain = []


grid = [["1","0","0","0","0"],["1","0","0","0","0"],["0","0","0","0","0"],["0","0","0","0","1"],["0","0","0","0","1"]]
numbers = [["-","1","2","3","4"],["-","5","-","-","-"],["6","-","-","-","-"],["7","-","-","-","-"],["8","-","-","-","-"]]
downClues = [['1', 'Partially melted snow'],['2', 'New employee'],['3', 'Result of a successful job interview'],['4', 'Director Anderson'],['6', '[not my mistake]']]
acrossClues = [['1', '"Brooklyn Nine-Nine" or "The King of Queens"'],['5', '"What happens to us while we are making other plans," per Allen Saunders'],['6', 'Enjoys Santa Monica, perhaps'],['7', '"It\'s all clear now"'],['8', 'Singer nicknamed the "Goddess of Pop"']]

solver = CrosswordSolver(grid, numbers, downClues, acrossClues)

print("\n Domain of down clues")
for i in solver.downClueDomains:
    print(i, solver.downClueDomains[i])

print("\n Domain of across clues")
for i in solver.acrossClueDomains:
    print(i, solver.acrossClueDomains[i])

print("\n Location of down clues")

for down in solver.locationOfDownClues:
    print(down, "start: ", solver.locationOfDownClues[down]["start"], "end: ", solver.locationOfDownClues[down]["end"])

print("\n Location of across clues")

for across in solver.locationOfAcrossClues:
    print(across, "start: ", solver.locationOfAcrossClues[across]["start"], "end: ", solver.locationOfAcrossClues[across]["end"])
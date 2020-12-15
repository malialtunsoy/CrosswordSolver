import itertools
import copy
import string
import json
class CrosswordSolver:
    def __init__(self, grid, numbers, downClues, acrossClues, domains):
        self.grid = grid
        self.numbers = numbers
        self.downClues = downClues
        self.acrossClues = acrossClues
        self.initialDomains = copy.deepcopy(domains) #INITIAL
        
        
        self.lengthOfDownClues = {}
        self.lengthOfAcrossClues = {}
        
        self.locationOfDownClues = {}
        self.locationOfAcrossClues = {}

        self.neglectedWords = {"row": [], "col": []} 
        self.neglectedWordsArray = []
        self.count = 0

        self.bestSolution = {"down": {}, "across": {}, "find": 0}

        self.solvedPuzzle = []
        """
        self.downClueDomains = {}
        self.acrossClueDomains = {}
        """
        self.filteredDomains = {"down": {}, "across": {}} #FILTERED

        self.wordLengthCalculator()    
        #self.webScrap()
        self.filterDomains()
        self.tempDomains = copy.deepcopy(self.filteredDomains) #TEMP
        for down in self.filteredDomains["down"]:
            print(down, self.filteredDomains["down"][down])
        for across in self.filteredDomains["across"]:
            print(across, self.filteredDomains["across"][across])
        
        
        
        print("Initial size of the down domains:")
        for down in self.filteredDomains["down"]:
            print(down, "length: ", len(self.filteredDomains["down"][down]))
        print("Initial size of the across domains:")
        for across in self.filteredDomains["across"]:
            print(across, "length: ", len(self.filteredDomains["across"][across]))


        self.solvePuzzle()
        self.printBestDomains()
        self.getAnswerGrid()

        
        
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
    """
    def webScrap(self):
        #textFromWeb = "reps cello alias pizza ncaa capn relic eliza plaza sosa Lorem Ipsum is + simply dummy sic offers slush show hiree life surfs offer wes isee cher text of the Henry's printing and 10 typesetting industry. John' Lorem 0 Ipsum has kill, murder!been john; plus+ for: the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        #textFromWeb = "reps cello alias pizza ncaa capn relic eliza plaza sosa"

        self.acrossClueDomains = self.domains["across"]
        self.downClueDomains = self.domains["down"]
        
        self.acrossClueDomains = {"1":textFromWeb,"5":textFromWeb ,"6":textFromWeb ,"7":textFromWeb ,"8":textFromWeb}
        self.downClueDomains = {"1":textFromWeb,"2":textFromWeb ,"3":textFromWeb ,"4":textFromWeb ,"5":textFromWeb}
        
    """
    def filterDomains(self):
        #downClues
        newDomain = []
        for clue in self.initialDomains["down"]:
            previousWord = ""
            for word in self.initialDomains["down"][clue].split():
                word = self.filterHelper(word)
                if word[len(word)-1] == "." or word[len(word)-1] == ","  or word[len(word)-1] == ":"  or word[len(word)-1] == ";"  or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]":
                    word = word[0:len(word)-1]
                if (len(word) == self.lengthOfDownClues[clue]) and (word.upper() not in newDomain): #if word lenght is valid
                    newDomain.append(word.upper())
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfDownClues[clue]) and (prevPlusCur != word) and (prevPlusCur.upper() not in newDomain): #if two words next to each others total length is valid
                    newDomain.append(prevPlusCur.upper())
                previousWord = word
                if (len(word) == self.lengthOfDownClues[clue]+1) and (word[self.lengthOfDownClues[clue]] == "s") and (word not in newDomain): #if the word ends with "s"
                    newDomain.append(word[0:self.lengthOfDownClues[clue]].upper())
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfDownClues[clue]) and (word[0:word.index("'")].upper() not in newDomain):
                    newDomain.append(word[0:word.index("'")].upper())
            for word in self.initialDomains["down"][clue].split("'"):
                if (len(word) == self.lengthOfDownClues[clue]) and (word.upper() not in newDomain): #if word lenght is valid
                    newDomain.append(word.upper())
            for word in reversed(newDomain):
                deleted = False
                for letter in word:
                    if not letter in list(string.ascii_uppercase) and not deleted:
                        newDomain.remove(word)
                        deleted = True       
            newDomain = sorted(newDomain, key=str.lower)     
            #self.downClueDomains[clue] = newDomain.copy()
            self.filteredDomains["down"][clue] = copy.deepcopy(newDomain)
            newDomain = []

        #acrossClues
        newDomain = []
        for clue in self.lengthOfAcrossClues:
            previousWord = ""
            for word in self.initialDomains["across"][clue].split():
                word = self.filterHelper(word)
                if word[len(word)-1] == "." or word[len(word)-1] == ","  or word[len(word)-1] == ":"  or word[len(word)-1] == ";"  or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]":
                    word = word[0:len(word)-1]
                if (len(word) == self.lengthOfAcrossClues[clue]) and (word.upper() not in newDomain): #if word lenght is valid
                    newDomain.append(word.upper())
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfAcrossClues[clue]) and (prevPlusCur != word) and (prevPlusCur.upper() not in newDomain): #if two words next to each others total length is valid
                    newDomain.append(prevPlusCur.upper())
                previousWord = word
                if (len(word) == self.lengthOfAcrossClues[clue]+1) and (word[self.lengthOfAcrossClues[clue]] == "s") and (word[0:self.lengthOfAcrossClues[clue]].upper() not in newDomain): #if the word ends with "s"
                    newDomain.append(word[0:self.lengthOfAcrossClues[clue]].upper())
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfAcrossClues[clue]) and (word[0:word.index("'")] not in newDomain):
                    newDomain.append(word[0:word.index("'")].upper())
            for word in self.initialDomains["across"][clue].split("'"):
                if (len(word) == self.lengthOfAcrossClues[clue]) and (word.upper() not in newDomain): #if word lenght is valid
                    newDomain.append(word.upper())
            for word in reversed(newDomain):
                deleted = False
                for letter in word:
                    if not letter in list(string.ascii_uppercase) and not deleted:
                        newDomain.remove(word)
                        deleted = True       
            newDomain = sorted(newDomain, key=str.lower)     
            #self.acrossClueDomains[clue] = newDomain
            self.filteredDomains["across"][clue] = copy.deepcopy(newDomain)
            newDomain = []

            
    def filterHelper(self, input):
        if input == "0":
            return "ZERO"
        if input == "1":
            return "ONE"
        if input == "2":
            return "TWO"
        if input == "3":
            return "THREE"
        if input == "4":
            return "FOUR"
        if input == "5":
            return "FIVE"
        if input == "6":
            return "SIX"
        if input == "7":
            return "SEVEN"
        if input == "8":
            return "EIGHT"
        if input == "9":
            return "NINE"
        if input == "10":
            return "TEN"
        if input == "-":
            return "MINUS"
        if input == "+":
            return "PLUS"
        return input

    def getTheRelatedDomainOfThisCell(self, row, col, option):
        domains = {}
        #down
        for location in self.locationOfDownClues:
            wordIndex = -1
            tempCol = self.locationOfDownClues[location]["start"]["col"]
            rowStart = self.locationOfDownClues[location]["start"]["row"]
            rowEnd = self.locationOfDownClues[location]["end"]["row"]
            if (row <= int(rowEnd)) and (row >= int(rowStart)) and (col == int(tempCol)):
                wordIndex = row-rowStart
                if option == "best":
                    domains["down"] = {"index": wordIndex, "domain": self.bestSolution["down"][location], "loc": self.locationOfDownClues[location]}
                else:
                    domains["down"] = {"index": wordIndex, "domain": self.tempDomains["down"][location], "loc": self.locationOfDownClues[location]}
        #across
        for location in self.locationOfAcrossClues:
            wordIndex = -1
            tempRow = self.locationOfAcrossClues[location]["start"]["row"]
            colStart = self.locationOfAcrossClues[location]["start"]["col"]
            colEnd = self.locationOfAcrossClues[location]["end"]["col"]
            if (col <= int(colEnd)) and (col >= int(colStart)) and (row == int(tempRow)):
                wordIndex = col-colStart
                if option == "best":
                    domains["across"] = {"index": wordIndex, "domain": self.bestSolution["across"][location], "loc": self.locationOfAcrossClues[location]}
                else:
                    domains["across"] = {"index": wordIndex, "domain": self.tempDomains["across"][location], "loc": self.locationOfAcrossClues[location]}
        return domains

    def solvePuzzle(self):
        puzzleNotSolved = True
        #while puzzle is solved try more jokers
        while puzzleNotSolved:
            puzzleNotSolved = False
            
            self.tempDomains = copy.deepcopy(self.filteredDomains)
            
            if self.changeNeglected():
                changeMade = True
                #Constraints
                while changeMade:
                    if self.count < 2:
                        print("changeMAde")
                        changeMade = False
                        for row in range(0,5):
                            if row not in self.neglectedWords["row"]: #--------------------
                                for col in range(0,5):
                                    if col not in self.neglectedWords["col"]: #--------------------
                                        if self.getTheRelatedDomainOfThisCell(row,col,"") != {}:
                                            domains = self.getTheRelatedDomainOfThisCell(row,col,"")
                                            if self.count < 2:
                                                print(domains)
                                                
                                                for downWord in domains["down"]["domain"]:
                                                    matched = False
                                                    for acrossWord in domains["across"]["domain"]:
                                                        if downWord[domains["down"]["index"]] == acrossWord[domains["across"]["index"]]:
                                                            matched = True
                                                    if matched == False:
                                                        domains["down"]["domain"].remove(downWord)
                                                        print(downWord)
                                                        changeMade = True

                                                for acrossWord in domains["across"]["domain"]:
                                                    matched = False
                                                    for downWord in domains["down"]["domain"]:
                                                        if downWord[domains["down"]["index"]] == acrossWord[domains["across"]["index"]]:
                                                            matched = True
                                                    if matched == False:
                                                        domains["across"]["domain"].remove(acrossWord)
                                                        print(acrossWord)
                                                        changeMade = True
                                                input(self.count)
                self.isItTheBestSolution()
                if self.count < 2:
                    self.printDomains()
                    print("\n\n------------------\n")
                puzzleNotSolved = not self.isPuzzleSolved()

            else: 
                return False
                
    def getAnswerGrid(self):
        answerGrid = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
        for row in range(0,5):
            for col in range(0,5):
                if answerGrid[row][col] == "":
                    domains = self.getTheRelatedDomainOfThisCell(row,col,"best")
                    if domains == {}:
                        answerGrid[row][col] = "-"
                    else:
                        if len(domains["across"]["domain"]) == 1:
                            for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0])):
                                answerGrid[row][colIndex] = domains["across"]["domain"][0][colIndex - domains["across"]["loc"]["start"]["col"]]                            
                        if len(domains["down"]["domain"]) == 1:
                            for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0])):
                                answerGrid[rowIndex][col] = domains["down"]["domain"][0][rowIndex - domains["down"]["loc"]["start"]["row"]]
        for row in range(0,5):
            for col in range(0,5):
                if answerGrid[row][col] == "":
                    answerGrid[row][col] = "*"
        for row in answerGrid:
            print(row)
        self.solvedPuzzle = answerGrid

    def isPuzzleSolved(self):
        answerGrid = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
        puzzleSolved = True
        for row in range(0,5):
            for col in range(0,5):
                if answerGrid[row][col] == "":
                    domains = self.getTheRelatedDomainOfThisCell(row,col,"")
                    if domains == {}:
                        answerGrid[row][col] = "-"
                    else:
                        if len(domains["across"]["domain"]) == 1:
                            for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0])):
                                answerGrid[row][colIndex] = domains["across"]["domain"][0][colIndex - domains["across"]["loc"]["start"]["col"]]                            
                        if len(domains["down"]["domain"]) == 1:
                            for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0])):
                                answerGrid[rowIndex][col] = domains["down"]["domain"][0][rowIndex - domains["down"]["loc"]["start"]["row"]]
        for row in range(0,5):
            for col in range(0,5):
                if answerGrid[row][col] == "":
                    puzzleSolved = False
        return puzzleSolved

    def printDomains(self):
        print("\n Domain of down clues")
        for i in self.tempDomains["down"]:
            print(i, self.tempDomains["down"][i])

        print("\n Domain of across clues")
        for i in self.tempDomains["across"]:
            print(i, self.tempDomains["across"][i])
    
    def printBestDomains(self):
        print("\n Domain of down clues")
        for i in self.bestSolution["down"]:
            print(i, self.bestSolution["down"][i])

        print("\n Domain of across clues")
        for i in self.bestSolution["across"]:
            print(i, self.bestSolution["across"][i])

    def changeNeglected(self):
        if self.count == 0:
            rows = [0,1,2,3,4]
            for r in range(0, len(rows)+1):
                for rsubset in itertools.combinations(rows, r):
                    cols = [0,1,2,3,4]
                    for c in range(0, len(cols)+1):
                        for csubset in itertools.combinations(cols, c):
                            self.neglectedWordsArray.append({"row": rsubset, "col": csubset})
            self.neglectedWords = self.neglectedWordsArray[self.count]
            self.count = self.count + 1
            return True
        else:
            #print(self.neglectedWords)
            if self.count == 1024:
                return False
            self.neglectedWords = self.neglectedWordsArray[self.count]
            self.count = self.count + 1
            return True
    
    def isItTheBestSolution(self):
        count = 0
        for down in self.tempDomains["down"]:
            if len(self.tempDomains["down"][down]) == 1:
                count = count + 1
        for across in self.tempDomains["across"]:
            if len(self.tempDomains["across"][across]) == 1:
                count = count + 1
        if count > self.bestSolution["find"]:
            for down in self.tempDomains["down"]:
                self.bestSolution["down"][down] =  self.tempDomains["down"][down]
            for across in self.tempDomains["across"]:
                self.bestSolution["across"][across] =  self.tempDomains["across"][across]
            self.bestSolution["find"] = count
"""
grid = [["1","0","0","0","0"],["1","0","0","0","0"],["0","0","0","0","0"],["0","0","0","0","1"],["0","0","0","0","1"]]
numbers = [["-","1","2","3","4"],["-","5","-","-","-"],["6","-","-","-","-"],["7","-","-","-","-"],["8","-","-","-","-"]]
downClues = [['1', 'Partially melted snow'],['2', 'New employee'],['3', 'Result of a successful job interview'],['4', 'Director Anderson'],['6', '[not my mistake]']]
acrossClues = [['1', '"Brooklyn Nine-Nine" or "The King of Queens"'],['5', '"What happens to us while we are making other plans," per Allen Saunders'],['6', 'Enjoys Santa Monica, perhaps'],['7', '"It\'s all clear now"'],['8', 'Singer nicknamed the "Goddess of Pop"']]

solver = CrosswordSolver(grid, numbers, downClues, acrossClues)

solver.printDomains()

print("\n Location of down clues")

for down in solver.locationOfDownClues:
    print(down, "start: ", solver.locationOfDownClues[down]["start"], "end: ", solver.locationOfDownClues[down]["end"])

print("\n Location of across clues")

for across in solver.locationOfAcrossClues:
    print(across, "start: ", solver.locationOfAcrossClues[across]["start"], "end: ", solver.locationOfAcrossClues[across]["end"])

print("")

print("SOLVE PUZZLE")
solver.solvePuzzle()

solver.printBestDomains()

print("")
solver.getAnswerGrid()
"""
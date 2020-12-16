import itertools
import copy
from json import decoder
import string
import json

class Word:
    def __init__(self,word,type,rowColIndex,clueIndex,active,cells):
        self.word = word
        self.type = type
        self.rowColIndex = rowColIndex
        self.clueIndex = clueIndex
        self.active = active
        self.cells = cells
class newSolver:
    def __init__(self, grid, numbers, downClues, acrossClues, domains):
        self.grid = grid
        self.numbers = numbers
        self.downClues = downClues
        self.acrossClues = acrossClues
        self.initialDomains = copy.deepcopy(domains) #INITIAL
        
        #with open('data.json', 'w') as fp:
         #   json.dump(domains, fp,  indent=4)
        self.lengthOfDownClues = {}
        self.lengthOfAcrossClues = {}
        
        self.locationOfDownClues = {}
        self.locationOfAcrossClues = {}

        self.filteredDomains = {"down": {}, "across": {}} #FILTERED

        self.neglectedWords = {"row": [], "col": []} 
        self.neglectedWordsArray = []
        
        self.count = 0

        self.bestSolution = {"across": [[],[],[],[],[]], "down": [[],[],[],[],[]], "find":0}

        self.solvedPuzzle = []

        self.possibleGrids = []
    
        
        self.idealGrids = []
    
        self.domains = {"across": [[],[],[],[],[]], "down": [[],[],[],[],[]]}

        self.cells = [[{"across": {}, "down":{}},{"across": {}, "down":{}},{"across": {}, "down":{}},{"across": {}, "down":{}},{"across": {}, "down":{}}] for r in range(5)]

        

        self.setup()
        self.printDomainLen()
        input("GO")
        self.dfs(0, None)
        
        for grid in self.idealGrids:
            self.printGrid(grid["grid"])
            print("")

        self.advanceGrids()
        
        #with open('filteredDomains.json', 'w') as fp:
       #   json.dump(self.domains, fp,  indent=4)
       
        #self.tempDomains = copy.deepcopy(self.domains) #TEMP
        #self.tempCells = copy.deepcopy(self.cells)
        """
        grid =  [["D", "O", "F", "F", "S"], ["", "", "", "", ""],["", "", "", "", ""], ["", "", "E", "", ""], ["", "", "", "", ""]]
        lastAdded = [(0,0),(0,1),(0,2),(0,3),(0,4)]
        emptyCells = [(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4),(3,0),(3,1),(3,3),(3,4),(4,0),(4,1),(4,2),(4,3),(4,4)]
        acrossDown = "across"

        grid =  [["", "O", "", "", ""], ["", "P", "", "I", ""],["", "E", "", "", ""], ["", "R", "", "", ""], ["", "A", "", "", ""]]
        lastAdded = [(0,1),(1,1),(2,1),(3,1),(4,1)]
        emptyCells = [(0,0),(0,2),(0,3),(0,4),(1,0),(1,2),(1,4),(2,0),(2,2),(2,3),(2,4),(3,0),(3,2),(3,3),(3,4),(4,0),(4,2),(4,3),(4,4)]
        #emptyCells = [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,2),(2,3),(2,4),(3,0),(3,1),(3,2),(3,3),(3,4),(4,0),(4,1),(4,2),(4,3),(4,4)]
        acrossDown = "down"
        pos = self.getPossibleGrids(grid,lastAdded,emptyCells,acrossDown)    
        tos = self.getPossibleGrids(pos[0]["grid"],pos[0]["lastAdded"],pos[0]["emptyCells"],pos[0]["acrossDown"])
        kos = self.getPossibleGrids(tos[0]["grid"],tos[0]["lastAdded"],tos[0]["emptyCells"],tos[0]["acrossDown"])
        
        init = self.getInitialGrids()
        sec = self.getPossibleGrids(init[1]["grid"],init[0]["lastAdded"],init[0]["emptyCells"],init[0]["acrossDown"])
        self.printGrid(init[0]["grid"])
        self.printGrid(sec[1]["grid"])
        
        self.printGrid(pos[0]["grid"])
        self.printGrid(tos[0]["grid"])
        self.printGrid(kos[2]["grid"])
        
        """
    def printGrid(self,grid):
        for i in grid:
            print(i)
    
    def setup(self):
        self.wordLengthCalculator()    
        self.filterDomains()
        self.deleteDups()
        self.setDomains()
        self.setCells()


    def setDomains(self):
        for i in range(0,5):
            for across in self.filteredDomains["across"]:
                if self.locationOfAcrossClues[across]["start"]["row"] == i:
                    for word in self.filteredDomains["across"][across]:
                        self.domains["across"][i].append(word)
        for i in range(0,5):
            for down in self.filteredDomains["down"]:
                if self.locationOfDownClues[down]["start"]["col"] == i:
                    for word in self.filteredDomains["down"][down]:
                        self.domains["down"][i].append(word)
        

    def reset(self):
        for index in range(0,5):
            for word in self.domains["across"][index]:
                word.active = True
            for word in self.domains["down"][index]:
                word.active = True

    def setCells(self):
        for row in range(0,5):
            for col in range(0,5):
                for letter in string.ascii_uppercase:
                    self.cells[row][col]["across"][letter] = []
                    self.cells[row][col]["down"][letter] = []

        for row in range(0,5):
            for col in range(0,5):
                for letter in string.ascii_uppercase:
                    if self.getTheRelatedDomainOfThisCell(row,col,"") != {}:
                        for word in self.getTheRelatedDomainOfThisCell(row,col,"")["across"]["domain"]:
                            if letter == word.word[self.getTheRelatedDomainOfThisCell(row,col,"")["across"]["index"]]:
                                self.cells[row][col]["across"][letter].append(word)
                        for word in self.getTheRelatedDomainOfThisCell(row,col,"")["down"]["domain"]:
                            if letter == word.word[self.getTheRelatedDomainOfThisCell(row,col,"")["down"]["index"]]:
                                self.cells[row][col]["down"][letter].append(word)

    
    def getTrueFalse(self, row, col, acrossDown, letter):
        for word in self.cells[row][col][acrossDown][letter]:
            if word.active:
                return True
        return False

    def getCurrentWords(self, row, col, acrossDown, letter):
        words = []
        for word in self.cells[row][col][acrossDown][letter]:
            if word.active:
                words.append(word)
        return words



    def printDomainss(self):
        print("Across")
        for col in range(0,5):
            print(str(col) + ": ", end=" ")
            for word in self.domains["across"][col]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

        print("\nDown")
        for row in range(0,5):
            print(str(row) + ": ", end=" ")
            for word in self.domains["down"][row]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

    def printDomainLen(self):
        print("Across")
        for col in range(0,5):
            count = 0
            for word in self.domains["across"][col]:
                if word.active:
                    count += 1
            print(str(col) + ": " + str(count))

        print("\nDown")
        for row in range(0,5):
            count = 0
            for word in self.domains["down"][row]:
                if word.active:
                    count += 1
            print(str(row) + ": " + str(count))


    def printCells(self):
        for row in range(0,5):
            for col in range(0,5):
                print(str(row) + ", " + str(col) + ": ")
                print("Across: ", end="")
                for letter in self.cells[row][col]["across"]:
                    if len(self.cells[row][col]["down"][letter]) > 0:
                        print(letter, end=": ")
                        for word in self.cells[row][col]["across"][letter]:
                            print(word.word, end=", ")
                        print("//", end="")
                print()
                print("Down: ", end="")
                for letter in self.cells[row][col]["down"]:
                    if len(self.cells[row][col]["down"][letter]) > 0:
                        print(letter, end=": ")
                        for word in self.cells[row][col]["down"][letter]:
                            print(word.word, end=", ")
                        print("//", end="")
                print()

    def getCells(self, clue, acrossDown):
        cells = []
        if acrossDown == "across":
            for col in range(self.locationOfAcrossClues[clue]["start"]["col"], self.lengthOfAcrossClues[clue]):
                cells.append((self.locationOfAcrossClues[clue]["start"]["row"],col))
        else:
            for row in range(self.locationOfDownClues[clue]["start"]["row"], self.lengthOfDownClues[clue]):
                cells.append((row,self.locationOfDownClues[clue]["start"]["col"]))
        return cells

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
 
    def filterDomains(self):
        #downClues
        newDomain = set()
        for clue in self.initialDomains["down"]:
            previousWord = ""
            for word in self.initialDomains["down"][clue].split():
                word = self.filterHelper(word)
                if word[len(word)-1] == "." or word[len(word)-1] == ","  or word[len(word)-1] == ":"  or word[len(word)-1] == ";"  or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]" :
                    word = word[0:len(word)-1]
                if (len(word) == self.lengthOfDownClues[clue]) and not self.checkDuplicates( clue, "down", word.upper()): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"down", -1, clue,True,self.getCells(clue,"down")))
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfDownClues[clue]) and (prevPlusCur != word) and not self.checkDuplicates( clue, "down", prevPlusCur.upper()): #if two words next to each others total length is valid
                    newDomain.add(Word(prevPlusCur.upper(),"down", -1, clue,True,self.getCells(clue,"down")))
                previousWord = word
                if (len(word) == self.lengthOfDownClues[clue]+1) and (word[self.lengthOfDownClues[clue]] == "s") and not self.checkDuplicates( clue, "down", word[0:self.lengthOfDownClues[clue]].upper()): #if the word ends with "s"
                    newDomain.add(Word(word[0:self.lengthOfDownClues[clue]].upper(),"down", -1, clue,True,self.getCells(clue,"down")))
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfDownClues[clue]) and not self.checkDuplicates(clue, "down",word[0:word.index("'")].upper()):
                    newDomain.add(Word(word[0:word.index("'")].upper(),"down", -1, clue,True,self.getCells(clue,"down")))
            for word in self.initialDomains["down"][clue].split("'"):
                if (len(word) == self.lengthOfDownClues[clue]) and not self.checkDuplicates( clue, "down", word.upper()): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"down", -1, clue,True,self.getCells(clue,"down")))
            newDomain = list(newDomain)
            for word in reversed(newDomain):
                deleted = False
                for letter in word.word:
                    if not letter in list(string.ascii_uppercase) and not deleted:
                        newDomain.remove(word)
                        deleted = True       
            def lexical(word):
                return word.word[0]   
            newDomain.sort(key=lexical)     
            #self.downClueDomains[clue] = newDomain.copy()
            self.filteredDomains["down"][clue] = copy.deepcopy(newDomain)
            newDomain = set()

        #acrossClues
        newDomain = set()
        for clue in self.lengthOfAcrossClues:
            previousWord = ""
            for word in self.initialDomains["across"][clue].split():
                word = self.filterHelper(word)
                if word[len(word)-1] == "." or word[len(word)-1] == ","  or word[len(word)-1] == ":"  or word[len(word)-1] == ";"  or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]" :
                    word = word[0:len(word)-1]
                if (len(word) == self.lengthOfAcrossClues[clue]) and not self.checkDuplicates( clue, "across", word.upper()): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"across", -1, clue,True,self.getCells(clue,"across")))
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfAcrossClues[clue]) and (prevPlusCur != word) and not self.checkDuplicates( clue, "across", prevPlusCur.upper()): #if two words next to each others total length is valid
                    newDomain.add(Word(prevPlusCur.upper(),"across", -1, clue,True,self.getCells(clue,"across")))
                previousWord = word
                if (len(word) == self.lengthOfAcrossClues[clue]+1) and (word[self.lengthOfAcrossClues[clue]] == "s") and not self.checkDuplicates( clue, "across", word[0:self.lengthOfAcrossClues[clue]].upper()): #if the word ends with "s"
                    newDomain.add(Word(word[0:self.lengthOfAcrossClues[clue]].upper(),"across", -1, clue,True,self.getCells(clue,"across")))
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfAcrossClues[clue]) and not self.checkDuplicates( clue, "across", word[0:word.index("'")].upper()):
                    newDomain.add(Word(word[0:word.index("'")].upper(),"across", -1, clue,True,self.getCells(clue,"across")))
            for word in self.initialDomains["across"][clue].split("'"):
                if (len(word) == self.lengthOfAcrossClues[clue]) and not self.checkDuplicates( clue, "across", word.upper()): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"across", -1, clue,True,self.getCells(clue,"across")))
            newDomain = list(newDomain)
            for word in reversed(newDomain):
                deleted = False
                for letter in word.word:
                    if not letter in list(string.ascii_uppercase) and not deleted:
                        newDomain.remove(word)
                        deleted = True    
            def lexical(word):
                return word.word[0]   
            newDomain.sort(key=lexical)     
            #self.acrossClueDomains[clue] = newDomain
            self.filteredDomains["across"][clue] = copy.deepcopy(newDomain)
            newDomain = set()

    def getExactLocation(self, numberIndex):
        for row in range(0,5):
            for col in range(0,5):
                if str(numberIndex) == self.numbers[row][col]:
                    return (row,col)


    def checkDuplicates(self, clueIndex, acrossDown, wordToCompare):
        if clueIndex in self.filteredDomains[acrossDown]:
            for word in self.filteredDomains[acrossDown][clueIndex]:
                if wordToCompare == word.word:
                    return True
        return False    

    def deleteDups(self):
        for key in self.filteredDomains["across"]:
            for word in self.filteredDomains["across"][key]:
                wordToCheck = word.word
                wordCount = 0
                for wordIn in reversed(self.filteredDomains["across"][key]):
                    if wordToCheck == wordIn.word:
                        wordCount += 1
                        if wordCount > 1:
                            self.filteredDomains["across"][key].remove(wordIn)

        for key in self.filteredDomains["down"]:
            for word in self.filteredDomains["down"][key]:
                wordToCheck = word.word
                wordCount = 0
                for wordIn in reversed(self.filteredDomains["down"][key]):
                    if wordToCheck == wordIn.word:
                        wordCount += 1
                        if wordCount > 1:
                            self.filteredDomains["down"][key].remove(wordIn)



            
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
                    domains["down"] = {"index": wordIndex, "domain": self.getCurrentDomainWord("down",tempCol), "loc": self.locationOfDownClues[location]}
                else:
                    domains["down"] = {"index": wordIndex, "domain": self.filteredDomains["down"][location], "loc": self.locationOfDownClues[location]}
        #across
        for location in self.locationOfAcrossClues:
            wordIndex = -1
            tempRow = self.locationOfAcrossClues[location]["start"]["row"]
            colStart = self.locationOfAcrossClues[location]["start"]["col"]
            colEnd = self.locationOfAcrossClues[location]["end"]["col"]
            if (col <= int(colEnd)) and (col >= int(colStart)) and (row == int(tempRow)):
                wordIndex = col-colStart
                if option == "best":
                    domains["across"] = {"index": wordIndex, "domain": self.getCurrentDomainWord("across",tempRow), "loc": self.locationOfAcrossClues[location]}
                else:
                    domains["across"] = {"index": wordIndex, "domain": self.filteredDomains["across"][location], "loc": self.locationOfAcrossClues[location]}
        return domains

   
    def getCurrentDomainWord(self, acrossDown, index):
        words = []
        for word in self.bestSolution[acrossDown][index]:
            if word.active:
                words.append(word)
        return words
    
    def getAnswerGrid(self):
        if self.bestSolution["find"] != 0:
            answerGrid = [["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
            for row in range(0,5):
                for col in range(0,5):
                    if answerGrid[row][col] == "":
                        domains = self.getTheRelatedDomainOfThisCell(row,col,"best")
                        if domains == {}:
                            answerGrid[row][col] = "-"
                        else:
                            if len(self.getCurrentDomainWord("across", row)) == 1:
                                for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0].word)):
                                    answerGrid[row][colIndex] = domains["across"]["domain"][0].word[colIndex - domains["across"]["loc"]["start"]["col"]]  
                            if len(self.getCurrentDomainWord("down", col)) == 1:
                                for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0].word)):
                                    answerGrid[rowIndex][col] = domains["down"]["domain"][0].word[rowIndex - domains["down"]["loc"]["start"]["row"]]

                            
            for row in range(0,5):
                for col in range(0,5):
                    if answerGrid[row][col] == "":
                        answerGrid[row][col] = "*"
            for row in answerGrid:
                print(row)
            self.solvedPuzzle = answerGrid
        else:
            print(" CORT ")

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
                        if len(self.getCurrentDomainWord("across", row)) == 1:
                            for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0].word)):
                                answerGrid[row][colIndex] = domains["across"]["domain"][0].word[colIndex - domains["across"]["loc"]["start"]["col"]]                            
                        if len(self.getCurrentDomainWord("down", col)) == 1:
                            for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0].word)):
                                answerGrid[rowIndex][col] = domains["down"]["domain"][0].word[rowIndex - domains["down"]["loc"]["start"]["row"]]
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
        print("Across")
        for col in range(0,5):
            print(str(col) + ": ", end=" ")
            for word in self.bestSolution["across"][col]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

        print("\nDown")
        for row in range(0,5):
            print(str(row) + ": ", end=" ")
            for word in self.bestSolution["down"][row]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

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
            print(self.neglectedWords)
            if self.count == 1024:
                return False
            self.neglectedWords = self.neglectedWordsArray[self.count]
            self.count = self.count + 1
            return True
    
    def isItTheBestSolution(self):
        count = 0
        for row in range(0,5):
            wordCount = 0
            for word in self.domains["across"][row]:
                if word.active:
                    wordCount += 1
            if wordCount == 1:
                count += 1
        for col in range(0,5):
            wordCount = 0
            for word in self.domains["down"][col]:
                if word.active:
                    wordCount += 1
            if wordCount == 1:
                count += 1

        if count > self.bestSolution["find"]:
            for row in range(0,5):
                self.bestSolution["across"][row] =  copy.deepcopy(self.domains["across"][row])
            for col in range(0,5):
                self.bestSolution["down"][col] =  copy.deepcopy(self.domains["down"][col])
            self.bestSolution["find"] = count


    
    def getPossibleGrids(self, grid, lastAdded, emptyCells, accrossDown): 
        possibleGrids = []
        for cell in lastAdded:
            possibleWords = []
            if accrossDown == "across":
                possibleWords = self.cells[ cell[0] ] [cell[1] ]["down"][grid[ cell[0] ] [cell[1] ]]
            else:
                possibleWords = self.cells[cell[0]][cell[1]]["across"][grid[ cell[0] ] [cell[1] ]]
            intersectedCells = []
            if len(possibleWords) > 0:
                for incell in possibleWords[0].cells:
                    if incell not in emptyCells and incell != (cell[0], cell[1]):
                        intersectedCells.append(incell)
            if len(intersectedCells) > 0:
                for intersectedCell in intersectedCells:
                    if accrossDown == "across":
                        intersectedWords = self.cells[ intersectedCell[0] ][ intersectedCell[1] ]["down"][grid[ intersectedCell[0] ] [intersectedCell[1] ]]
                    else:
                        intersectedWords = self.cells[ intersectedCell[0] ][ intersectedCell[1] ]["across"][grid[ intersectedCell[0] ] [intersectedCell[1] ]]
                    for word in reversed(possibleWords):
                        if word not in intersectedWords:
                            possibleWords.remove(word)

            tempEmptyCell = copy.deepcopy(emptyCells)
            for word in possibleWords:
                for filledCell in word.cells:
                    if filledCell in tempEmptyCell:
                        tempEmptyCell.remove(filledCell)
                if accrossDown == "across":
                    newGrid = {"grid":self.gridWordAdder(copy.deepcopy(grid), word.word, word.cells), "lastAdded": word.cells, "emptyCells": copy.deepcopy(tempEmptyCell) , "acrossDown": "down" }
                else:
                    newGrid = {"grid":self.gridWordAdder(copy.deepcopy(grid), word.word, word.cells), "lastAdded": word.cells, "emptyCells": copy.deepcopy(tempEmptyCell) , "acrossDown": "across" }
                if grid != newGrid["grid"] and newGrid["grid"] not in self.possibleGrids:
                    possibleGrids.append(newGrid)
                    self.possibleGrids.append(newGrid["grid"])
            
        return possibleGrids

    def getInitialGrids(self):
        possibleGrids = []
        emptyCells = []
        grid = copy.deepcopy(self.grid)
        for i in range(0,5):
            for j in range(0,5):
                if grid[i][j] == "1":
                    grid[i][j] = "-"
                else:
                    grid[i][j] = ""
                    emptyCells.append((i,j))
        
        for row in range(0,5):
            tempEmptyCell = copy.deepcopy(emptyCells)
            for word in self.domains["across"][row]:
                for filledCell in word.cells:
                    if filledCell in tempEmptyCell:
                        tempEmptyCell.remove(filledCell)
                possibleGrids.append({"grid":self.gridWordAdder(copy.deepcopy(grid), word.word, word.cells), "lastAdded": word.cells, "emptyCells": copy.deepcopy(tempEmptyCell) , "acrossDown": "across" })

        for col in range(0,5):
            tempEmptyCell = copy.deepcopy(emptyCells)
            for word in self.domains["down"][col]:
                for filledCell in word.cells:
                    if filledCell in tempEmptyCell:
                        tempEmptyCell.remove(filledCell)
                possibleGrids.append({"grid":self.gridWordAdder(copy.deepcopy(grid), word.word, word.cells), "lastAdded": word.cells, "emptyCells": copy.deepcopy(tempEmptyCell) , "acrossDown": "down" })
            
        return possibleGrids



    def gridWordAdder(self, grid, word, cellsToAdd):
        i = 0
        for cell in cellsToAdd:
            grid[cell[0]][cell[1]] = word[i]
            i += 1
        return grid


    def getEmptyCells(self, grid, cellsToControl):
        intersectedCells = []
        for cell in cellsToControl:
            if grid[cell[0]][cell[1]] != "":
                intersectedCells.append(cell)
        return intersectedCells

    def dfs(self, level, grid):
        
        if level > 4 :
            self.isGridIdeal(grid)
            
        

        possibleGrids = []
        if level == 0:
            possibleGrids = self.getInitialGrids()
        else:
            possibleGrids = self.getPossibleGrids(grid["grid"], grid["lastAdded"], grid["emptyCells"], grid["acrossDown"])
        
        for grid in possibleGrids:
            self.dfs(level+1, grid)

    def isGridSolved(self, grid):
        count = 0
        for i in range(0,5):
            for j in range(0,5):
                if grid["grid"][i][j] != "":
                    count += 1
        if count == 25:
            return True
        return False
    def isGridSolvedRaw(self, grid):
            count = 0
            for i in range(0,5):
                for j in range(0,5):
                    if grid[i][j] != "":
                        count += 1
            if count == 25:
                return True
            return False

    def isGridIdeal(self, grid):
        count = 0
        for i in range(0,5):
            for j in range(0,5):
                if grid["grid"][i][j] != "":
                    count += 1
        if count > 20:
            self.idealGrids.append(grid)
        return False
    """
    def advanceGrids(self):
        for grid in self.idealGrids:
            for row in range(0,5):
                for col in range(0,5):
                    if grid["grid"][row][col] == "":
                        for letter in string.ascii_uppercase:
    """               



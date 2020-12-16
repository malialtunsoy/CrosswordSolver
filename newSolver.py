import itertools
import copy
import string
import json

class Word:
    def __init__(self,word,type,rowColIndex,clueIndex,active):
        self.word = word
        self.type = type
        self.rowColIndex = rowColIndex
        self.clueIndex = clueIndex
        self.active = active

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

        self.neglectedWords = {"row": [], "col": []} 
        self.neglectedWordsArray = []
        self.count = 0

        self.bestSolution = {"down": {}, "across": {}, "find": 0}

        self.solvedPuzzle = []
    
        self.filteredDomains = {"down": {}, "across": {}} #FILTERED

    
        self.domains = {"across": [[],[],[],[],[]], "down": [[],[],[],[],[]]}

        self.cells = [[{"across": {}, "down":{}},{"across": {}, "down":{}},{"across": {}, "down":{}},{"across": {}, "down":{}},{"across": {}, "down":{}}] for r in range(5)]



        self.setup()
        #with open('filteredDomains.json', 'w') as fp:
         #   json.dump(self.filteredDomains, fp,  indent=4)
       
        #self.tempDomains = copy.deepcopy(self.domains) #TEMP
        #self.tempCells = copy.deepcopy(self.cells)
        self.solver()
        """
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
        """
        
    
    def setup(self):
        self.wordLengthCalculator()    
        self.filterDomains()
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

    def solver(self):
        puzzleNotSolved = True
        #while puzzle is solved try more jokers
        while puzzleNotSolved:
            puzzleNotSolved = False
            
            self.printDomainLen()
            self.printDomainss()
            
            if self.changeNeglected():
                changeMade = True
                #Constraints
                #self.printTempDomains()
                input("go")
                while changeMade:
                    changeMade = False
                    #Single Cell
                    for row in range(0,5):
                        #if row not in self.neglectedWords["row"]: #--------------------
                        for col in range(0,5):
                            #if col not in self.neglectedWords["col"]: #--------------------
                            for letter in string.ascii_uppercase:
                                #if len(self.cells[row][col]["across"][letter]) > 0 and len(self.cells[row][col]["down"][letter]) > 0:
                                    #   continue
                                if self.getTrueFalse(row, col, "across", letter) and not self.getTrueFalse(row, col, "down", letter):
                                    for word in self.cells[row][col]["across"][letter]:
                                        word.active = False
                                    changeMade = True
                                
                                elif not self.getTrueFalse(row, col, "across", letter) and self.getTrueFalse(row, col, "down", letter):
                                    for word in self.cells[row][col]["down"][letter]:
                                        word.active = False
                                    changeMade = True
                    #Quadra Cell
                    for row in range(0,4):
                        for col in range(0,4):
                            mathced = False
                            matchedTopLeft = []
                            matchedTopRight = []
                            matchedBottomLeft = []
                            matchedBottomRight = []
                            for TopLeft in string.ascii_uppercase:
                                for TopRight in string.ascii_uppercase:
                                    for BottomLeft in string.ascii_uppercase:
                                        for BottomRight in string.ascii_uppercase:
                                            
                                            if any(word in self.cells[row][col]["across"][TopLeft] for word in self.cells[row][col+1]["across"][TopRight]):
                                                if any(word in self.cells[row+1][col]["across"][BottomLeft] for word in self.cells[row+1][col+1]["across"][BottomRight]):
                                                    if any(word in self.cells[row][col]["down"][TopLeft] for word in self.cells[row+1][col]["down"][BottomLeft]):
                                                        if any(word in self.cells[row][col+1]["down"][TopRight] for word in self.cells[row+1][col+1]["down"][BottomRight]):
                                                            mathced = True
                                                            matchedTopLeft.append(TopLeft)
                                                            matchedTopRight.append(TopRight)
                                                            matchedBottomLeft.append(BottomLeft)
                                                            matchedBottomRight.append(BottomRight)
                            for letter in string.ascii_uppercase:
                                if letter not in matchedTopLeft:
                                    for word in self.cells[row][col]["across"][letter]:
                                        word.active = False
                                    for word in self.cells[row][col]["down"][letter]:
                                        word.active = False
                                if letter not in matchedBottomRight:
                                    for word in self.cells[row+1][col+1]["across"][letter]:
                                        word.active = False
                                    for word in self.cells[row+1][col+1]["down"][letter]:
                                        word.active = False
                                
                                

                self.printDomainLen()
                self.printDomainss()
                input("done")                        
                                            
                self.isItTheBestSolution()
                """
                if self.count < 2:
                    self.printDomains()
                    print("\n\n------------------\n")
                """
                puzzleNotSolved = not self.isPuzzleSolved()
                print(self.tempDomains)
                input(self.neglectedWords)

                #with open('row1neglect.json', 'w') as fp:
                #    json.dump(self.tempDomains, fp,  indent=4)
            else: 
                return False



    def getTrueFalse(self, row, col, acrossDown, letter):
        for word in self.cells[row][col][acrossDown][letter]:
            if word.active:
                return True
        return False



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

        """
        for i in self.filteredDomains["across"]:
            print(i, end=": ")
            for j in self.filteredDomains["across"][i]:
                print(j.word, end=" ")
            print("\n\n")

        for i in self.filteredDomains["down"]:
            print(i, end=": ")
            for j in self.filteredDomains["down"][i]:
                print(j.word, end=" ")
            print("\n\n")
        """


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
                if word[len(word)-1] == "." or word[len(word)-1] == ","  or word[len(word)-1] == ":"  or word[len(word)-1] == ";"  or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]":
                    word = word[0:len(word)-1]
                if (len(word) == self.lengthOfDownClues[clue]): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"down", -1, clue,True))
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfDownClues[clue]) and (prevPlusCur != word): #if two words next to each others total length is valid
                    newDomain.add(Word(prevPlusCur.upper(),"down", -1, clue,True))
                previousWord = word
                if (len(word) == self.lengthOfDownClues[clue]+1) and (word[self.lengthOfDownClues[clue]] == "s"): #if the word ends with "s"
                    newDomain.add(Word(word[0:self.lengthOfDownClues[clue]].upper(),"down", -1, clue,True))
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfDownClues[clue]):
                    newDomain.add(Word(word[0:word.index("'")].upper(),"down", -1, clue,True))
            for word in self.initialDomains["down"][clue].split("'"):
                if (len(word) == self.lengthOfDownClues[clue]): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"down", -1, clue,True))
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
                if word[len(word)-1] == "." or word[len(word)-1] == ","  or word[len(word)-1] == ":"  or word[len(word)-1] == ";"  or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]":
                    word = word[0:len(word)-1]
                if (len(word) == self.lengthOfAcrossClues[clue]): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"across", -1, clue,True))
                prevPlusCur = previousWord + word
                if (len(prevPlusCur) == self.lengthOfAcrossClues[clue]) and (prevPlusCur != word): #if two words next to each others total length is valid
                    newDomain.add(Word(prevPlusCur.upper(),"across", -1, clue,True))
                previousWord = word
                if (len(word) == self.lengthOfAcrossClues[clue]+1) and (word[self.lengthOfAcrossClues[clue]] == "s"): #if the word ends with "s"
                    newDomain.add(Word(word[0:self.lengthOfAcrossClues[clue]].upper(),"across", -1, clue,True))
                if ("'" in word) and (len( word[0:word.index("'")] ) == self.lengthOfAcrossClues[clue]):
                    newDomain.add(Word(word[0:word.index("'")].upper(),"across", -1, clue,True))
            for word in self.initialDomains["across"][clue].split("'"):
                if (len(word) == self.lengthOfAcrossClues[clue]): #if word lenght is valid
                    newDomain.add(Word(word.upper(),"across", -1, clue,True))
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
                    domains["across"] = {"index": wordIndex, "domain": self.bestSolution["across"][location], "loc": self.locationOfAcrossClues[location]}
                else:
                    domains["across"] = {"index": wordIndex, "domain": self.filteredDomains["across"][location], "loc": self.locationOfAcrossClues[location]}
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
                    changeMade = False
                    for row in range(0,5):
                        if row not in self.neglectedWords["row"]: #--------------------
                            for col in range(0,5):
                                if col not in self.neglectedWords["col"]: #--------------------
                                    if self.getTheRelatedDomainOfThisCell(row,col,"") != {}:
                                        domains = self.getTheRelatedDomainOfThisCell(row,col,"")
                                    
                                        #print(domains)
                                        for downWord in domains["down"]["domain"]:
                                            matched = False
                                            for acrossWord in domains["across"]["domain"]:
                                                if downWord[domains["down"]["index"]] == acrossWord[domains["across"]["index"]]:
                                                    matched = True
                                            if matched == False:
                                                domains["down"]["domain"].remove(downWord)
                                                #print(downWord)
                                                changeMade = True

                                        for acrossWord in domains["across"]["domain"]:
                                            matched = False
                                            for downWord in domains["down"]["domain"]:
                                                if downWord[domains["down"]["index"]] == acrossWord[domains["across"]["index"]]:
                                                    matched = True
                                            if matched == False:
                                                domains["across"]["domain"].remove(acrossWord)
                                                #print(acrossWord)
                                                changeMade = True
                                        #input(self.count)
                                            
                self.isItTheBestSolution()
                """
                if self.count < 2:
                    self.printDomains()
                    print("\n\n------------------\n")
                """
                puzzleNotSolved = not self.isPuzzleSolved()
                print(self.tempDomains)
                input(self.neglectedWords)

                #with open('row1neglect.json', 'w') as fp:
                #    json.dump(self.tempDomains, fp,  indent=4)
            else: 
                return False
                
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
            print(self.neglectedWords)
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

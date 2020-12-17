import itertools
import copy
import string
import json
from ScorePuzzle import ScorePuzzle

class Word:
    def __init__(self, word, type, rowColIndex, clueIndex, active):
        self.word = word
        self.type = type
        self.rowColIndex = rowColIndex
        self.clueIndex = clueIndex
        self.active = active


class NewSolver:
    def __init__(self, grid, numbers, downClues, acrossClues, domains):
        self.grid = grid
        self.numbers = numbers
        self.downClues = downClues
        self.acrossClues = acrossClues
        self.initialDomains = copy.deepcopy(domains)  # INITIAL

        with open('data.json', 'w') as fp:
            json.dump(domains, fp,  indent=4)

        self.lengthOfDownClues = {}
        self.lengthOfAcrossClues = {}
        self.locationOfDownClues = {}
        self.locationOfAcrossClues = {}
        self.filteredDomains = {"down": {}, "across": {}}  # FILTERED
        self.neglectedWords = {"row": [], "col": []}
        self.neglectedWordsArray = []
        self.count = 0
        self.bestSolution = {"across": [[], [], [], [], []], "down": [
            [], [], [], [], []], "find": 0}
        self.finalSolutions = []
        self.busGrids = []
        self.finalSolution = []
        self.solvedPuzzle = []
        self.domains = {"across": [[], [], [],
                                   [], []], "down": [[], [], [], [], []]}
        self.cells = [[{"across": {}, "down": {}}, {"across": {}, "down": {}}, {"across": {
        }, "down": {}}, {"across": {}, "down": {}}, {"across": {}, "down": {}}] for r in range(5)]

        self.setup()
        print("===================\nINITIAL FILTERED DOMAINS\n===================")
        self.printDomainss()
        # with open('filteredDomains.json', 'w') as fp:
       #   json.dump(self.domains, fp,  indent=4)

        # self.tempDomains = copy.deepcopy(self.domains) #TEMP
        #self.tempCells = copy.deepcopy(self.cells)
        print("===================\nFILTERING DOMAINS BY APPLYING CONSTRAINTS\n===================")
        self.solver()
        print("===================\nBEST DOMAINS FROM FILTERING\n===================")
        self.printBestDomains()
        # self.getAnswerGrid()
        print(
            "===================\nCOMPARING MULTIPLE OPTIMAL SOLUTIONS\n===================")
        print("\n")
        print("===================\nOPTIMAL GRIDS TO COMPARE\n===================")
        self.findFinalPuzzle()
        self.solvedPuzzle = self.finalSolution

        # print(self.bestSolution["find"])

    def setup(self):
        self.wordLengthCalculator()
        self.filterDomains()
        self.deleteDups()
        self.setDomains()
        self.setCells()

    def setDomains(self):
        for i in range(0, 5):
            for across in self.filteredDomains["across"]:
                if self.locationOfAcrossClues[across]["start"]["row"] == i:
                    for word in self.filteredDomains["across"][across]:
                        self.domains["across"][i].append(word)
        for i in range(0, 5):
            for down in self.filteredDomains["down"]:
                if self.locationOfDownClues[down]["start"]["col"] == i:
                    for word in self.filteredDomains["down"][down]:
                        self.domains["down"][i].append(word)

    def reset(self):
        for index in range(0, 5):
            for word in self.domains["across"][index]:
                word.active = True
            for word in self.domains["down"][index]:
                word.active = True

    def setCells(self):
        for row in range(0, 5):
            for col in range(0, 5):
                for letter in string.ascii_uppercase:
                    self.cells[row][col]["across"][letter] = []
                    self.cells[row][col]["down"][letter] = []

        for row in range(0, 5):
            for col in range(0, 5):
                for letter in string.ascii_uppercase:
                    if self.getTheRelatedDomainOfThisCell(row, col, "") != {}:
                        for word in self.getTheRelatedDomainOfThisCell(row, col, "")["across"]["domain"]:
                            if letter == word.word[self.getTheRelatedDomainOfThisCell(row, col, "")["across"]["index"]]:
                                self.cells[row][col]["across"][letter].append(
                                    word)
                        for word in self.getTheRelatedDomainOfThisCell(row, col, "")["down"]["domain"]:
                            if letter == word.word[self.getTheRelatedDomainOfThisCell(row, col, "")["down"]["index"]]:
                                self.cells[row][col]["down"][letter].append(
                                    word)

    def solver(self):
        puzzleNotSolved = True
        # while puzzle is solved try more jokers
        while puzzleNotSolved:
            puzzleNotSolved = False
            """
            self.printDomainLen()
            self.printDomainss()
            """
            self.reset()
            # print(self.neglectedWords)
            if self.changeNeglected():
                changeMade = True
                # Constraints
                # self.printTempDomains()
                # input("go")
                while changeMade:
                    changeMade = False
                    # Single Cell

                    for row in range(0, 5):
                        # --------------------
                        if row not in self.neglectedWords["row"]:
                            for col in range(0, 5):
                                # --------------------
                                if col not in self.neglectedWords["col"]:
                                    for letter in string.ascii_uppercase:
                                        # if len(self.cells[row][col]["across"][letter]) > 0 and len(self.cells[row][col]["down"][letter]) > 0:
                                        #   continue
                                        if self.getTrueFalse(row, col, "across", letter) and not self.getTrueFalse(row, col, "down", letter):
                                            for word in self.cells[row][col]["across"][letter]:
                                                word.active = False
                                            changeMade = True

                                        elif not self.getTrueFalse(row, col, "across", letter) and self.getTrueFalse(row, col, "down", letter):
                                            for word in self.cells[row][col]["down"][letter]:
                                                word.active = False
                                            changeMade = True
                self.isItTheBestSolution()

                puzzleNotSolved = not self.isPuzzleSolved()
                # input(self.neglectedWords)

                # with open('row1neglect.json', 'w') as fp:
                #    json.dump(self.tempDomains, fp,  indent=4)
            else:
                return False

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
        for col in range(0, 5):
            print(str(col) + ": ", end=" ")
            for word in self.domains["across"][col]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

        print("\nDown")
        for row in range(0, 5):
            print(str(row) + ": ", end=" ")
            for word in self.domains["down"][row]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

    def printDomainLen(self):
        print("Across")
        for col in range(0, 5):
            count = 0
            for word in self.domains["across"][col]:
                if word.active:
                    count += 1
            print(str(col) + ": " + str(count))

        print("\nDown")
        for row in range(0, 5):
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
        for row in range(0, 5):
            for col in range(0, 5):
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
        # downClues
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

            # count spaces
            wordLength = 0
            for row in self.grid[rowIndex:]:
                if row[colIndex] == "0":
                    wordLength = wordLength + 1
            self.lengthOfDownClues[clueNumber] = wordLength
            self.locationOfDownClues[clueNumber] = {"start": {
                "row": rowIndex, "col": colIndex}, "end": {"row": rowIndex+wordLength-1, "col": colIndex}}

            # acrossClues
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

            # count spaces
            wordLength = 0
            for cell in self.grid[rowIndex][colIndex:]:
                if cell == "0":
                    wordLength = wordLength + 1
            self.lengthOfAcrossClues[clueNumber] = wordLength
            self.locationOfAcrossClues[clueNumber] = {"start": {
                "row": rowIndex, "col": colIndex}, "end": {"row": rowIndex, "col": colIndex+wordLength-1}}

    def filterDomains(self):
        # downClues
        newDomain = set()
        for clue in self.initialDomains["down"]:
            previousWord = ""
            for word in self.initialDomains["down"][clue].split():
                word = self.filterHelper(word)
                if word[len(word)-1] == "." or word[len(word)-1] == "," or word[len(word)-1] == ":" or word[len(word)-1] == ";" or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]":
                    word = word[0:len(word)-1]
                # if word lenght is valid
                if (len(word) == self.lengthOfDownClues[clue]) and not self.checkDuplicates(clue, "down", word.upper()):
                    newDomain.add(Word(word.upper(), "down", -1, clue, True))
                prevPlusCur = previousWord + word
                # if two words next to each others total length is valid
                if (len(prevPlusCur) == self.lengthOfDownClues[clue]) and (prevPlusCur != word) and not self.checkDuplicates(clue, "down", prevPlusCur.upper()):
                    newDomain.add(
                        Word(prevPlusCur.upper(), "down", -1, clue, True))
                previousWord = word
                # if the word ends with "s"
                if (len(word) == self.lengthOfDownClues[clue]+1) and (word[self.lengthOfDownClues[clue]] == "s") and not self.checkDuplicates(clue, "down", word[0:self.lengthOfDownClues[clue]].upper()):
                    newDomain.add(
                        Word(word[0:self.lengthOfDownClues[clue]].upper(), "down", -1, clue, True))
                if ("'" in word) and (len(word[0:word.index("'")]) == self.lengthOfDownClues[clue]) and not self.checkDuplicates(clue, "down", word[0:word.index("'")].upper()):
                    newDomain.add(
                        Word(word[0:word.index("'")].upper(), "down", -1, clue, True))
            for word in self.initialDomains["down"][clue].split("'"):
                # if word lenght is valid
                if (len(word) == self.lengthOfDownClues[clue]) and not self.checkDuplicates(clue, "down", word.upper()):
                    newDomain.add(Word(word.upper(), "down", -1, clue, True))
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

        # acrossClues
        newDomain = set()
        for clue in self.lengthOfAcrossClues:
            previousWord = ""
            for word in self.initialDomains["across"][clue].split():
                word = self.filterHelper(word)
                if word[len(word)-1] == "." or word[len(word)-1] == "," or word[len(word)-1] == ":" or word[len(word)-1] == ";" or word[len(word)-1] == "+" or word[len(word)-1] == "?" or word[len(word)-1] == "!" or word[len(word)-1] == ")" or word[len(word)-1] == "}" or word[len(word)-1] == "]":
                    word = word[0:len(word)-1]
                # if word lenght is valid
                if (len(word) == self.lengthOfAcrossClues[clue]) and not self.checkDuplicates(clue, "across", word.upper()):
                    newDomain.add(Word(word.upper(), "across", -1, clue, True))
                prevPlusCur = previousWord + word
                # if two words next to each others total length is valid
                if (len(prevPlusCur) == self.lengthOfAcrossClues[clue]) and (prevPlusCur != word) and not self.checkDuplicates(clue, "across", prevPlusCur.upper()):
                    newDomain.add(Word(prevPlusCur.upper(),
                                       "across", -1, clue, True))
                previousWord = word
                # if the word ends with "s"
                if (len(word) == self.lengthOfAcrossClues[clue]+1) and (word[self.lengthOfAcrossClues[clue]] == "s") and not self.checkDuplicates(clue, "across", word[0:self.lengthOfAcrossClues[clue]].upper()):
                    newDomain.add(
                        Word(word[0:self.lengthOfAcrossClues[clue]].upper(), "across", -1, clue, True))
                if ("'" in word) and (len(word[0:word.index("'")]) == self.lengthOfAcrossClues[clue]) and not self.checkDuplicates(clue, "across", word[0:word.index("'")].upper()):
                    newDomain.add(
                        Word(word[0:word.index("'")].upper(), "across", -1, clue, True))
            for word in self.initialDomains["across"][clue].split("'"):
                # if word lenght is valid
                if (len(word) == self.lengthOfAcrossClues[clue]) and not self.checkDuplicates(clue, "across", word.upper()):
                    newDomain.add(Word(word.upper(), "across", -1, clue, True))
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
        # down
        for location in self.locationOfDownClues:
            wordIndex = -1
            tempCol = self.locationOfDownClues[location]["start"]["col"]
            rowStart = self.locationOfDownClues[location]["start"]["row"]
            rowEnd = self.locationOfDownClues[location]["end"]["row"]
            if (row <= int(rowEnd)) and (row >= int(rowStart)) and (col == int(tempCol)):
                wordIndex = row-rowStart
                if option == "best":
                    domains["down"] = {"index": wordIndex, "domain": self.getCurrentDomainWord(
                        "down", tempCol), "loc": self.locationOfDownClues[location]}
                else:
                    domains["down"] = {"index": wordIndex, "domain": self.filteredDomains["down"]
                                       [location], "loc": self.locationOfDownClues[location]}
        # across
        for location in self.locationOfAcrossClues:
            wordIndex = -1
            tempRow = self.locationOfAcrossClues[location]["start"]["row"]
            colStart = self.locationOfAcrossClues[location]["start"]["col"]
            colEnd = self.locationOfAcrossClues[location]["end"]["col"]
            if (col <= int(colEnd)) and (col >= int(colStart)) and (row == int(tempRow)):
                wordIndex = col-colStart
                if option == "best":
                    domains["across"] = {"index": wordIndex, "domain": self.getCurrentDomainWord(
                        "across", tempRow), "loc": self.locationOfAcrossClues[location]}
                else:
                    domains["across"] = {"index": wordIndex, "domain": self.filteredDomains["across"]
                                         [location], "loc": self.locationOfAcrossClues[location]}
        return domains

    def getCurrentDomainWord(self, acrossDown, index):
        words = []
        for word in self.bestSolution[acrossDown][index]:
            if word.active:
                words.append(word)
        return words

    def getAnswerGrid(self):
        if self.bestSolution["find"] != 0:
            answerGrid = [["", "", "", "", ""], ["", "", "", "", ""], [
                "", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]]
            for row in range(0, 5):
                for col in range(0, 5):
                    if answerGrid[row][col] == "":
                        domains = self.getTheRelatedDomainOfThisCell(
                            row, col, "best")
                        if domains == {}:
                            answerGrid[row][col] = "-"
                        else:
                            if len(self.getCurrentDomainWord("across", row)) == 1:
                                for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0].word)):
                                    answerGrid[row][colIndex] = domains["across"]["domain"][0].word[colIndex -
                                                                                                    domains["across"]["loc"]["start"]["col"]]
                            if len(self.getCurrentDomainWord("down", col)) == 1:
                                for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0].word)):
                                    answerGrid[rowIndex][col] = domains["down"]["domain"][0].word[rowIndex -
                                                                                                  domains["down"]["loc"]["start"]["row"]]

            for row in range(0, 5):
                for col in range(0, 5):
                    if answerGrid[row][col] == "":
                        answerGrid[row][col] = "*"

            for row in answerGrid:
                print(row)
            self.solvedPuzzle = answerGrid
        else:
            print(" CORT ")

    def isPuzzleSolved(self):
        answerGrid = [["", "", "", "", ""], ["", "", "", "", ""], [
            "", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]]
        puzzleSolved = True
        for row in range(0, 5):
            for col in range(0, 5):
                if answerGrid[row][col] == "":
                    domains = self.getTheRelatedDomainOfThisCell(row, col, "")
                    if domains == {}:
                        answerGrid[row][col] = "-"
                    else:
                        if len(self.getCurrentDomainWord("across", row)) == 1:
                            for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0].word)):
                                answerGrid[row][colIndex] = domains["across"]["domain"][0].word[colIndex -
                                                                                                domains["across"]["loc"]["start"]["col"]]
                        if len(self.getCurrentDomainWord("down", col)) == 1:
                            for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0].word)):
                                answerGrid[rowIndex][col] = domains["down"]["domain"][0].word[rowIndex -
                                                                                              domains["down"]["loc"]["start"]["row"]]
        for row in range(0, 5):
            for col in range(0, 5):
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
        for col in range(0, 5):
            print(str(col) + ": ", end=" ")
            for word in self.bestSolution["across"][col]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

        print("\nDown")
        for row in range(0, 5):
            print(str(row) + ": ", end=" ")
            for word in self.bestSolution["down"][row]:
                if word.active:
                    print(word.word, end=" ")
            print("\n")

    def changeNeglected(self):
        if self.count == 0:
            rows = [0, 1, 2, 3, 4]
            for r in range(0, len(rows)+1):
                for rsubset in itertools.combinations(rows, r):
                    cols = [0, 1, 2, 3, 4]
                    for c in range(0, len(cols)+1):
                        for csubset in itertools.combinations(cols, c):
                            self.neglectedWordsArray.append(
                                {"row": rsubset, "col": csubset})
            self.neglectedWords = self.neglectedWordsArray[self.count]
            self.count = self.count + 1
            return True
        else:
            """
            print("Neglected: ", end  ="")
            print(self.neglectedWords)
            """
            if self.count == 1024:
                return False
            self.neglectedWords = self.neglectedWordsArray[self.count]
            self.count = self.count + 1
            return True

    def isItTheBestSolution(self):
        count = 0
        for row in range(0, 5):
            wordCount = 0
            for word in self.domains["across"][row]:
                if word.active:
                    wordCount += 1
            if wordCount == 1:
                count += 1
        for col in range(0, 5):
            wordCount = 0
            for word in self.domains["down"][col]:
                if word.active:
                    wordCount += 1
            if wordCount == 1:
                count += 1

        if count > self.bestSolution["find"]:
            for row in range(0, 5):
                self.bestSolution["across"][row] = copy.deepcopy(
                    self.domains["across"][row])
            for col in range(0, 5):
                self.bestSolution["down"][col] = copy.deepcopy(
                    self.domains["down"][col])
            self.bestSolution["find"] = count

        # Büşranın fonksiyonu
        if count > 5:
            tempSolution = {"across": [[], [], [],
                                       [], []], "down": [[], [], [], [], []]}
            for row in range(0, 5):
                tempSolution["across"][row] = copy.deepcopy(
                    self.domains["across"][row])
            for col in range(0, 5):
                tempSolution["down"][col] = copy.deepcopy(
                    self.domains["down"][col])
            self.finalSolutions.append(tempSolution)

    def findFinalPuzzle(self):
        if len(self.finalSolution) == 1:
            self.finalSolution = self.gridMaker(self.finalSolution[0])
        else:
            maxPoint = 0
            for solution in self.finalSolutions:
                grid = self.gridMaker(solution)
                print("Calculating score for a possible grid:")
                for row in grid:
                    print(row)
                print("")
                score = ScorePuzzle(grid, self.locationOfAcrossClues,
                                    self.locationOfDownClues, self.acrossClues, self.downClues).score
                print("Score: ", score)
                if score > maxPoint:
                    maxPoint = score
                    self.finalSolution = grid

    def gridMaker(self, solution):
        answerGrid = [["", "", "", "", ""], ["", "", "", "", ""], [
            "", "", "", "", ""], ["", "", "", "", ""], ["", "", "", "", ""]]
        for row in range(0, 5):
            for col in range(0, 5):
                if answerGrid[row][col] == "":
                    domains = self.gridMakerHelper(row, col, solution)
                    if domains == {}:
                        answerGrid[row][col] = "-"
                    else:
                        if len(self.getCurrentDomainWord("across", row)) == 1:
                            for colIndex in range(domains["across"]["loc"]["start"]["col"], domains["across"]["loc"]["start"]["col"] + len(domains["across"]["domain"][0].word)):
                                answerGrid[row][colIndex] = domains["across"]["domain"][0].word[colIndex -
                                                                                                domains["across"]["loc"]["start"]["col"]]
                        if len(self.getCurrentDomainWord("down", col)) == 1:
                            for rowIndex in range(domains["down"]["loc"]["start"]["row"], domains["down"]["loc"]["start"]["row"] + len(domains["down"]["domain"][0].word)):
                                answerGrid[rowIndex][col] = domains["down"]["domain"][0].word[rowIndex -
                                                                                              domains["down"]["loc"]["start"]["row"]]

        return answerGrid

    def gridMakerHelper(self, row, col, curDomain):
        domains = {}
        # down
        for location in self.locationOfDownClues:
            wordIndex = -1
            tempCol = self.locationOfDownClues[location]["start"]["col"]
            rowStart = self.locationOfDownClues[location]["start"]["row"]
            rowEnd = self.locationOfDownClues[location]["end"]["row"]
            if (row <= int(rowEnd)) and (row >= int(rowStart)) and (col == int(tempCol)):
                wordIndex = row-rowStart
                domains["down"] = {"index": wordIndex, "domain": self.getCurrentDomainWords(
                    "down", tempCol, curDomain), "loc": self.locationOfDownClues[location]}
        # across
        for location in self.locationOfAcrossClues:
            wordIndex = -1
            tempRow = self.locationOfAcrossClues[location]["start"]["row"]
            colStart = self.locationOfAcrossClues[location]["start"]["col"]
            colEnd = self.locationOfAcrossClues[location]["end"]["col"]
            if (col <= int(colEnd)) and (col >= int(colStart)) and (row == int(tempRow)):
                wordIndex = col-colStart
                domains["across"] = {"index": wordIndex, "domain":  self.getCurrentDomainWords(
                    "across", tempRow, curDomain), "loc": self.locationOfAcrossClues[location]}
        return domains

    def getCurrentDomainWords(self, acrossDown, index, domain):
        words = []
        for word in domain[acrossDown][index]:
            if word.active:
                words.append(word)
        return words

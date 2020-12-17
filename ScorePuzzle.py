import requests

class ScorePuzzle:
    def __init__(self, grid, acrossLocation, downLocation, acrossClues, downClues):
        self.grid = grid
        self.acrossClues = acrossClues
        self.downClues = downClues
        self.acrossLocation = acrossLocation
        self.downLocation = downLocation
        self.downAnswers = {}
        self.acrossAnswers = {}
        self.score = 0

        self.getAnswers()
        self.scoreGrid()
    
    def getAnswers(self):
        """
        This function gets answers from letters stored in grid
        and stores them in downAnswers and acrossAnswers.
        """
        for clue in self.acrossLocation: # For across clues
            answer = ""
            empty = False
            for j in range(self.acrossLocation[clue]["start"]["col"], self.acrossLocation[clue]["end"]["col"] + 1):
                col = j
                row = self.acrossLocation[clue]["start"]["row"]
                if self.grid[row][col] != "":
                    answer += self.grid[row][col]
                else:
                    empty = True
                    break # If there is an empty cell, no need to find remaining cells for that clue
            if empty == False:
                self.acrossAnswers[clue] = answer

        for clue in self.downLocation: # For down clues
            answer = ""
            empty = False
            for j in range(self.downLocation[clue]["start"]["row"], self.downLocation[clue]["end"]["row"] + 1):
                row = j
                col = self.downLocation[clue]["start"]["col"]
                if self.grid[row][col] != "":
                    answer += self.grid[row][col]
                else:
                    empty = True
                    break # If there is an empty cell, no need to find remaining cells for that clue
            if empty == False:
                self.downAnswers[clue] = answer

    def scoreGrid(self):
        """
        This function scores grid by looking at each answers relation
        to the according clue. If an answer is related to the clue,
        it gets score given in the datamuse data.
        """
        downDict = {}
        acrossDict = {}
        for i in self.downClues:
            downDict[i[0]] = i[1]
        for i in self.acrossClues:
            acrossDict[i[0]] = i[1]

        self.helperScoreGrid(self.acrossAnswers,  acrossDict)
        self.helperScoreGrid(self.downAnswers, downDict)

    def helperScoreGrid(self, answers, clues):
        for answer in answers:
            word = clues[answer]
            r = requests.get('https://api.datamuse.com/words?ml={}'.format(word))
            if r != None:
                results = r.json()
                count = 0
                for result in results:
                    count += 1
                    if result['word'] == answers[answer].lower():#answers[indices[index]].lower():
                        self.score += result['score']
                        break
                    if count > 50:
                        break

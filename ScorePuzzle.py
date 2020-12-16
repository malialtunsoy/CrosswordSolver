import grequests

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
        self.helperScoreGrid(self.acrossAnswers, self.acrossClues)
        self.helperScoreGrid(self.downAnswers, self.downClues)
    
    def helperScoreGrid(self, answers, clues):
        urls = []
        indices = []
        for answer in answers:
            word = clues[answer]
            indices.append(answer)
            urls.append('https://api.datamuse.com/words?ml={}'.format(word))

        #requests_session = grequests.Session()
        rs = (grequests.get(u) for u in urls) #requests.get('https://api.datamuse.com/words?ml={}'.format(word))
        m = grequests.map(rs)

        index = 0
        for req in m:
            results = req.json()
            count = 0
            for result in results:
                count += 1
                if result['word'] == answers[indices[index]].lower():
                    self.score += result['score']
                    break
                if count > 10:
                    break
            index += 1

"""
downClues = {"1": "See 4-Down", "2": "Lincoln Center Performance", "3": "Less restricted", "4":"With 1-Down, tradition for the married couple at a wedding reception",
"5": "Symbol that shares a key with '?'"}
acrossClues = {"1": "Removes politely, as a hat", "6": "Rainy month", "7":"___ Tanden, Biden's pick to lead the O.M.B.", "8":"Salad green with a peppery taste",
"9": "Subject of the famous photo 'The Blue Marble'"}
grid = [["D", "O", "F", "F", "S"], ["A", "P", "R", "I", "K"],
["N", "E", "E", "R", "A"], ["C", "R", "E", "S", "S"], ["E", "A", "R", "T", "H"]]
downLocation = {"1": {"start": {"row": 0, "col": 0}, "end": {"row": 4, "col": 0}},
"2": {"start": {"row": 0, "col": 1}, "end": {"row": 4, "col": 1}},
"3": {"start": {"row": 0, "col": 2}, "end": {"row": 4, "col": 2}},
"4": {"start": {"row": 0, "col": 3}, "end": {"row": 4, "col": 3}},
"5": {"start": {"row": 0, "col": 4}, "end": {"row": 4, "col": 4}}
}
acrossLocation = {"1": {"start": {"row": 0, "col": 0}, "end": {"row": 0, "col": 4}},
"6": {"start": {"row": 1, "col": 0}, "end": {"row": 1, "col": 4}},
"7": {"start": {"row": 2, "col": 0}, "end": {"row": 2, "col": 4}},
"8": {"start": {"row": 3, "col": 0}, "end": {"row": 3, "col": 4}},
"9": {"start": {"row": 4, "col": 0}, "end": {"row": 4, "col": 4}}
}
 

puzzle = ScorePuzzle(grid, acrossLocation, downLocation, acrossClues, downClues)
print(puzzle.score)
"""
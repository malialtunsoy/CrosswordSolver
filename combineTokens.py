import nltk
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

# Processes the clue to generate token pairs to be later used in scraping
# Returns all the possible pairs of tokens for a clue
def combine_tokens(clue, acrossClues, downClues):
    # Checks if the clue is in the form of "See X-Down" or "See X-Across"
    if "See" in clue:
        clue = getPointedClue(clue, acrossClues, downClues)

    clue = clue.lower()
    #clue = clue.replace("-", " ")
    clue_without_punctuation = clue.translate(
        str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(clue_without_punctuation)
    tokens = [w for w in tokens if not w in stop_words]
    number_of_tokens = len(tokens)
    for i in range(number_of_tokens):
        if i != number_of_tokens - 1:
            tokens.append(tokens[i] + " " + tokens[i + 1])
    # print(tokens)
    return tokens

# Used to find the clues that are in the form of "See X-Down" or "See X-Across"
def getPointedClue(clue, acrossClues, downClues):
    pointedClue = ""
    if "Down" in clue:
        pointedClue = downClues[clue[4]]
    else:
        pointedClue = acrossClues[clue[4]]
    return pointedClue

# Example test
"""
acrossClues = {"1": "Removes politely, as a hat", "2": "Rainy month", "3": "___ Tanden, Biden's pick to lead the O.M.B.", 
                    "4": "Salad green with a peppery taste", "5": 'Subject of the famous photo "The Blue Marble"'}


downClues = {"1": "See 4-Down", "2": "Lincoln Center performance", "3":"Less restricted", 
                "4": "With 1-Down, tradition for the married couple at a wedding reception", "5": "Symbol that shares a key with \"?\""}

print("DOWN CLUES")
for key in downClues:
    print(combine_tokens(downClues[key], acrossClues, downClues))

print("ACROSS CLUES")
for key in acrossClues:
    print(combine_tokens(acrossClues[key], acrossClues, downClues))
"""
import nltk
import string
from nltk.corpus import stopwords
import spacy
from spacy.tokenizer import Tokenizer

stop_words = set(stopwords.words('english'))

def combine_tokens(clue, acrossClues, downClues):
    
    if "See" in clue:
        clue = getPointedClue(clue, acrossClues, downClues)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(clue)

    if len(doc.ents) != 0:
        tokens = list()
        for entity in doc.ents:
            tokens.append(entity.text)
    else:
        clue = clue.lower()
        clue_without_punctuation = clue.translate(
            str.maketrans('', '', string.punctuation))
        tokens = nltk.word_tokenize(clue_without_punctuation)
        tokens = [w for w in tokens if not w in stop_words]
        number_of_tokens = len(tokens)
        # print(tokens)
        for i in range(number_of_tokens):
            if i != number_of_tokens -1:
                tokens.append(tokens[i] + " " + tokens[i + 1])
    print(tokens)
    return tokens


    
def getPointedClue(clue, acrossClues, downClues):
    pointedClue = ""
    if "Down" in clue:
        pointedClue = downClues[clue[4]]
    else:
        pointedClue = acrossClues[clue[4]]
    return pointedClue

"""
acrossClues = {"1": "Removes politely, as a hat", "2": "Rainy month", "3": "___ Tanden, Biden's pick to lead the O.M.B.", 
                    "4": "Salad green with a peppery taste", "5": 'Subject of the famous photo "The Blue Marble"'}


downClues = {"1": "See 4-Down", "2": "Lincoln Center performance", "3":"Less restricted", 
                "4": "With 1-Down, tradition for the married couple at a wedding reception", "5": "Symbol that shares a key with \"?\""}

print("DOWN CLUES")
for key in downClues:
    combine_tokens(downClues[key], acrossClues, downClues)

print("ACROSS CLUES")
for key in acrossClues:
    combine_tokens(acrossClues[key], acrossClues, downClues)
"""

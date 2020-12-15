import nltk
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def combine_tokens(clue):
    clue = clue.lower()
    clue_without_punctuation = clue.translate(
        str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(clue_without_punctuation)
    tokens = [w for w in tokens if not w in stop_words]
    number_of_tokens = len(tokens)

    for i in range(number_of_tokens):
        if i != number_of_tokens -1:
            tokens.append(tokens[i] + " " + tokens[i + 1])

    return tokens
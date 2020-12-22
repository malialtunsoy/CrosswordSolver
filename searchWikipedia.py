import wikipedia
import string
from combineTokens import combine_tokens

def searchWikipedia(clue):
    """
    This function takes clue and search for the clue in wikipedia.
    Takes the first result found in wikipedia and considers only the summary
    of that page.
    Returns a set containing words it found on a wikipedia page.
    """
    text = set()
    clue = clue.translate(str.maketrans('', '', string.punctuation))
    search_results = wikipedia.search(clue, results=1)
    for result in search_results:
        try:
            content = wikipedia.page(result + ".").summary.translate(str.maketrans('', '', string.punctuation))
            for w in content.split():
                text.add(w.lower())
        except:
            continue

    return text
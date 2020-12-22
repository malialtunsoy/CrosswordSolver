import requests
from time import sleep
from bs4 import BeautifulSoup
import string
from combineTokens import combine_tokens 
import cProfile
import lxml
import cchardet

def searchSynonyms(clue, acrossClues, downClues):
    """
    This function takes clue, list of across clues and list of down clues.
    It tokenizes the clue first to subwords and search for each word on Merriam Webster
    and Datamuse.
    """
    print('Search list for "' + clue + '":', end=' ')
    tokens = combine_tokens(clue, acrossClues, downClues)
    print(tokens)
    words = set()
    for word in tokens:
        if(contains_multiple_words(word)):
            # Merriam webster
            r_mw = requests.get("https://www.merriam-webster.com/thesaurus/" + word.split()[0] + "%20" + word.split()[1])

            # Datamuse
            r_dm = requests.get('https://api.datamuse.com/words?rel_syn={}'.format(word))
            r_dm2 = requests.get('https://api.datamuse.com/words?ml={}'.format(word))

        else:
            # Merriam webster
            r_mw = requests.get("https://www.merriam-webster.com/thesaurus/" + word)

            # Datamuse
            r_dm = requests.get('https://api.datamuse.com/words?rel_syn={}'.format(word))
            r_dm2 = requests.get('https://api.datamuse.com/words?ml={}'.format(word))

        soup = BeautifulSoup(r_mw.text, 'lxml')

        # Search for synonym list on Merriam Webster
        for i in soup.select('.thes-list.syn-list a'):
            words.add(str(i.string).lower())

        # Search for related list on Merriam Webster
        for i in soup.select('.thes-list.rel-list a'):
            words.add(str(i.string).lower())
        
         # Search for similarity list on Merriam Webster
        for i in soup.select('.thes-list.sim-list a'):
            words.add(str(i.string).lower())      

        count = 0
        results = r_dm.json()
        for result in results:
            words.add(result['word'])
            count += 1
            if count > 20: # 20 is an enough value to get synonyms from one website
                break

        results = r_dm2.json()
        count = 0
        for result in results:
            words.add(result['word'])
            count += 1
            if count > 20:
                break
    return words


def contains_multiple_words(s):
  return len(s.split()) > 1


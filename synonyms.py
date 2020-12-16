import requests
from time import sleep
from bs4 import BeautifulSoup
import string
from combineTokens import combine_tokens 
import cProfile
import lxml
import cchardet

def searchSynonyms(clue, acrossClues, downClues):
    tokens = combine_tokens(clue, acrossClues, downClues)
    words = set()
    for word in tokens:
        if(contains_multiple_words(word)):
            # Thesaurus.com
            #r_th = requests.get("https://www.thesaurus.com/browse/" + word.split()[0] + "%20" + word.split()[1])

            # Merriam webster
            r_mw = requests.get("https://www.merriam-webster.com/thesaurus/" + word.split()[0] + "%20" + word.split()[1])

            # Datamuse
            r_dm = requests.get('https://api.datamuse.com/words?rel_syn={}+{}'.format(word.split()[0], word.split()[1]))
            r_dm2 = requests.get('https://api.datamuse.com/words?ml={}+{}'.format(word.split()[0], word.split()[1]))

        else:
            # Thesaurus.com
            #r_th = requests.get("https://www.thesaurus.com/browse/" + word)

            # Merriam webster
            r_mw = requests.get("https://www.merriam-webster.com/thesaurus/" + word)

            # Datamuse
            r_dm = requests.get('https://api.datamuse.com/words?rel_syn={}'.format(word))
            r_dm2 = requests.get('https://api.datamuse.com/words?ml={}'.format(word))
        """
        soup = BeautifulSoup(r_th.text, 'lxml')
        texts = soup.select('.MainContentContainer.css-cv252o.e1h3b0ep0 a')
        for i in texts:
            for each in i.text.split():
                each = each.translate(str.maketrans('', '', string.punctuation))
                words.add(each.lower())
        """
        soup = BeautifulSoup(r_mw.text, 'lxml')

        for i in soup.select('.thes-list.syn-list a'):
            words.add(str(i.string).lower())

        for i in soup.select('.thes-list.rel-list a'):
            words.add(str(i.string).lower())
            
        for i in soup.select('.thes-list.sim-list a'):
            words.add(str(i.string).lower())        
        
        results = r_dm.json()
        for result in results:
            words.add(result['word'])
        results = r_dm2.json()
        for result in results:
            words.add(result['word'])
    return words


def contains_multiple_words(s):
  return len(s.split()) > 1


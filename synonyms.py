import requests
from time import sleep
from bs4 import BeautifulSoup

def searchSynonyms(clue_words):
    words = set()
    for word in clue_words:
        r = requests.get("https://www.merriam-webster.com/thesaurus/" + word)
        soup = BeautifulSoup(r.content, 'html.parser')

        for i in soup.select('.thes-list.syn-list a'):
            words.add(i.string)

        for i in soup.select('.thes-list.rel-list a'):
            words.add(i.string)
            
        for i in soup.select('.thes-list.sim-list a'):
            words.add(i.string)
        
        r = requests.get(
            'https://api.datamuse.com/words?rel_syn={}'
            .format(word))
        results = r.json()
        for result in results:
            words.add(result['word'])

    return ' '.join(words)
    
#print(searchSynonyms(["historical", "artifact"]))
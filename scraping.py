import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wikipedia
import time

class Scraping:
    def __init__(self, clues):
        self.clues = clues
        self.domains = {"across": {}, "down":{}}

    def setDomains(self):
        for down in self.clues["down"]:
            self.domains["down"][down] = self.search(self.clues["down"][down])
        for across in self.clues["across"]:
            self.domains["across"][across] = self.search(self.clues["across"][across])

    def getClueList(self, clue):
        clueList = [clue]
        return clueList

    def search(self, clue):
        domain = ""
        for toSearch in self.getClueList(clue):
            #domain = domain + self.getGoogle(toSearch)
            domain = domain + self.getWiki(toSearch)
            #domain = domain + self.getSynonyms(toSearch)
            #domain = domain + self.getMerriam(toSearch)

        return domain

    def getGoogle(self, toSearch):

        return "toSearch"

    def getWiki(self, toSearch):
        search_results = wikipedia.search(toSearch, results=2)
        text = ""
        for result in search_results:
            text += wikipedia.page(result + ".").content
        return text

    def getMerriam(self,toSearch):
        request_url = "https://www.merriam-webster.com/dictionary/" + toSearch
        page = requests.get(request_url)
        source = page.text
        soup = BeautifulSoup(source, 'html.parser')
        for span in soup.find_all("span", class_="ex-sent first-child t no-aq sents"):
            span.decompose()

        results = soup.find_all("span", class_="dtText")

        string_results = list()
        for result in results:
            result = result.text
            result = result[1:]
            result = result.replace("\n", "")
            result = result.replace("\t", "")
            result = result.strip()
            string_results.append(result)
        
        return " ".join(string_results)

    def getSynonyms(self, toSearch):
        words = set()
        for word in toSearch.split():
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

"""
scraping = Scraping()
scraping.setDomains()
print(scraping.domains)
"""
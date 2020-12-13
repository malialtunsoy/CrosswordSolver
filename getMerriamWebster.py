import nltk 
import requests
from bs4 import BeautifulSoup

URL = "https://www.merriam-webster.com/dictionary/"

def get_merriam_webster(query):
    # Tokenize the search query (clue)
    words = nltk.word_tokenize(query)
    string_results = list()

    for word in words:
        request_url = URL + word
        page = requests.get(request_url)
        source = page.text
        soup = BeautifulSoup(source, 'html.parser')
        for span in soup.find_all("span", class_="ex-sent first-child t no-aq sents"):
            span.decompose()
    
        results = soup.find_all("span", class_="dtText")

        for result in results:
            result = result.text
            result = result[1:]
            result = result.replace("\n", "")
            result = result.replace("\t", "")
            string_results.append(' '.join(result.split()))
    
    return " ".join(string_results)
import nltk 
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

URL = "https://www.merriam-webster.com/dictionary/"

def get_merriam_webster(query):
    # Tokenize the search query (clue)
    tokens = nltk.word_tokenize(query)
    tokens_without_sw = [word for word in tokens if not word in stopwords.words()]

    string_results = list()

    for token in tokens_without_sw:
        request_url = URL + token
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
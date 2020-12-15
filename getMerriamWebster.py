import requests
from bs4 import BeautifulSoup
import string
from combineTokens import combine_tokens

URL = "https://www.merriam-webster.com/dictionary/"


def searchMerriamWebster(query):
    # Tokenize the search query (clue)
    tokens = combine_tokens(query)

    string_results = set()

    for token in tokens:
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
            string_results.add(' '.join(result.split()))

    return string_results



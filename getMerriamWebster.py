import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
stop_words = set(stopwords.words('english'))

URL = "https://www.merriam-webster.com/dictionary/"


def get_merriam_webster(query):
    # Tokenize the search query (clue)
    tokens = combine_tokens(query)

    string_results = list()

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
            string_results.append(' '.join(result.split()))

    return " ".join(string_results)


def combine_tokens(clue):
    clue = clue.lower()
    clue_without_punctuation = clue.translate(
        str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(clue_without_punctuation)
    tokens = [w for w in tokens if not w in stop_words]
    number_of_tokens = len(tokens)
    print(tokens)

    for i in range(number_of_tokens):
        if i != number_of_tokens -1:
            tokens.append(tokens[i] + " " + tokens[i + 1])

    return tokens
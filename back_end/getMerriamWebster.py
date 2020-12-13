import requests
from bs4 import BeautifulSoup

URL = "https://www.merriam-webster.com/dictionary/"

def get_merriam_webster(query):

    request_url = URL + query
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

print(get_merriam_webster("jargon"))


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import wikipedia
import time
import string

def searchWikipediaSelenium(clue):
    driver = webdriver.Chrome("C:\chromedriver.exe")
    driver.get("https://www.google.com")
    search_bar = driver.switch_to.active_element
    search_bar.send_keys(clue + " wikipedia.com")

    search_bar.send_keys(Keys.ENTER)
    driver.get(driver.current_url + "&lr=lang_en")
    time.sleep(3)
    driver.find_element_by_xpath('(//h3)[1]/../../a').click()
    text = driver.find_element_by_id('content').text

    words = ""
    for word in text.split():
        words += word

    return words


def searchWikipedia(clue):
    search_results = wikipedia.search(clue, results=2)
    text = set()
    for result in search_results:
        content = wikipedia.page(result + ".").content.translate(str.maketrans('', '', string.punctuation))
        for w in content.split():
            text.add(w.lower())
    return ' '.join(text) 

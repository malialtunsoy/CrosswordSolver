from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import WEBDRIVER_PREFERENCES

def executeGoogleSearch(query, site=None):
    word_list = set()

    driver = webdriver.Chrome()
    driver.get("https://www.google.com")
    search_bar = driver.switch_to_active_element()

    if site is None:
        search_bar.send_keys(query)
    # to get results from  a website
    else:
        search_bar.send_keys(query + " " + "site:" + site)

    search_bar.send_keys(Keys.ENTER)
    driver.get(driver.current_url + "&lr=lang_en")

    """
    result_headers = driver.find_element_by_id("ellip")
    for elem in result_headers:
        for word in elem.text.split():
            word_list.add(word)

    driver.close()
    print(word_list)
    return word_list
    """


executeGoogleSearch("varolakman")
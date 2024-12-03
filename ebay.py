import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

dirname, scriptname = os.path.split(os.path.abspath(__file__))
THIS_DIRECTORY = f"{dirname}{os.sep}"
HEADLESS = True
DRIVER = None

if DRIVER is None:
    options = webdriver.ChromeOptions()
    # options.headless = HEADLESS
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--user-data-dir=~/.config/google-chrome")
    options.add_argument("--headless=new")

    DRIVER = webdriver.Chrome(
        options=options  # , executable_path=f"{THIS_DIRECTORY}chromedriver.exe"
    )


def load_page(url):
    """Load the specified page with an automated browser"""
    DRIVER.get(url)
    DRIVER.implicitly_wait(5)


def findAllLinks():
    results = []
    url = "https://www.ebay.pl/sch/Obuwie-damskie/3034/i.html"
    for i in range(1, 1000, 1):
        print(i)
        load_page(url + "?_pgn=" + str(i))
        try:
            myElem = WebDriverWait(DRIVER, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[@id='srp-river-results']",
                    )
                )
            )
        except TimeoutException:
            print("Loading took too much time!")
        time.sleep(5)

        html = DRIVER.execute_script(
            "return document.getElementsByTagName('html')[0].innerHTML"
        )

        soup = BeautifulSoup(html, "html.parser")
        list_wrapper = soup.find("div", id="srp-river-results")
        items = list_wrapper.find_all(
            "div",
            class_=("s-item__wrapper"),
        )

        for item in items:
            results.append(findAllMemberData(item))


def findAllMemberData(item):
    title = item.find("div", class_="s-item__title")
    price = item.find("span", class_="s-item__price")

    return {
        "title": title.text.strip(),
        "price": price.text.strip(),
    }


if __name__ == "__main__":
    findAllLinks()

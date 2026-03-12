
import os
import pickle
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from app.config.settings import SETTINGS

# get the user data directory by running chrome://version/ in the browser and change the path accordingly
DATA_DIRECTORY = SETTINGS["DATA_DIRECTORY"]
# how to get user agent: https://www.whatismybrowser.com/detect/what-is-my-user-agent
USER_AGENT = SETTINGS["USER_AGENT"]

def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

def load_cookies(driver):
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except:
        pass

def gen_driver():
    chrome_options = Options()
    chrome_options.add_argument("user-agent=" + USER_AGENT)
    chrome_options.add_argument("--user-data-dir=" + DATA_DIRECTORY)
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.google.com/')
    load_cookies(driver)
    return driver
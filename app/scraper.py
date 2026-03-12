from random import randint
import traceback
import json
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from app.helpers.stealthDriver import gen_driver
from app.sources.sources import SOURCES
from app.config.settings import SETTINGS

sources_path = SETTINGS["SOURCES_PATH"]

class DummyClass:
    def __init__(self, text):
        self.text = text

def scrape_allsides_ratings() -> dict:
    jsonSources = SOURCES
    driver = gen_driver()
    missingVals = 0
    for s in jsonSources:
        missing = False
        random_sleep()
        url = f"https://www.allsides.com/news-source/{format_news_name(s["name"])}-media-bias"
        print(f"Starting scrape for {s["name"]} at {url}")
        driver.get(url)
        try:
            random_sleep()
            # Try to get rating if not keep as previous rating. Default to "0.00"
            rating = DummyClass(s.get("rating", "0.00"))
            try:
                rating = driver.find_element(By.CLASS_NAME, "numerical-bias-rating")
            except NoSuchElementException as e:
                missing = True
                print(f"No rating found for {s["name"]}")

            # Try to get lean if not keep as previous lean. Default to "Center"
            lean = "Center"
            if float(rating.text) < -3.00:
                lean = "Left"
            elif float(rating.text) < -1.00:
                lean = "Center-Left"
            elif float(rating.text) < 1.00:
                lean = "Center"
            elif float(rating.text) < 3.00:
                lean = "Center-Right"
            else:
                lean = "Right"

            print(f"Scrape for {s["name"]} done. Rating: {s.get("rating", "0.00")} to {rating.text}. Lean: {s.get("lean", "Center")} to {lean}")
            s["rating"] = rating.text
            s["lean"] = lean
            missingVals += int(missing)
        except Exception as e:
            print(e, traceback.format_exc())
    driver.close()
    print(f"Finished scraping. Missing values: {missingVals}")
    with open(sources_path, "w") as sources:
        json.dump(jsonSources, sources, indent=4)

def format_news_name(name: str) -> str:
    return name.lower().strip().removeprefix("the ").replace(" ", "-")

def random_sleep():
    sleep(randint(2, 5))

if __name__ == "__main__":
    scrape_allsides_ratings()
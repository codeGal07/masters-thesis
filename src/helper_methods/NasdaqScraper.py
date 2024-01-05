import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.helper_methods.utils.scraper_utils import get_title_and_text, process_opening


class NasdaqScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_accept(self):
        try:
            time.sleep(3)
            cookies2 = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookies2.click()

        except Exception as e:
            print(f"Error: {e}")
            pass

    def get_article_title(self):
        try:
            title = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1")))
            return title.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def get_article_text(self):
        try:
            article_body = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.body__content")))
            return article_body.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def process_opening(self):
        process_opening(self)

    def get_title_and_text(self):
        return get_title_and_text(self)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.helper_methods.utils.scraper_utils import process_opening, get_title_and_text


class InvestopediaScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_accept(self):
        try:
            cookies = self.wait.until(EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
            cookies.click()

        except:  # there is no accept cookies button
            pass

    def get_article_title(self):
        try:
            title_element = self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "h1")))
            return title_element.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def get_article_text(self):
        try:
            article_body = self.wait.until(
                EC.presence_of_element_located((By.ID, "article-body_1-0")))
            return article_body.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def process_opening(self):
        process_opening(self)

    def get_title_and_text(self):
        return get_title_and_text(self)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.helper_methods.utils.scraper_utils import get_title_and_text, process_opening


class YahooFinanceScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_accept(self):
        try:
            agree_button = self.wait.until(EC.presence_of_element_located((By.NAME, 'agree')))
            try:
                scroll_down_button = self.driver.find_element(By.ID, 'scroll-down-btn')
                scroll_down_button.click()
            except:
                pass
            agree_button.click()
        except Exception as e:
            print(f"Error: {e}")
            pass

    def click_show_more_button(self):
        try:
            story_continues = self.driver.find_element(By.CSS_SELECTOR, "button.link.caas-button.collapse-button")
            story_continues.click()
        except:
            pass

    def get_article_title(self):
        try:
            title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cover-title.yf-1at0uqp")))
            return title.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def get_article_text(self):
        try:
            article_body = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".body.yf-tsvcyu")))
            return article_body.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def process_opening(self):
        process_opening(self)
        self.click_show_more_button()

    def get_title_and_text(self):
        return get_title_and_text(self)

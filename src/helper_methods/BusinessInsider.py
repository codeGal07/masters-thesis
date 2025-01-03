import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.helper_methods.utils.scraper_utils import get_title_and_text, process_opening


class BusinessInsider:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_accept(self):
        try:
            time.sleep(3)
            iframe = self.driver.find_element(By.ID, "sp_message_iframe_1218008")
            self.driver.switch_to.frame(iframe)

            # Locate and click the button inside the iframe
            cookies = self.driver.find_element(By.XPATH, "//button[@title='Accept All']")
            cookies.click()
        except Exception:
            # If the iframe or button doesn't exist, pass
            pass
        finally:
            # Ensure the context switches back to the main content
            self.driver.switch_to.default_content()

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
                EC.presence_of_element_located((By.ID, "piano-inline-content-wrapper")))
            return article_body.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def process_opening(self):
        process_opening(self)

    def get_title_and_text(self):
        return get_title_and_text(self)

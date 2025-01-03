from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.helper_methods.utils.scraper_utils import get_title_and_text, process_opening


class BBCScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_accept(self):
        try:
            # Wait for the iframe to be present
            iframe = self.wait.until(
                EC.presence_of_element_located((By.ID, "sp_message_iframe_1192447"))
            )

            # Switch to the iframe
            self.driver.switch_to.frame(iframe)

            # Find and click the "I agree" button
            agree_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='I agree']"))
            )
            agree_button.click()

            # Switch back to the default content
            self.driver.switch_to.default_content()

        except:
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
                EC.presence_of_element_located((By.ID, "main-content")))
            return article_body.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def process_opening(self):
        process_opening(self)

    def get_title_and_text(self):
        return get_title_and_text(self)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.helper_methods.utils.scraper_utils import get_title_and_text, process_opening


class TheMotleyFoolScraper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)

    def click_accept(self):
        try:
            cookies = self.wait.until(
                EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
            cookies.click()

        except:  # there is no accept cookies button
            pass

        try:
            radio_button_agree = self.wait.until(
                self.driver.find_element_by_css_selector("input[name='legalese_id_1'][value='True']"))
            radio_button_agree.click()

            radio_button_agree = self.driver.find_element_by_css_selector("input[name='legalese_id_4'][value='False']")
            radio_button_agree.click()

            submit_button = self.driver.find_element_by_id("gdpr-submit-button")
            submit_button.click()
        except:  # there is no gdpr dialog opened
            pass

    def close_sale_popUp(self):
        try:
            close_popUp_button = self.wait.until(self.driver.find_element_by_id("popup-x"))
            close_popUp_button.click()
        except:
            pass

    def get_article_title(self):
        try:
            title = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".text-3xl")))
            return title.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def get_article_text(self):
        try:
            article_body = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "article-body")))
            return article_body.text
        except Exception as e:
            print(f"Error: {e}")
            pass

    def process_opening(self):
        process_opening(self)
        self.close_sale_popUp()

    def get_title_and_text(self):
        return get_title_and_text(self)

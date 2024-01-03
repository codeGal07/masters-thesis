import time

from selenium.webdriver.common.by import By


class TheMotleyFoolScraper:
    def __init__(self, driver):
        self.driver = driver

    def click_accept(self):
        try:
            time.sleep(3)
            cookies = self.driver.find_element_by_id("onetrust-accept-btn-handler")
            cookies.click()

        except:  # there is no accept cookies button
            pass

        try:
            time.sleep(3)
            radio_button_agree = self.driver.find_element_by_css_selector("input[name='legalese_id_1'][value='True']")
            radio_button_agree.click()

            radio_button_agree = self.driver.find_element_by_css_selector("input[name='legalese_id_4'][value='False']")
            radio_button_agree.click()

            submit_button = self.driver.find_element_by_id("gdpr-submit-button")
            submit_button.click()
        except:  # there is no gdpr dialog opened
            pass

    def close_sale_popUp(self):
        try:
            time.sleep(3)
            close_popUp_button = self.driver.find_element_by_id("popup-x")
            close_popUp_button.click()
        except:
            pass

    def get_title(self):
        try:
            title_element = self.driver.find_element(By.CSS_SELECTOR,
                                                     "h1.font-medium.text-gray-1100.leading-relative-2.md\\:text-h2.lg\\:text-h1-tight.xl\\:text-h1")
            return title_element.text
        except:
            pass

    def get_data(self):
        try:
            article_body = self.driver.find_element(By.CLASS_NAME, "article-body")
            return article_body.text
        except:
            return ""

    def process_opening(self):
        self.click_accept()
        self.close_sale_popUp()

    def get_title_and_data(self):
        title = self.get_title()
        data = self.get_data()
        return title, data

from selenium.webdriver.common.by import By


class YahooFinanceScraper:
    def __init__(self, driver):
        self.driver = driver

    def click_agree_button(self):
        try:
            agree_button_yahoo = self.driver.find_element(By.NAME, 'agree')
            # agree_button_yahoo = driver.find_element(By.CSS_SELECTOR, 'button.btn.secondary.accept-all')

            try:
                scroll_down_button_yahoo = self.driver.find_element(By.ID, 'scroll-down-btn')
                scroll_down_button_yahoo.click()
            except:
                pass
            agree_button_yahoo.click()
        except:
            pass

    def click_show_more_button(self):
        try:
            story_continues_yahoo = self.driver.find_element(By.CSS_SELECTOR, "button.link.caas-button.collapse-button")
            story_continues_yahoo.click()
        except:
            pass

    def get_data(self):
        try:
            article_body = self.driver.find_element(By.CSS_SELECTOR, "div.caas-body")
            return article_body.text
        except:
            return ""

    def get_title(self):
        try:
            title_yahoo = self.driver.find_element(By.CSS_SELECTOR, "h1[data-test-locator='headline']")
            return title_yahoo.text
        except:
            pass

    def process_opening_yahoo_finance(self):
        self.click_agree_button()
        self.click_show_more_button()

    def get_title_and_data(self):
        title = self.get_title()
        data = self.get_data()
        return title, data

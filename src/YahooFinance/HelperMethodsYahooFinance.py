from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


def click_agree_button_yahoo_finance(driver):
    try:
        agree_button_yahoo = driver.find_element(By.NAME, 'agree')
        # agree_button_yahoo = driver.find_element(By.CSS_SELECTOR, 'button.btn.secondary.accept-all')
        agree_button_yahoo.click()

    except:

        pass


def click_show_more_button_yahoo_finance(driver):
    try:
        story_continues_yahoo = driver.find_element(By.CSS_SELECTOR, "button.link.caas-button.collapse-button")
        story_continues_yahoo.click()
    except NoSuchElementException:
        pass


def get_title_yahoo_finance(driver):
    try:
        title_yahoo = driver.find_element(By.CSS_SELECTOR, "div.caas-title-wrapper")
        return title_yahoo.text
    except NoSuchElementException:
        pass

def get_data_yahoo_finance(driver):
    try:
        content = driver.find_element(By.CSS_SELECTOR, "div.caas-body")
        return content.text
    except:
        return ""

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def click_agree_button(driver):
    try:
        agree_button_yahoo = driver.find_element(By.NAME, 'agree')
        # agree_button_yahoo = driver.find_element(By.CSS_SELECTOR, 'button.btn.secondary.accept-all')

        try:
            scroll_down_button_yahoo = driver.find_element(By.ID, 'scroll-down-btn')
            scroll_down_button_yahoo.click()
        except:
            pass
        agree_button_yahoo.click()
    except:
        pass


def click_show_more_button(driver):
    try:
        story_continues_yahoo = driver.find_element(By.CSS_SELECTOR, "button.link.caas-button.collapse-button")
        story_continues_yahoo.click()
    except:
        pass


def get_title(driver):
    try:
        title_yahoo = driver.find_element(By.CSS_SELECTOR, "h1[data-test-locator='headline']")
        return title_yahoo.text
    except:
        pass


def get_data(driver):
    try:
        article_body = driver.find_element(By.CSS_SELECTOR, "div.caas-body")
        return article_body.text
    except:
        return ""

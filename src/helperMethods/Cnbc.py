import time

from selenium.webdriver.common.by import By


def click_accept(driver):
    try:
        time.sleep(3)
        cookies = driver.find_element_by_id("onetrust-accept-btn-handler")
        cookies.click()

    except:  # there is no accept cookies button
        pass


def get_title(driver):
    try:
        title_element = driver.find_element(By.CLASS_NAME, "ArticleHeader-headline")
        return title_element.text
    except:
        pass


def get_data(driver):
    try:
        article_body = driver.find_element(By.CLASS_NAME, "ArticleBody-articleBody")
        return article_body.text
    except:
        return ""

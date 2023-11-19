import time

from selenium.webdriver.common.by import By


def click_accept(driver):
    try:
        time.sleep(3)
        cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies.click()

    except:  # there is no accept cookies button
        pass

def get_title(driver):
    try:
        title_element = driver.find_element(By.TAG_NAME, "h1")
        return title_element.text
    except Exception as e:
        print(f"Error: {e}")
        pass


def get_data(driver):
    try:
        article_body = driver.find_element(By.CLASS_NAME, "article-body__wrapper__3IxHM")
        return article_body.text
    except Exception as e:
        print(f"Error: {e}")
        return ""

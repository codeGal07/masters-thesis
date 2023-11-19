from selenium.webdriver.common.by import By

def get_title(driver):
    try:
        title_element = driver.find_element(By.TAG_NAME, "h1")
        return title_element.text
    except Exception as e:
        print(f"Error: {e}")
        pass


def get_data(driver):
    try:
        article_body = driver.find_element(By.ID, "main-content")
        return article_body.text
    except Exception as e:
        print(f"Error: {e}")
        return ""

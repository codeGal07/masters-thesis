from selenium.webdriver.common.by import By


def click_agree_button(driver):
    agree_button_yahoo = driver.find_element(By.NAME, 'agree')
    agree_button_yahoo.click()


def click_show_more_button(driver):
    story_continues_yahoo = driver.find_element(By.CSS_SELECTOR, "button.link.caas-button.collapse-button")
    story_continues_yahoo.click()

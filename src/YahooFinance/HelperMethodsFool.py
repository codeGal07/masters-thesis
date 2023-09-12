import time

from selenium.webdriver.common.by import By


def click_accept_button_fool(driver):
    try:
        time.sleep(6)
        cookies_fool = driver.find_element_by_id("onetrust-accept-btn-handler")
        cookies_fool.click()

    except:  # there is no accept cookies button
        pass

    try:
        time.sleep(1)
        radio_button_agree = driver.find_element_by_css_selector("input[name='legalese_id_1'][value='True']")
        radio_button_agree.click()

        radio_button_agree = driver.find_element_by_css_selector("input[name='legalese_id_4'][value='False']")
        radio_button_agree.click()

        submit_button_yahoo = driver.find_element_by_id("gdpr-submit-button")
        submit_button_yahoo.click()
    except:  # there is no gdpr dialog opened
        pass


def get_title_fool(driver):
    try:
        title_element = driver.find_element(By.CSS_SELECTOR,
                                            "h1.font-medium.text-gray-1100.leading-relative-2.md\\:text-h2.lg\\:text-h1-tight.xl\\:text-h1")
        return title_element.text
    except:
        pass

from selenium import webdriver

from YahooFinance.HelperMethodsYahooFinance import *


def search_stock_info(stock_name, site, after, before, number_of_hits):
    search_string = stock_name + " site:" + site + " after:" + after + " before:" + before

    driver = webdriver.Chrome('chromedriver')
    driver.set_window_position(-1000, 0)

    for i in range(number_of_hits):
        driver.get("https://www.google.com/search?q=" + search_string + "&start=" + str(i))

        if i == 0:
            agree_button_google = driver.find_element(By.ID, 'L2AGLb')
            agree_button_google.click()

        # Click the first hit on Google
        first_hit = driver.find_element(By.CLASS_NAME, 'MjjYud')
        first_hit.click()

        # Get data based on website
        if site == "https://finance.yahoo.com/":
            click_agree_button(driver)
            click_show_more_button(driver)

    driver.quit()


def main():
    stock_name = "AAPL"
    site = "https://finance.yahoo.com/"
    after = "2021-01-02"
    before = "2021-02-02"
    number_of_hits = 1

    search_stock_info(stock_name, site, after, before, number_of_hits)


if __name__ == "__main__":
    main()

from datetime import time

from selenium import webdriver
import pandas_market_calendars as mcal
import pandas as pd
import sys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from src.SP500DataScraper import get_SP500_data
from src.SemanticAnalysis import *
from src.WriteFile import *
from src.YahooFinance.HelperMethodsYahooFinance import *
from src.YahooFinance.HelperMethodsFool import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


# from selenium.webdriver.firefox.options import Options


def get_all_data(date_from, date_to, number_of_hits, file_data_path, driver):
    trading_dates = get_trading_dates(date_from, date_to)
    stock_symbols = get_all_stock_symbols()
    sources = get_specify_sources()

    for i in range(len(trading_dates) - 1):
        before = trading_dates[i].strftime("%Y-%m-%d")
        after = trading_dates[i + 1].strftime("%Y-%m-%d")
        for stock_name in stock_symbols:
            for source in sources:
                search_stock_info(stock_name, source, before, after, number_of_hits, file_data_path, driver, i)


def get_trading_dates(start_date, end_date):
    # Create a calendar
    nyse = mcal.get_calendar('NYSE')
    dates = nyse.schedule(start_date=start_date, end_date=end_date)

    # Filter out non-trading dates
    trading_dates = dates.index.normalize()

    return trading_dates


def get_all_stock_symbols():
    # Read the CSV file into a pandas DataFrame
    # TODO temporary cropped data
    data = pd.read_csv('data/sp500_CROP.csv')
    stock_symbols = data['Company']

    return stock_symbols


def get_specify_sources():
    # TODO add more sources
    # sources = ["https://finance.yahoo.com/", "https://www.fool.com/"]
    sources = ["https://www.fool.com/"]

    return sources


def check_link_starts_with_source(source, lnk):
    if source in lnk:
        return True
    else:
        return False


def search_stock_info(stock_name, source, after, before, number_of_hits, file_data_path, driver, i):
    search_string = stock_name + " site:" + source + " after:" + after + " before:" + before

    driver.get("https://www.google.com/search?q=" + search_string)

    # checks if cought being a bot
    try:
        driver.find_element(By.NAME, 'Our systems have detected unusual traffic from your computer network')
        sys.exit("CAUGHT BEING A BOT")
    except:
        pass

    try:

        agree_button_google = driver.find_element(By.ID, 'L2AGLb')
        agree_button_google.click()
    except:
        pass

    lnks = driver.find_elements(By.TAG_NAME, "a")
    count_hits = 0

    # Get links from Google search page
    myLnks = []
    for lnk in lnks:
        # print(lnk.get_attribute("href"))
        myLnks.append(lnk.get_attribute("href"))

    for news_link in myLnks:
        if count_hits == number_of_hits:
            break
        if news_link is not None and news_link.startswith(source):
            count_hits += 1
            # Go to yahoo news
            driver.get(news_link)
            # Get text data based on website
            text_data = ""
            title_data = ""
            if source == "https://finance.yahoo.com/":
                click_agree_button_yahoo_finance(driver)
                title_data = get_title_yahoo_finance(driver)
                click_show_more_button_yahoo_finance(driver)
                text_data = get_data_yahoo_finance(driver)
            if source == "https://www.fool.com/":
                click_accept_button_fool(driver)
                title_data = get_title_fool(driver)

            polarity = evaluate_text_semantics(text_data)

            current_url = driver.current_url
            write_data_into_file(before, stock_name, polarity, source, title_data, current_url, file_data_path,
                                 text_data)


def create_chrome_driver(headless):
    if headless:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        path = "/Users/sabina.matjasic/Documents/googlechrome.dmg"
        driver = webdriver.Chrome(executable_path=path, options=options)
        return driver
    else:
        driver = webdriver.Chrome(executable_path='/opt/homebrew/Caskroom/chromedriver/102.0.5005.61/chromedriver')
        driver.set_window_position(-100, 0)
        driver.maximize_window()
        return driver


def create_firefox_driver(headless):
    pass
    if headless:
        # todo
        pass
    else:
        # Create the WebDriver instance
        driver = webdriver.Firefox()
        driver.set_window_position(-100, 0)
        driver.maximize_window()
        return driver


def main():
    date_from = '2023-02-07'
    date_to = '2023-03-01'
    number_of_hits = 3
    file_data_path = "data/stock_info.txt"
    headless = False

    # Only needed once to get SP500 data into CSV file
    # get_SP500_data()

    driver = create_firefox_driver(headless)
    # driver = create_chrome_driver(headless)
    create_file_if_not_exists(file_data_path)
    get_all_data(date_from, date_to, number_of_hits, file_data_path, driver)
    driver.quit()


if __name__ == "__main__":
    main()

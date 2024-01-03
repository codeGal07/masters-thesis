from datetime import time

from selenium import webdriver
import pandas_market_calendars as mcal
import pandas as pd
import sys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from src.SP500DataScraper import get_SP500_data
from src.SemanticAnalysis import *
from src.WriteFile import *
import src.helperMethods.TheMotleyFool as motley_fool_methods
import src.helperMethods.YahooFinance as yahoo_finance_methods
import src.helperMethods.Cnbc as cnbc_methods
import src.helperMethods.BBC as BBC_methods
import src.helperMethods.Reuters as reuters_methods
import src.helperMethods.Investopedia as investopedia_methods

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
    # NOTE temporary cropped data
    data = pd.read_csv('data/sp500_CROP.csv')
    stock_symbols = data['Company']

    return stock_symbols


def get_specify_sources():
    # TODO add more sources
    # Bloomberg: detected unusual activity right away
    # Seekingalpha: not free
    # MarketWatch: not free
    # New york times: not free
    # WSY: not free

    # bbc: Ok, but not a lot of data
    # investopedia: Ok, but not a lot of data

    # sources =
    # ["https://finance.yahoo.com/",
    # "https://www.fool.com/",
    # "https://www.cnbc.com/,
    # https://www.bbc.com/,
    # https://www.reuters.com/,
    # https://www.investopedia.com/"]

    sources = ["https://finance.yahoo.com/"]

    return sources


def check_link_starts_with_source(source, lnk):
    if source in lnk:
        return True
    else:
        return False


def search_stock_info(stock_name, source, after, before, number_of_hits, file_data_path, driver, i):
    search_string = stock_name + " site:" + source + " after:" + after + " before:" + before

    driver.get("https://www.google.com/search?q=" + search_string)

    # Checks if caught being a bot
    try:
        driver.find_element(By.NAME, 'Our systems have detected unusual traffic from your computer network')
        sys.exit("CAUGHT BEING A BOT")
    except:
        pass

    agree_with_cookies_on_google(driver)
    myLinks = get_links_from_google_search_page(driver)

    count_hits = 0
    for news_link in myLinks:
        if count_hits == number_of_hits:
            break
        if news_link is not None and news_link.startswith(source):
            driver.get(news_link)
            # Get text data based on website
            text_data = ""
            title_data = ""
            if source == "https://finance.yahoo.com/":
                yahoo_scraper = yahoo_finance_methods.YahooFinanceScraper(driver)
                yahoo_scraper.process_opening_yahoo_finance()
                title_data, text_data = yahoo_scraper.get_title_and_data()
            # if source == "https://finance.yahoo.com/":
            #     yahoo_finance_methods.click_agree_button(driver)
            #     yahoo_finance_methods.click_show_more_button(driver)
            #     title_data = yahoo_finance_methods.get_title(driver)
            #     text_data = yahoo_finance_methods.get_data(driver)
            if source == "https://www.fool.com/":
                motley_fool_methods.click_accept(driver)
                title_data = motley_fool_methods.get_title(driver)
                text_data = motley_fool_methods.get_data(driver)
            if source == "https://www.cnbc.com/":
                cnbc_methods.click_accept(driver)
                title_data = cnbc_methods.get_title(driver)
                text_data = cnbc_methods.get_data(driver)
            if source == "https://www.bbc.com/":
                title_data = BBC_methods.get_title(driver)
                text_data = BBC_methods.get_data(driver)
            if source == "https://www.reuters.com/":
                reuters_methods.click_accept(driver)
                title_data = reuters_methods.get_title(driver)
                text_data = reuters_methods.get_data(driver)
            if source == "https://www.investopedia.com/":
                investopedia_methods.click_accept(driver)
                title_data = investopedia_methods.get_title(driver)
                text_data = investopedia_methods.get_data(driver)

            if text_data is not None:
                polarity = evaluate_text_semantics(text_data)
                current_url = driver.current_url
                count_hits += 1
                write_data_into_file(before, stock_name, polarity, source, title_data, current_url, file_data_path,
                                     text_data)


def agree_with_cookies_on_google(driver):
    try:
        agree_button_google = driver.find_element(By.ID, 'L2AGLb')
        agree_button_google.click()
    except:
        pass


def get_links_from_google_search_page(driver):
    links = driver.find_elements(By.TAG_NAME, "a")
    myLinks = []
    for lnk in links:
        # print(lnk.get_attribute("href"))
        myLinks.append(lnk.get_attribute("href"))
    return myLinks


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

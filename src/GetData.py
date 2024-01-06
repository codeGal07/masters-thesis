from datetime import time
import time
from selenium import webdriver
import pandas_market_calendars as mcal
import pandas as pd
import random
import sys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from src.SP500DataScraper import get_SP500_data
from src.SemanticAnalysis import *
from src.WriteFile import *
import src.helper_methods.CnbcScraper as cnbc_methods
import src.helper_methods.BBCScraper as BBC_methods
import src.helper_methods.InvestopediaScraper as investopedia_methods

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.helper_methods.TheMotleyFoolScraper import TheMotleyFoolScraper
from src.helper_methods.YahooFinanceScraper import YahooFinanceScraper
from src.helper_methods.ReutersScraper import ReutersScraper
from src.helper_methods.InvestopediaScraper import InvestopediaScraper
from src.helper_methods.CnbcScraper import CnbcScraper
from src.helper_methods.BBCScraper import BBCScraper
from src.helper_methods.NasdaqScraper import NasdaqScraper
from src.helper_methods.CnnScraper import CnnScraper
from src.helper_methods.BusinessInsider import BusinessInsider


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
    # https://www.ft.com/ not free
    # https://www.reuters.com/ TODO knows I'm a bot
    # https://www.investing.com/ random articles
    # https://www.marketscreener.com/ random articles

    # bbc: Ok, but not a lot of data
    # investopedia: Ok, but not a lot of data
    # cnn: almost no data

    # sources = ["https://finance.yahoo.com/",
    #            "https://www.fool.com/",
    #            "https://www.cnbc.com/",
    #            "https://www.bbc.com/",
    #            "https://www.nasdaq.com/",
    #            "https://www.cnn.com/",
    #            "https://www.investopedia.com/",
    #            "https://www.businessinsider.com/"]

    sources = ["https://www.businessinsider.com/"]

    return sources


def check_link_starts_with_source(source, lnk):
    if source in lnk:
        return True
    else:
        return False


def search_stock_info(stock_name, source, after, before, number_of_hits, file_data_path, driver, i):
    search_string = stock_name + " site:" + source + " after:" + after + " before:" + before

    wait_to_avoid_bot_detection()

    driver.get("https://www.google.com/search?q=" + search_string)

    # Checks if caught being a bot
    try:
        driver.find_element(By.NAME, 'Our systems have detected unusual traffic from your computer network')
        sys.exit("CAUGHT BEING A BOT")
    except:
        pass

    agree_with_cookies_on_google(driver)
    myLinks = get_links_from_google_search_page(driver)

    # Define a dictionary to map sources to their corresponding scraper classes
    scraper_mapping = {
        "https://finance.yahoo.com/": YahooFinanceScraper,
        "https://www.fool.com/": TheMotleyFoolScraper,
        "https://www.cnbc.com/": CnbcScraper,
        "https://www.bbc.com/": BBCScraper,
        "https://www.reuters.com/": ReutersScraper,
        "https://www.investopedia.com/": InvestopediaScraper,
        "https://www.nasdaq.com/": NasdaqScraper,
        "https://www.cnn.com": CnnScraper,
        "https://www.businessinsider.com/": BusinessInsider

    }

    count_hits = 0
    for news_link in myLinks:
        if count_hits == number_of_hits:
            break
        if news_link is not None and news_link.startswith(source):
            driver.get(news_link)
            # Get text data based on website
            text_data = ""
            title_data = ""

            # Check if the source is in the mapping
            if source in scraper_mapping:
                # Get the scraper class based on the source
                scraper_class = scraper_mapping[source]

                # Instantiate the scraper and process the opening
                current_scraper = scraper_class(driver)
                current_scraper.process_opening()

                # Get title and text data
                title_data, text_data = current_scraper.get_title_and_text()

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


def wait_to_avoid_bot_detection():
    some_time = random.uniform(0, 3)
    time.sleep(some_time)


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
        # Create a Firefox WebDriver instance in headless mode
        FIREFOXPATH = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'

        # Create a Firefox WebDriver instance in headless mode
        options = webdriver.FirefoxOptions()
        options.binary = FIREFOXPATH
        options.add_argument('--headless')

        # You can edit firefox profiles in about:profiles
        options.set_preference('profile',
                               "/Users/sabina.matjasic_new/Library/Application Support/Firefox/Profiles/t9vwtgiz.FirstUser")

        return webdriver.Firefox(options=options, log_path="geckodriver.log")

    else:
        # Create the WebDriver instance
        driver = webdriver.Firefox()
        driver.set_window_position(-100, 0)
        driver.maximize_window()
        return driver


def main():
    date_from = '2023-02-07'
    date_to = '2023-03-01'
    number_of_hits = 1
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

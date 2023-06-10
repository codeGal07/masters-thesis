from selenium import webdriver
import pandas_market_calendars as mcal
import pandas as pd

from src.SP500DataScraper import get_SP500_data
from src.SemanticAnalysis import *
from src.WriteFile import *
from src.YahooFinance.HelperMethodsYahooFinance import *


def get_all_data(date_from, date_to, number_of_hits, file_data_path):
    trading_dates = get_trading_dates(date_from, date_to)
    stock_symbols = get_all_stock_symbols()
    sources = get_specify_sources()

    for i in range(len(trading_dates) - 1):
        before = trading_dates[i].strftime("%Y-%m-%d")
        after = trading_dates[i + 1].strftime("%Y-%m-%d")
        for stock_name in stock_symbols:
            for source in sources:
                search_stock_info(stock_name, source, before, after, number_of_hits, file_data_path)


def get_trading_dates(start_date, end_date):
    # Create a calendar
    nyse = mcal.get_calendar('NYSE')
    dates = nyse.schedule(start_date=start_date, end_date=end_date)

    # Filter out non-trading dates
    trading_dates = dates.index.normalize()

    return trading_dates


def get_all_stock_symbols():
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv('data/sp500_data.csv')
    stock_symbols = data['Symbol']

    return stock_symbols


def get_specify_sources():
    # TODO add more sources
    # sources = ["https://finance.yahoo.com/", "https://www.wsj.com/"]
    sources = ["https://finance.yahoo.com/"]

    return sources


def search_stock_info(stock_name, source, after, before, number_of_hits, file_data_path):
    search_string = stock_name + " site:" + source + " after:" + after + " before:" + before

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

        # Get text data based on website
        text_data = ""
        if source == "https://finance.yahoo.com/":
            click_agree_button_yahoo_finance(driver)
            click_show_more_button_yahoo_finance(driver)
            text_data = get_data_yahoo_finance(driver)

        polarity = evaluate_text_semantics(text_data)

        write_data_into_file(before, stock_name, polarity, source, file_data_path)

    driver.quit()


def main():
    date_from = '2023-02-01'
    date_to = '2023-03-01'
    number_of_hits = 1
    file_data_path = "data/stock_info.txt"

    # Only needed once to get SP500 data into CSV file
    # get_SP500_data()

    get_all_data(date_from, date_to, number_of_hits, file_data_path)


if __name__ == "__main__":
    main()

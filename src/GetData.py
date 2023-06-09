from selenium import webdriver
import pandas_market_calendars as mcal

from src.SP500DataScraper import get_SP500_data
from src.SemanticAnalysis import *
from src.WriteFile import *
from src.yahooFinance.HelperMethodsYahooFinance import *


def go_through_all_dates():
    trading_dates = get_trading_dates('2023-01-01', '2023-02-01')

    for date in trading_dates():
        pass


def get_trading_dates(start_date, end_date):
    # Create a calendar
    nyse = mcal.get_calendar('NYSE')
    dates = nyse.schedule(start_date=start_date, end_date=end_date)

    # Filter out non-trading dates
    trading_dates = dates.index.normalize()
    return trading_dates

def go_through_all_stocks():
    pass


def go_through_all_sources():
    pass


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

        # todo include real date
        write_data_into_file("2020-01-01", stock_name, polarity, source, file_data_path)

    driver.quit()


def main():
    stock_name = "AAPL"
    source = "https://finance.yahoo.com/"
    after = "2021-01-02"
    before = "2021-02-02"
    number_of_hits = 1
    file_data_path = "data/stock_info.txt"

    # Only needed once to get SP500 data into CSV file
    # get_SP500_data()

    go_through_all_dates()
    # search_stock_info(stock_name, source, after, before, number_of_hits, file_data_path)


if __name__ == "__main__":
    main()

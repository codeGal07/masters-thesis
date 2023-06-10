import pandas as pd
from bs4 import BeautifulSoup


def get_SP500_data():

    # Data in my master's thesis was extracted on date 9.6.2023

    text_file = open("data/html_sp500.txt", "r")
    html = text_file.read()

    bs = BeautifulSoup(html, features="lxml")

    table = bs.find('table', {'class': 'table table-hover table-borderless table-sm'})

    data = []  # List to store the extracted data

    # Extract data from each row in the table
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) >= 4:  # Check if the row has enough columns
            company = columns[1].text.strip()
            symbol = columns[2].text.strip()
            weight = float(columns[3].text.strip())
            data.append((company, symbol, weight))

    # Print the extracted data
    for item in data:
        print("Company:", item[0])
        print("Symbol:", item[1])
        print("Weight:", item[2])
        print("--------------------")

    # Save the data to a CSV file
    save_to_csv(data, "data\sp500_data.csv")

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=["Company", "Symbol", "Weight"])
    df.to_csv(filename, index=False)
    print("Data saved to", filename)

import os
import csv

def write_data_into_file(date, stock_name, polarity, source, title_data, current_url, file_data_path, text_data):
    # text_data = text_data.replace(',', '|')  # Replace commas with a different character

    with open(file_data_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, stock_name, polarity, title_data, source, current_url, text_data])


def create_file_if_not_exists(file_data_path):
    if not os.path.exists(file_data_path):
        with open(file_data_path, "w", newline='') as file:
            writer = csv.writer(file)
            header = ["date", "stock_name", "polarity", "title_data", "source", "url", "text_data"]
            writer.writerow(header)
            print("New file created at:", file_data_path)
    else:
        print("File already exists at:", file_data_path)
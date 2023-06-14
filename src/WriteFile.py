import os


def write_data_into_file(date, stock_name, polarity, source, title_data, current_url, file_data_path):
    with open(file_data_path, "a") as file:
        new_data_row = "{}, {}, {:.5f}, {}, {}, {}".format(date, stock_name, polarity, title_data, source, current_url)
        file.write(new_data_row + "\n")


def create_file_if_not_exists(file_data_path):
    if not os.path.exists(file_data_path):
        with open(file_data_path, "w") as file:
            header = "date, stock_name, polarity, title_data, source, url\n"
            file.write(header)
            print("New file created at:", file_data_path)
    else:
        print("File already exists at:", file_data_path)

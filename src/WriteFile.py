import os


def write_data_into_file(date, stock_name, polarity, source, file_data_path):
    with open(file_data_path, "a") as file:
        new_data_row = "{}, {}, {:.1f}, {}".format(date, stock_name, polarity, source)
        file.write(new_data_row + "\n")


def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            header = "date, stock_name, polarity, source\n"
            file.write(header)
            print("New file created at:", file_path)
    else:
        print("File already exists at:", file_path)

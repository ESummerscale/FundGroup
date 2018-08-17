import pandas as pd
from FundGroupCheckFiles import check_file_exists

def create_csv_dataframe(input_file_name):
    check_file_exists(input_file_name)
    with open(input_file_name, "r") as csv_file:
        return pd.read_csv(csv_file)
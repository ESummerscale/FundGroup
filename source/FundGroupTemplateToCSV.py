import pandas as pd
from datetime import datetime
import os

from FundGroupCheckFiles import generate_path

def format_sheet_for_csv(excel_file):
    values_list = []
    for column in excel_file.columns:
        values_list.append(column)
    values_list.append("\n")
    for row_index, row in enumerate(excel_file.iterrows()):
        for column in excel_file.columns:
            value = excel_file.iloc[row_index][column]
            if pd.isnull(value):
                values_list.append("")
            else:
                values_list.append(value)
        values_list.append("\n")
    return values_list

def open_data_sheet():
    excel_path = generate_path("Excel", "FundGroupTemplateForTest.xlsx")
    try:
        data_book = pd.read_excel(excel_path, sheet_name=2)
    except FileNotFoundError:
        print("Template file not found")
        raise SystemExit
    else:
        return data_book

def write_csv_to_folder_from_excel(file_name, excel_file):
    values_list = format_sheet_for_csv(excel_file)
    with open(file_name, "w") as f:
        for next_index, value in enumerate(values_list):
            if value == "\n" or values_list[next_index] == "\n": #Prevents comma at end of line
                f.write("{}".format(value))
            else:
                f.write("{},".format(value))
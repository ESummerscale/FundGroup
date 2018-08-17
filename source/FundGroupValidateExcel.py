import pandas as pd
import os
from dateutil.parser import parse
from FundGroupCheckDataTypes import  check_data_type, check_third_party_values, give_error_for_no_third_party_values, capture_data_type_results
from FundGroupDataTypesDict import data_types_dict
from FundGroupCheckFiles import generate_path 
from FundGroupTemplateToCSV import write_csv_to_folder_from_excel, open_data_sheet

def remove_empty_rows_from_excel_file():
    excel_file = open_data_sheet()
    for row_index, row in excel_file.iterrows():
        empty_values = 0
        for value in row:
            if pd.isnull(value):
                empty_values = empty_values + 1
        if empty_values == len(excel_file.columns):
            excel_file = excel_file.drop(excel_file.index[[-1]])
    return excel_file

def find_and_capture_errors(excel_file, data_types_dict):
    third_party_mand_dict = {}
    error_list = []
    for column in excel_file.columns.tolist():
        row_index = 2
        for value in excel_file[column]:
            if "ThirdParty" in column:
                column = "ThirdPartyX"
            third_party_mand_dict[row_index] = check_third_party_values(column, check_data_type(column, data_types_dict, value, column), third_party_mand_dict, row_index)
            if capture_data_type_results(column, row_index, data_types_dict, value):
                error_list.append(capture_data_type_results(column, row_index, data_types_dict, value))
            row_index = row_index + 1
    for item in give_error_for_no_third_party_values(third_party_mand_dict):
        error_list.append(item)
    return error_list

def write_results_to_file(error_list, excel_file):
    excel_path = generate_path("Output", "FundGroupTemplateForTest.xlsx")
    if error_list:
        errors_file_path = generate_path("Output", "FundGroupCSVErrors.csv")
        with open(errors_file_path, "w") as f:
            f.write("Errors found in {}\n".format(excel_path))
            for error in error_list:
                f.write(error + "\n")
    else:
        write_csv_to_folder_from_excel(generate_path("Output", "FundGroupValidCSV.csv"), excel_file)
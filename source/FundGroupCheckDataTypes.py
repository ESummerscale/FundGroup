import pandas as pd
from fastnumbers import fast_float, fast_int, isintlike
from dateutil.parser import parse
from datetime import datetime
from FundGroupDataTypesDict import data_types_dict

#from FundGroupDataTypesDict import get_dict_key
def open_data_sheet():
    excel_path = generate_path("Excel Template", "FundGroupTemplateForTest.xlsx")
    try:
        data_book = open_workbook(excel_path)
    except FileNotFoundError:
        print("Template file not found")
        raise SystemExit
    else:
        return data_book.sheet_by_index(2)

def check_data_type(header, data_types_dict, cell_value, dict_key):
    #dict_key = get_dict_key(header)
    valid_type = type(data_types_dict[dict_key][0])
    if pd.isnull(cell_value) and data_types_dict[dict_key][1]:
        return "Mandatory field left empty."
    elif pd.isnull(cell_value) and not data_types_dict[dict_key][1]:
        return "Empty: potential error"
    elif data_types_dict[dict_key][0] == "datetime":
        try:
            parse(cell_value)
        except ValueError:
            return "Wrong data type - \"{}\" should be {} NOT {}".format(cell_value, datetime, type(cell_value))
    elif valid_type is not type(cell_value) and\
        valid_type is not type(fast_float(cell_value)) and\
        (valid_type is int) and not (isintlike(cell_value)) and\
        (valid_type is int) and not str(cell_value).isdigit():
            return "Wrong data type - \"{}\" should be {} NOT {}".format(cell_value, type(data_types_dict[dict_key][0]), type(cell_value))
    return "Success"

def check_third_party_values(dict_key, error_check_result, mand_dict, row_num): 
    if dict_key == "ThirdPartyX" and error_check_result == "Success":
        mand_dict[row_num] = "Row not empty"
    else:
        try:
            mand_dict[row_num]
        except KeyError:
            mand_dict[row_num] = ""
    return mand_dict[row_num]

def give_error_for_no_third_party_values(third_party_mand_dict):
    error_list = []
    for row_num in third_party_mand_dict:
        if third_party_mand_dict[row_num] == "":
            error_list.append("Error in row {} - no valid ThirdParty values entered.".format(row_num))
    return error_list

def capture_data_type_results(header, row_index, data_types_dict, cell_value):
    error_check_result = check_data_type(header, data_types_dict, cell_value, header)
    if error_check_result != "Success" and error_check_result != "Empty: potential error":
        return "Error in column {}; row {} -- {}".format(header, row_index, error_check_result)
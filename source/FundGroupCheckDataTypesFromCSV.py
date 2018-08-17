import pandas as pd
from fastnumbers import fast_float, fast_int, isintlike
from dateutil.parser import parse
from datetime import datetime

from FundGroupDataTypesDict import get_dict_key

def check_data_type(dict_key, cell_value, data_types_dict):
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

def capture_data_type_results(csv_file_df, data_types_dict):
    third_party_mand_dict = {} #Dictionary used to check that at least one value is present per row in the ThirdParty columns
    error_list = []
    for header in csv_file_df.columns:
        for row_num, cell in enumerate(csv_file_df[header], 2):         
            dict_key = get_dict_key(header)
            error_check_result = check_data_type(dict_key, cell, data_types_dict)
            if error_check_result != "Success" and error_check_result != "Empty: potential error":
                error_list.append("Error in column {}; row {} under {} -- {}".format(chr(csv_file_df.columns.get_loc(header)+65), row_num, header, error_check_result))
        third_party_mand_dict[row_num] = check_third_party_values(dict_key, error_check_result, third_party_mand_dict, row_num)
    return error_list, third_party_mand_dict

def give_error_for_no_third_party_values(error_list, third_party_mand_dict):
    for row_num in third_party_mand_dict:
        if third_party_mand_dict[row_num] == "":
            error_list.append("Error in row {} - no valid ThirdParty values entered.".format(row_num))
    return error_list
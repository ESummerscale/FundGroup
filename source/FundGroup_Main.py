from fastnumbers import fast_int
import os

from FundGroupDataTypesDict import data_types_dict
from FundGroupValidateExcel import remove_empty_rows_from_excel_file, find_and_capture_errors, write_results_to_file

def main():
    excel_file = remove_empty_rows_from_excel_file()
    error_list = find_and_capture_errors(excel_file, data_types_dict)
    write_results_to_file(error_list, excel_file)

if __name__ == "__main__":
    main()
import os
from shutil import copyfile

def generate_path(folder_name, file_name=False):
    if file_name:
        path = "{}\{}\{}".format(os.pardir, folder_name, file_name)
    else:
        path = "{}\{}".format(os.pardir, folder_name)
    return path

def write_file_check_status(error_list, validated_csv_path, input_file_name):
    if error_list == []:
        with open(validated_csv_path, "a") as f:
            f.write("FileCheckStatus,Passed")
    else:
        with open(validated_csv_path, "a") as f:
            f.write("FileCheckStatus,Failed")
        errors_file_path = generate_path("ValidatedCSV", "FundGroupCSVErrors.csv")
        with open(errors_file_path, "w") as f: #FIX
            f.write("Errors found in {}\n".format(input_file_name))
            for error in error_list:
                f.write(error + "\n")

def check_file_exists(path):
    try:
        open(path)
    except FileNotFoundError:
        print("File not found")
        raise SystemExit

def copy_validated_file(input_file_name):
    path = generate_path("ValidatedCSV")
    try:
        os.makedirs(path)
    except  OSError:
        pass
    finally:
        validated_csv_path = generate_path("ValidatedCSV", "FundGroupValidatedCSV.csv")
        copyfile(input_file_name, validated_csv_path)
    return  validated_csv_path

def check_file_check_status(validated_csv_path):    
    with open(validated_csv_path, "r") as f:
        if list(f)[-1] == "FileCheckStatus,Passed":
            return True
        else:
            return False

def remove_errors_file():
    errors_file_path = generate_path("ValidatedCSV", "FundGroupCSVErrors.csv")
    try:
        os.remove(errors_file_path)
    except OSError:
        pass
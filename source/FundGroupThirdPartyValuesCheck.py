def check_third_party_cols(dict_key, error_check_result, mand_dict, row_num): 
    if dict_key == "ThirdPartyX" and error_check_result == "Success":
        mand_dict[row_num] = "Row not empty"
    else:
        try:
            mand_dict[row_num]
        except KeyError:
            mand_dict[row_num] = ""
    return mand_dict[row_num]
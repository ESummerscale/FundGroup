import pandas as pd

def create_csv_dataframe(input_file_name):
    with open(input_file_name, "r") as csv_file:
        return pd.read_csv(csv_file)

# def get_dict_key(header):
#     if header[0:10] == "ThirdParty":
#         dict_key = "ThirdPartyX"
#     else:
#         dict_key = header
#     return dict_key

data_types_dict = { #Header (datatype, mandatory/not mandatory)
    "Period": ("datetime", True),
    "Commentary": ("str", False),
    "Currency": ("str", True),
    "ThirdPartyX": (1.0, False),
    "MasterBusinessLineId": (1, False),
    "MasterFundGroupId": (1, False),
    "MasterFundGroupFriendlyName": ("str", True),
    "ICGBalanceSheetAUM": ("str", False),
    "MasterDataSourceSystemId": (1, False),
    "MasterDataProviderId": (1, False),
    "SourceSystemName": ("str", False),
    "SpreadsheetVersion": (1.0, False),
    }
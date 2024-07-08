import pandas as pd
import os


def read_excel(file_path):
    path = os.path.join(os.getcwd(), f"data\\{file_path}")
    data_frame = pd.read_excel(io=path, sheet_name="Sheet1", engine="openpyxl")
    data_dict = data_frame.set_index("模块名称").to_dict()
    print(data_dict)

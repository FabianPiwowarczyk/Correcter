"""
Program by B.Sc. Fabian Piwowarczyk, e-mail: fg.piwowarczyk@gmail.com
Version: 1.0

Functions for duplicate finder
Content:
    - return data frame of .xlsx file
    - check for duplicates in columns
    - format check
"""

# package imports
import pandas as pd
import xlsxwriter
from os.path import join
import openpyxl


def duplicates_df(file, chbx):
    """
    reader function .xlsx files

    :param file:
        file directory as str
    :param chbx:
        checkBox True or false from user input
    :return:
        pandas data frame of the .xlsx file
    """
    if chbx:
        df = pd.read_excel(file)
    else:
        df = pd.read_excel(file, header=None)
    return df


def check_duplicates(df, lt):
    """
    Main function to check for duplicates in chosen columns

    :param df:
        data frame from the .xlsx file
    :param lt:
        columns to check
    :return:
        list of idx that contain duplicates (+1 to align with xlsx idx's)
    """
    dt = df.duplicated(subset=lt, keep=False)
    idx = [x +1 for x in dt.index[dt].tolist()]
    return idx


def check_xlsx(file):
    """
    checks the format of the file

    :param file:
        file directory as str
    :return:
        True or False
    """
    if file.split('.')[1] != 'xlsx':
        return False
    else:
        return True

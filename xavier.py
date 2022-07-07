"""
Program by B.Sc. Fabian Piwowarczyk, e-mail: fg.piwowarczyk@gmail.com
Version: 1.0

Saving routine for pandas data frame in .xlsx file.
Content:
    - safe function
"""

# package imports
import pandas as pd
import xlsxwriter
from os.path import join


def safe_df(df, dir):
    """
    Save function

    :param df:
        pandas data frame with file data
    :param dir:
        directory for saving
    :return:
        saves data
    """
    df.to_excel(join(dir, "output.xlsx"), engine='xlsxwriter', index=False)
import pandas as pd
import xlsxwriter


def safe_df(df):

    df.to_excel("output.xlsx", engine='xlsxwriter')
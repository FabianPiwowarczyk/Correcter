from os.path import join
from main_fkt import start_fkt

start_fkt()

import pandas as pd




#
# # the first line is the first line of column headers
# col_headers = re.split(r' +', lines[0])[1:]
# print(len(col_headers))
# col_headers.insert(2, re.split(r' +', lines[1])[2])
# print(col_headers)
#
# # third line and on are the data lines
# lines = lines[2:]
#
# # average values are every four lines
# avg_lines = lines[::2]
# # the lines with the time (and sddev values) are the ones immediately following the average value lines
# time_lines = lines[1::2]
#
# # columns are 11 characters wide, except the first two
# col_widths = [7, 15] + [11] * (len(col_headers) - 2)
#
#
# def col_values_iter(line, col_widths):  # read fixed-width column values
#     i = 0
#     for w in col_widths:
#         start = i
#         end = i + w
#         yield line[start:end].lstrip()
#         i += w
#
#
# def col_values(line, col_widths):
#     return list(col_values_iter(line, col_widths))
#
#
# # now assemble the rows of the dataframe
# rows = []
#
# for al, tl in zip(avg_lines, time_lines):
#     cvs = col_values(al, col_widths)
#     print(len(cvs))
#     time = col_values(tl, col_widths)[1]  # just use the first value
#     cvs.insert(2, time)
#     rows.append(cvs)
#
# print(rows)
# df = pd.DataFrame(rows, columns=col_headers)
# print(df.head())
#
# df.to_excel("output.xlsx", engine='xlsxwriter')

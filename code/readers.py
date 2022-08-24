"""
Program by B.Sc. Fabian Piwowarczyk, e-mail: fg.piwowarczyk@gmail.com
Version: 1.0

Reader function for converter
Content:
    - reader for .ros and .btl files
"""

# package imports
import numpy as np
import pandas as pd
from os.path import join

# program intern functions
from code.general_use_func import get_frmt, get_file_values, get_btl_heads


def reader(indir, filelist, form, file_h):
    """
    Main reader function

    :param indir:
        directory of folder with files as str
    :param filelist:
        list of files as str
    :param form:
        data format (.ros / .btl)
    :param file_h:
        user input for headers in file name as str
    :return:
        returns data frame from multiple files in one data frame
    """

    frmt, heads_f = get_frmt(file_h)  # returns format to search head values from file name and headers from file name

    if form == 'ros':  # determines which readers routine is used
        df = reader_ros(indir, filelist, frmt, heads_f)

    if form == 'btl':
        df = reader_btl(indir, filelist, frmt, heads_f)

    return df  # returns data frame


def reader_ros(indir, filelist, frmt, heads_f):
    """
    Reads .ros files and collects data from multiple files in one data frame

    :param indir:
        directory of folder with files as str
    :param filelist:
        list of files as str
    :param frmt:
        format to search head values from file name
    :param heads_f:
        headers form file name
    :return:
        returns data frame from multiple files in one data frame
    """
    col_headers = []  # list of column headers
    col_headers.extend(heads_f)
    with open(join(indir, filelist[0]), 'r') as f:
        for line in f.readlines():
            if 'name' in line:  # all lines with 'name' contain headers
                col_headers.append(line.split()[4])

    lines = []
    for file in filelist:
        head_values = get_file_values(frmt, file, heads_f)  # separates values from file names
        with open(join(indir, file)) as fp:
            eline = [head_values + l.rstrip().split() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]
        lines.extend(eline)

    lines = np.asarray(lines)
    df = pd.DataFrame(lines, columns=col_headers)

    return df


def reader_btl(indir, filelist, frmt, heads_f):
    """
    Reads .btl files and collects data from multiple files in one data frame
    :param indir:
        directory of folder with files as str
    :param filelist:
        list of files as str
    :param frmt:
        format to search head values from file name
    :param heads_f:
        headers form file name
    :return:
        returns data frame from multiple files in one data frame
    """

    data = dict()

    headers = get_btl_heads(join(indir, filelist[0]), heads_f)

    for file in filelist:
        head_values = get_file_values(frmt, file, heads_f)
        with open(join(indir, file), encoding='cp437') as fp:  # read out all data lines
            lines = [l.rstrip() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]

        lines = lines[2:]  # cut of header lines

        avg_lines = lines[::2]  # cut out sdev lines

        def separate_avg_line(line):
            """
            Separate values in one line

            :param line:
                line as str
            :return:
                list with values from line
            """
            return head_values + [line[i:i + 11].strip() for i in range(0, len(line), 11)][:-1]

        values = []
        for line in avg_lines:
            values.append(separate_avg_line(line))

        data[file] = [headers, values]

    df = pd.DataFrame(data[filelist[0]][1], columns=data[filelist[0]][0])
    for key in filelist[1:]:
        df = df.append(pd.DataFrame(data[key][1], columns=data[key][0]), ignore_index=True)

    return df  # return data frame

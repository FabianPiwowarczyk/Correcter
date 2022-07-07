"""
Program by B.Sc. Fabian Piwowarczyk, e-mail: fg.piwowarczyk@gmail.com
Version: 1.0

General functions for converter
Content:
    - get functions
    - check functions
    - save config
"""

# package imports
from os import listdir
from os.path import isfile, join
import re
import json


def get_file_list(dir):
    """
    :param dir:
        directory with files
    :return:
        list with strings of file names in dir
    """
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    onlyfiles.sort()
    return onlyfiles


def check_format(filelist):
    """
    Check for formats

    :param filelist:
        list of files
    :return:
        format of files and bool if all files have the same format
    """
    check = True
    form = filelist[0].split('.')[1]
    for file in filelist:
        if form != file.split('.')[1]:
            check = False
        else:
            continue
    return form, check


def get_frmt(file_h):
    """
    Gets format for values in the file names for separation
    :param file_h:
        user input str
    :return:
        format for separation and headers from file name
    """
    lst1 = [i for i, s in enumerate(file_h) if '{' in s]
    lst2 = [i for i, s in enumerate(file_h) if '}' in s]
    if len(lst1) != len(lst2):  # false user input
        frmt = None
        heads_f = False
        return frmt, heads_f
    else:
        heads_f = []
        trash = []
        tidx = 0
        for idx in zip(lst1, lst2):
            heads_f.append(file_h[idx[0] + 1: idx[1]])

            trash_str = file_h[tidx:idx[0]]
            tidx = idx[1] + 1
            trash.append(trash_str)
        trash_str = file_h[tidx:]
        trash.append(trash_str)

        frmt = ''
        for ele in trash:
            frmt = frmt + ele + '(.*)'
        return frmt[:-4], heads_f


def get_file_values(frmt, file, heads_f):
    """
    :param frmt:
        search format
    :param file:
        file as str
    :param heads_f:
        headers in file name
    :return:
        header values in file name
    """
    search = re.search(frmt, file)
    counts = [search.group(i + 1) for i in range(len(heads_f))]
    return counts


def get_btl_heads(file, heads_f):
    """
    Read headers form btl files and use correcting algorithm

    :param file:
        file name as str
    :param heads_f:
        headers from file name
    :return:
        list of headers
    """
    with open(file, encoding='cp437') as fp:
        heads = [l.rstrip() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]  # read all lines
    heads = [heads[0][i:i + 11] for i in range(0, len(heads[0]), 11)]  # separate headers in first line (width 11)

    # correcting headers that are bigger than 11 char in a loop
    temp_headers = []
    while heads:
        if len(heads[0].strip().split()) == 1:
            temp_headers.append(heads[0].strip())
            heads = heads[1:]
        else:
            temp_headers[-1] = temp_headers[-1] + heads[0].split()[0]
            err = len(heads[0].split()[0])

            for i in range(len(heads) - 1):
                heads[i] = heads[i][err:] + heads[i + 1][:err]
            heads = heads[:-1]
    headers = []
    headers.extend(heads_f)
    headers.extend(temp_headers)
    return headers


def save_config(l):
    """
    :param l:
        list of headers in config
    :return:
        save file with config
    """
    with open("config.json", "w") as fp:
        json.dump(l, fp)


def get_config():
    """
    loads config for output layout

    :return:
        list of headers
    """
    with open("config.json", "r") as fp:
        config = json.load(fp)
    return config


def check_file_values(file_h, filelist):
    """
    Checks if all names can be read with the format from user input.
    (This function is a mess and needs a makeover, but it works)

    :param file_h:
        user input for file name
    :param filelist:
        list of file names
    :return:
        bool if file_h can be read, bool if file values can be read and frmt for separation
    """
    file_n = None
    try:
        check = True
        frmt, heads_f = get_frmt(file_h)
        if frmt:
            for f in filelist:
                if check:
                    try:
                        get_file_values(frmt, f, heads_f)
                    except:
                        check = False
                        file_n = f
                else:
                    continue
        else:
            frmt = False
            check = False
    except:
        frmt = False
        check = False
    return check, file_n, frmt


def check_col_header(form, indir, filelist):
    """
    Checks if all files include the same headers

    :param form:

    :param indir:
        directory of files
    :param filelist:
        list of file names
    :return:
         bool if all files contain same header and str with first file that does not
    """
    f = False
    check = True
    if form == 'ros':
        with open(join(indir, filelist[0]), 'r') as fp:
            headlist = [l.split()[4] for l in fp.readlines() if 'name' in l]
        for file in filelist:
            if not f:
                with open(join(indir, file), 'r') as fp:
                    if headlist != [l.split()[4] for l in fp.readlines() if 'name' in l]:
                        check = False
                        f = file
            else:
                continue

    if form == 'btl':
        with open(join(indir, filelist[0]), encoding='cp437') as fp:
            lines = [l.rstrip() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]
        headlist = [lines[0][i:i + 11] for i in range(0, len(lines[0]), 11)]
        for file in filelist:
            if not f:
                with open(join(indir, file), encoding='cp437') as fp:
                    lines = [l.rstrip() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]
                    if headlist != [lines[0][i:i + 11] for i in range(0, len(lines[0]), 11)]:
                        check = False
                        f = file
            else:
                continue
    return check, f

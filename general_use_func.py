from os import listdir
from os.path import isfile, join


def get_file_list(dir):
    """
    input: direction where the files are.
    output: list with all file names in this direction, as strings
    """
    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    onlyfiles.sort()
    return onlyfiles


def check_format(filelist):
    i = 0
    form = None
    for ele in filelist:
        if i == 0:
            form = ele.split('.')[1]
            i+=1
        if i > 0:
            if form != ele.split('.')[1]:
                print('Not all files in this directory have the same format')
                raise ValueError
    return form


def check_col_header(indir, filelist, col_header, form):
    pass
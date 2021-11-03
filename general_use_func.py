from os import listdir
from os.path import isfile, join


def file_list(dir):
    """
    input: direction where the files are.
    output: list with all file names in this direction, as strings
    """
    cond = True
    while cond:
        try:
            onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
            onlyfiles.sort()
            cond = False
        except:
            print('There is no directory: ', dir)
            dir = input('Please enter valid directory: ')
    return onlyfiles, dir


def check_format(filelist):
    i = 0
    form = None
    for ele in filelist:
        if i == 0:
            form = ele[-3:]
            i+=1
        if i > 0:
            if form != ele[-3:]:
                print('Not all files in this directory have the same format')
                raise ValueError
    return form


def check_col_header(indir, filelist, col_header, form):
    pass
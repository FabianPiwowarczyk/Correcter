from general_use_func import file_list, check_format
from readers import reader


def start_fkt():

    indir = '../files_for_correcter/ros'

    filelist, indir = file_list(indir)
    form = check_format(filelist)

    data = reader(indir, filelist, form)





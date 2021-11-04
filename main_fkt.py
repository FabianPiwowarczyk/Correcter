from general_use_func import file_list, check_format
from readers import reader


def start_fkt():

    indir = '../files_for_correcter/MSM65_wahrheit_wahrheit'

    filelist, indir = file_list(indir)
    form = check_format(filelist)

    data = reader(indir, filelist, form)





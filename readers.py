import pandas as pd
import xlsxwriter
from os.path import join
from general_use_func import check_col_header


def reader(indir, filelist, form):
    if form == 'ros':
        col_headers = []
        with open(join(indir, filelist[0]), 'r') as f:
            for line in f.readlines():
                if 'name' in line:
                    col_headers.append(line.split()[4])

        check_col_header(indir, filelist, col_headers, form)

        lines = []
        for file in filelist:
            with open(join(indir, file)) as fp:
                for l in fp.readlines():
                    if l.startswith('#') or l.startswith('*'):  # skip header lines
                        continue
                    lines.append(l.rstrip().split())

        df = pd.DataFrame(lines, columns=col_headers)
        df.to_excel("output.xlsx", engine='xlsxwriter')

    if form == 'btl':
        pass

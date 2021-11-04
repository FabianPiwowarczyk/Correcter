import pandas as pd
import xlsxwriter
from os.path import join
from general_use_func import check_col_header


def reader(indir, filelist, form):
    if form == 'ros':
        reader_ros(indir, filelist)

    if form == 'btl':
        reader_btl(indir, filelist)


def reader_ros(indir, filelist):
    col_headers = []
    with open(join(indir, filelist[0]), 'r') as f:
        for line in f.readlines():
            if 'name' in line:
                col_headers.append(line.split()[4])

    check_col_header(indir, filelist, col_headers)

    lines = []
    for file in filelist:
        with open(join(indir, file)) as fp:
            lines = [l.rstrip().split() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]

    df = pd.DataFrame(lines, columns=col_headers)
    df.to_excel("output.xlsx", engine='xlsxwriter')


def reader_btl(indir, filelist):
    data = dict()

    for file in filelist:
        with open(join(indir, file), encoding='cp437') as fp:
            lines = [l.rstrip() for l in fp.readlines() if not (l.startswith('#') or l.startswith('*'))]

        heads = [lines[0][i:i + 11] for i in range(0, len(lines[0]), 11)]
        headers = []

        while heads:
            if len(heads[0].strip().split()) == 1:
                headers.append(heads[0].strip())
                heads = heads[1:]
            else:
                headers[-1] = headers[-1] + heads[0].split()[0]
                err = len(heads[0].split()[0])

                for i in range(len(heads) - 1):
                    heads[i] = heads[i][err:] + heads[i + 1][:err]
                heads = heads[:-1]

        lines = lines[2:]

        avg_lines = lines[::2]

        def separate_avg_line(line):
            return [line[i:i + 11].strip() for i in range(0, len(line), 11)][:-1]

        values = []
        for line in avg_lines:
            values.append(separate_avg_line(line))

        data[file] = [headers, values]

    check_head = [data[filelist[0]][0] == data[key][0] for key in filelist]
    if False in check_head:
        raise ValueError

    df = pd.DataFrame(data[filelist[0]][1], columns=data[filelist[0]][0])
    for key in filelist[1:]:
        df = df.append(pd.DataFrame(data[key][1], columns=data[key][0]), ignore_index=True)

    print(df.head(5))
    df.to_excel("output.xlsx", engine='xlsxwriter')
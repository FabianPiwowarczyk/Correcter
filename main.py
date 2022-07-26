"""
Program by B.Sc. Fabian Piwowarczyk, e-mail: fg.piwowarczyk@gmail.com
Version: 1.0

Main file for execution of the converter project.
Content:
    - GUI code
    - main execution
    - main interface for all code
"""

# package imports
from appJar import gui  # GUI package

# program intern functions
from general_use_func import get_file_list, check_format, get_config, save_config, check_file_values, check_col_header
import readers as rd
import xavier as sf
from duplicates import duplicates_df, check_duplicates, check_xlsx


def open_dic(bnt):
    """
    Button function to open a directory box and selecting directory.

    :param bnt:
        defines button function
    :return:
        sets path entry to selected directory
    """
    directory = app.directoryBox('open_dir')  # choose directory
    app.setEntry('path', directory)  # set path Entry to directory


def open_file(btn):
    """
    Button function to open file directory box and selecting .xlsx  file.

    :param btn:
        defines button function
    :return:
        sets Filedir entry to selected file directory
    """
    xslxfile = app.openBox(title='open_file', fileTypes=[('excel worksheets', '*.xlsx')])  # choose file directory
    app.setEntry('Filedir', xslxfile, callFunction=False)  # set Filedir entry to file directory


def get_entry(bnt):
    """
    Primary button function for converter.

    :param bnt:
        defines button function
    :return:
        opens subwindow to select data header in file names by user input
    """
    app.destroyAllSubWindows()  # destroying all subwindows to guarantee functionality after canceling mid process

    def get_header(bnt):
        """
        Secondary button function for converter.

        :param bnt:
            defines button function
        :return:
            opens subwindow to select format for the output .xlsx file
        """

        def get_options(bnt):
            """
            Tertiary button function for converter.

            :param bnt:
                defines button function
            :return:
                reads the format and saves data frame as .xlsx file.
            """
            lt = app.getAllOptionBoxes()  # gets user input form option boxes as dict()
            new_heads = [ele for ele in list(lt.values()) if ele != 'empty']  # list of all chosen headers for output
            df_safe = df[new_heads]  # reframes data frame with new headers

            sf.safe_df(df_safe, dir)  # saves data frame as output.xlsx
            save_config(df_safe.columns.tolist())  # saves used config
            app.hideSubWindow('header', useStopFunction=True)

            app.infoBox('Saved', 'Your output has been saved!', parent=None)  # end of converter, returns to start

        file_h = app.getEntry('name')  # gets name entry str
        app.hideSubWindow('file_name', useStopFunction=True)  # closes subwindow

        check2, file, forma = check_file_values(file_h, file_list)  # checks if all file names can be read
        if check2:  # check file name
            check3, file = check_col_header(form, dir, file_list)  # checks if all files include the same column headers
            if check3:  # check column headers
                df = rd.reader(dir, file_list, form, file_h)  # reader function extracts all data in pandas data frame

                app.startSubWindow("header", modal=True)  # starts subwindow to format the output file
                app.setSticky('new')
                app.setStretch('column')

                for i, _ in enumerate(df.columns.tolist()):  # add option box for every header in data frame
                    app.addLabelOptionBox(i, ['empty'] + df.columns.tolist())

                try:
                    config = get_config()  # gets last used config for output format
                except:
                    app.infoBox('config', 'No config.json can be found.')
                for ii, ele in enumerate(config):  # add config in option boxes
                    if ele in df.columns.tolist():  # only adds header from config that exist in the data frame
                        app.setOptionBox(ii, ele)
                    else:  # header does not exist in data frame
                        continue

                app.addButton('save', get_options, column=0, colspan=0, row=i + 1)  # calls tertiary button function
                app.stopSubWindow()  # close subwindow
                launch('header')  # launch subwindow
            else:  # failed check column headers
                app.infoBox('file_heads', f'A file does not contain the same column headers as the other: {file}')
                app.destroyAllSubWindows()
        else:  # fails file name check
            if not forma:  # the user input the wrong format for the file name
                app.infoBox('head_format', f'The format for the file heads is invalid: {file_h}')
                app.destroyAllSubWindows()
            else:  # values from file name can not be read
                app.infoBox('head_value_check', f'Values from file name cannot be read: {file}', parent=None)
                app.destroyAllSubWindows()

    dir = app.getEntry('path')  # gets path entry

    file_list = get_file_list(dir)  # gets list of files in dir as str
    form, check1 = check_format(file_list)  # checks if all files have a fitting format

    if check1:  # check file format
        app.startSubWindow('file_name', modal=True)  # starts subwindow for selecting data headers in file names
        app.setSticky('new')
        app.setStretch('column')
        app.addLabel('lbl1', 'Add headers', 0, 0, 1)
        app.addEntry('name', 1, 0, 2)  # entry for editing file name
        app.setEntry('name', file_list[0], callFunction=False)  # set file name entry to first file name in file_list
        app.setEntryWidths('name', 40)
        app.addButton('get header', get_header, 1, 2)  # calls secondary button function
        app.stopSubWindow()  # end subwindow
        launch('file_name')  # launch the subwindow
    else:  # file format fail infobox
        app.infoBox('form_check', f'One of your files does not have the right format: {form}', parent=None)


def duplicates(bnt):
    """
    Primary button function to check duplicates in .xlsx file

    :param bnt:
        defines button function
    :return:
        checks for duplicates
    """
    app.destroyAllSubWindows()  # re-usability

    def check_dups(bnt):
        """
        Secondary button function to check duplicates

        :param bnt:
            defines button function
        :return:
            opens pop-up window with duplicates if any
        """
        lt = app.getAllOptionBoxes()  # returns dict() with columns
        if chbx:  # if headers
            to_check = [ele for ele in list(lt.values()) if ele != 'empty']
        else:  # if no headers
            to_check = [int(ele) for ele in list(lt.values()) if ele != 'empty']
        if to_check:  # if columns were selected
            idx = check_duplicates(df, to_check)  # returns list of idx for duplicates
            if idx:  # contains duplicates
                app.infoBox('found', f'The input columns contain duplicate values in row: {idx}')
            else:  # contains no duplicates
                app.infoBox('clear', 'The input columns contain no duplicates.')

            app.hideSubWindow('duplicates', useStopFunction=True)
            app.destroyAllSubWindows()  # end of function
        else:  # no columns selected
            app.infoBox('no_col', 'You did not select any columns.')
            app.hideSubWindow('duplicates', useStopFunction=True)
            app.destroyAllSubWindows()

    file = app.getEntry('Filedir')  # gets directory of the file
    check4 = check_xlsx(file)  # checks for correct format
    if check4:  # if correct format
        chbx = app.getCheckBox('headers')  # user input if file has headers
        df = duplicates_df(file, chbx)  # reads file and returns data frame
        app.startSubWindow('duplicates', modal=True)  # starts subwindow for column choice
        app.addLabel('Lbl1', 'Input the columns to check:', row=0, colspan=3)
        app.addLabelOptionBox('col1', ['empty'] + df.columns.tolist(), row=1, column=0, colspan=1)  # column 1
        app.addLabelOptionBox('col2', ['empty'] + df.columns.tolist(), row=1, column=2, colspan=1)  # column 2
        app.addButton('run', check_dups, row=2)  # checks for duplicates in selected columns
        app.stopSubWindow()
        launch('duplicates')
    else:  # failed format check
        app.infoBox('wrong_format', 'The file you selected was not in .xlsx format.')


def launch(win):
    """
    :return:
        launches subwindow
    """
    app.showSubWindow(win)


if __name__ == '__main__':
    """
    Main window:
        selection of file or directory 
    """
    app = gui("File Converter")
    app.setSticky('ew')
    app.setSize(600, 200)
    app.setStretch('column')
    app.addLabel('Title1', 'Converter:', row=0, column=0, colspan=3)
    app.addEntry('path', row=1, column=0, colspan=2)  # entry for dir
    app.setEntryDefault('path', '-- directory --')
    app.setStretch('none')
    app.addButton('open directory', open_dic, row=1, column=2, colspan=1)  # button for directoryBox
    app.addButton('convert', get_entry, row=2, column=2, colspan=1)  # button starts converter
    app.setStretch('column')
    app.addLabel('Title2', 'Check for duplicates:', row=4, column=0, colspan=3)
    app.addEntry('Filedir', row=5, column=0, colspan=2)  # entry for file
    app.setEntryDefault('Filedir', '-- file path --')
    app.setStretch('none')
    app.addButton('open file', open_file, row=5, column=2)  # button for fileBox
    app.addCheckBox('headers', row=6, column=2, colspan=1)  # check box if file contains header
    app.setCheckBox('headers', True)
    app.addButton('check', duplicates, row=7, column=2, colspan=1)  # button starts duplicate finder

    app.go()

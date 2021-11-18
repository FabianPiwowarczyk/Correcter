from appJar import gui
from general_use_func import get_file_list, check_format
import readers as rd
import xavier as sf


def add_dir(btn):
    filename = app.directoryBox(title=None, dirName='/home/fabian/Schreibtisch/Arbeit/', parent=None)
    app.setEntry('path', filename)


def get_entry(bnt):

    def get_options(bnt):
        lt = app.getAllOptionBoxes()  # returns dict()
        new_heads = [ele for ele in list(lt.values()) if ele is not None]
        df_safe = df[new_heads]

        sf.safe_df(df_safe)
        app.hideSubWindow("one")

        app.infoBox('Saved', 'Your output has been saved!', parent=None)

    dir = app.getEntry('path')

    file_list = get_file_list(dir)
    form = check_format(file_list)
    df = rd.reader(dir, file_list, form)

    app.startSubWindow("one", modal=True)
    app.setSticky("new")
    app.setStretch("column")

    for i, _ in enumerate(df.columns.tolist()):
        app.addLabelOptionBox(i, ['- empty -'] + df.columns.tolist())

    app.addButton('save', get_options, column=0, colspan=0, row=i + 1)

    app.stopSubWindow()

    launch('one')




def launch(win):
    app.showSubWindow(win)


app = gui("File Converter")
app.setSticky("new")
app.setStretch("column")
app.addEntry('path', 0, 0, 2)
app.setEntryWidths('path', 40)
app.setEntryDefault('path', 'path')
app.addButton('Choose path', add_dir, 0, 2)
app.setButtonWidths('Choose path', 15)
app.addButton('get entry', get_entry, 1, 2)
app.setButtonWidths('get entry', 15)

app.go()

# start_fkt()

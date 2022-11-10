#!/bin/bash

# funtion to colore echo's
function col_echo () {
    GREEN="\e[0;32m"
    NC="\033[0m"
    STR=$1
    echo -e "${GREEN} $STR${NC}"
}

function inst_miniconda3 () {
    # downloading miniconda
    col_echo "Downloading miniconda3 installer."
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    col_echo "Installing miniconda3."
    bash ~/miniconda.sh -b -p
    col_echo "Removing miniconda3 installer."
    rm ~/miniconda.sh

    col_echo "Activating conda env."
    source $HOME/miniconda3/bin/activate
    return 1
}

function try_sourcing () {
    source $HOME/miniconda3/bin/activate
}

col_echo "Try activating conda env."
try_sourcing || inst_miniconda3
CHECK_CONDA=$? # Is 0 if miniconda already installed, 1 if installation was needed

# setting up conda env
col_echo "Setting up conda env with python3 and pip"
conda create --name py3 python=3 pip
# activating conda py3
col_echo "Activating py3"
conda activate py3
# PyInstaller
col_echo "Installing required packages."
pip3 install -r code/requirements.txt
col_echo "Executing pyinstaller."
pyinstaller --onefile --windowed main.py
col_echo "Sorting folder."
mv dist/main main_lin
mv main.py code/main.py
rm -r build
rm -r dist
rm main.spec

col_echo "Deactivating py3"
conda deactivate

# Removing miniconda3 if not installed before
if [ "1" = "$CHECK_CONDA" ]; then
    col_echo "Removing miniconda3 and .conda"
    rm -r ~/miniconda3/
    rm -r ~/.conda/
fi

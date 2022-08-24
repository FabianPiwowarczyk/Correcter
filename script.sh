#!/bin/bash

function installing () {
    PKG="$1"
    PKG_STATUS=$(dpkg-query -W --showformat='${Status}\n' $PKG|grep "install ok installed")
    echo Checking for $PKG: $PKG_STATUS
    if [ "" = "$PKG_STATUS" ]; then
	echo "No $PKG. Installing $PKG."
	sudo apt-get --yes install $PKG
	CHECK=1
    else
	CHECK=0
    fi
    return $CHECK
}

installing "python3"
CHECK_PY=$?
echo "$CHECK_PY"
installing "pyinstaller"
CHECK_PYIN=$?
echo "$CHECK_PY"
echo "$CHECK_PYIN"

pyinstaller --onefile main.py
mv dist/main main
mv main.py code/main.py
rm -r build
rm -r dist
rm main.spec

if [ "$CHECK_PYIN" == "0" ]; then
    sudo apt-get remove pyinstaller
fi

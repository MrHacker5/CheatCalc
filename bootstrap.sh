#!/bin/sh
cd /home/pi/drive2raspi/

EXIT="exit.txt"
if [ -e $EXIT ]; then
    rm $EXIT
fi

python3 ./CheatCalc/cheatCalc.py

if [ -e $EXIT ]; then
    value=`cat $EXIT`
    if value="shutdown"; then
        sudo shutdown -h now
    elif value="update"; then
        sh sync.sh
        sh bootstrap.sh
    fi
    rm $EXIT
fi
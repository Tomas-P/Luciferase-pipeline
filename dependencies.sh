#!/bin/bash
set -e
echo -e "This script installs the dependencies for the luciferase program"
echo -e "those dependencies are:"
echo -e "* tkinter\n* pip\n* python3\n* java\n* numpy\n* matlplotlib"
echo -e "* cython\n* pyjnius"
echo -e "Would you like to continue? [y/n]"
read response
first=${response:0:1}
low=$(echo $first | tr '[:upper:]' '[:lower:]')
if [ $low = n ]
then
    exit
fi

pkexec apt-get install python3 python3-tk python3-pip default-jdk
pip3 install numpy matplotlib Cython
pip3 install PyJnius

ij=$(find $HOME -name Fiji.app)

if [ -z $ij ]
then
    echo "Fiji needed"
    if [ $(uname -m) = "x86_64" ]
    then
        url="https://downloads.imagej.net/fiji/latest/fiji-linux64.zip"
    elif [ $(uname -m) = "x86" ]
    then
        url="https://downloads.imagej.net/fiji/latest/fiji-linux32.zip"
    else
        echo "what are you doing in my swamp?"
        uname -m
        exit
    fi
    here=$(pwd)
    cd $HOME
    wget $url
    zip=$(find $HOME -name "fiji*.zip")
    unzip $zip
    echo "feel free to move the Fiji folder around,"
    echo "so long as you keep it in your home folder"
    rm $zip
else
    echo "all done"
fi


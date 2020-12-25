#!/bin/bash

set -euo pipefail

if ! command -v python3
then 
	pkexec apt-get install python3 -y
fi

if ! command -v pip3
then
	pkexec apt-get install python3-pip -y
fi


if ! dpkg -l | grep python3-venv
then
	pkexec apt-get install python3-venv -y
fi

if ! dpkg -l | grep python3-tk 
then
	pkexec apt-get install python3-tk -y
fi

cd "$HOME/Documents"
# these are underscores and not spaces, can't you tell?
if [ ! -d luciferase_pipeline_installation_folder ];
then
	mkdir luciferase_pipeline_installation_folder
fi

cd luciferase_pipeline_installation_folder

python3 -m venv $(pwd)
source bin/activate

if ! pip3 list | grep numpy
then
	pip3 install numpy
fi

if ! pip3 list | grep matplotlib
then
	pip3 install matplotlib
fi

if ! pip3 list | grep pyjnius
then
	pip3 install pyjnius
fi

deactivate

FILEID="18LdiTBg9rJRLTQKGzqdgZXQfWWeb6kF4"

FILENAME="luc.tar.gz"

wget --save-cookies cookies.txt \
    'https://drive.google.com/uc?export=download&id='$FILEID -O algo
CONFIRM=$(sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1/p' algo)

wget --load-cookies cookies.txt -O $FILENAME \
    'https://drive.google.com/uc?export=download&id='$FILEID'&confirm='$CONFIRM

rm algo
rm cookies.txt

tar -xzf $FILENAME

mv Program/* .
rm $FILENAME
chmod +x run.sh
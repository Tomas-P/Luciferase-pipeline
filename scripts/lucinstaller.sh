#!/bin/bash

#set -euo pipefail

pkexec apt-get install python3 python3-pip python3-venv python3-tk default-jdk -y

if [ ! -d ./luc];
then
	mkdir luc
fi
cd luc

python3 -m venv $(pwd)
source bin/activate
pip3 install numpy matplotlib pyjnius
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



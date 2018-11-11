#!/usr/bin/env bash

# install python dependencies
sudo apt-get install python3 && sudo apt-get install python3-pip && sudo pip3 install numpy && sudo pip3 install pandas && sudo pip3 install matplotlib && sudo apt-get install python3-tk

# install ImageJ
if [ ! -d ~/Fiji.app ]; then
	cd ~
	wget https://downloads.imagej.net/fiji/latest/fiji-linux64.zip
	unzip fiji-linux64.zip
	rm fiji-linux64.zip
fi

echo dependencies installed
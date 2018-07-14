#!/bin/bash

# install dependencies unless already installed
which python3 || sudo apt-install python3
which pip3 || sudo apt-get install python3-pip
pip3 list --format=columns | grep numpy || sudo pip3 install numpy
pip3 list --format=columns | grep pandas || sudo pip3 install pandas
pip3 list --format=columns | grep matplotlib || sudo pip3 install matplotlib

# Install Imagej if not present
if [ ! -d ~/Fiji.app ]; then
	cd ~
	curl -O https://downloads.imagej.net/fiji/latest/fiji-linux64.zip
	unzip fiji-linux64.zip
	rm fiji-linux64.zip
fi

echo "Dependencies installed!"

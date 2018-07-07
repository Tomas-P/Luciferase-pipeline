#!/bin/bash
# save the current directory
here=$(pwd)

# Check if python3 is installed,
# and install it if it is not.
which python3 && echo Python 3 installed || sudo apt-get install python3 && echo Python 3 installed;

# Check if Python 3 pip is installed,
# and install it if it is not
which pip3 && echo Python 3 pip installed || sudo apt-get install python3-pip && echo Python 3 pip installed;

# Install numpy
sudo pip3 install numpy

# Install pandas
sudo pip3 install pandas

# Install matplotlib
sudo pip3 install matplotlib

# move to the home path
cd ~

# check if Fiji is installed and install it if it is not
cat ~/Fiji.app/ImageJ2.desktop && echo ImageJ installed || curl -O https://downloads.imagej.net/fiji/latest/fiji-linux64.zip && unzip fiji-linux64.zip && rm fiji-linux64.zip && echo ImageJ successfully installed

# go back to the starting directory
cd $here

# Announce completion
echo Dependencies have been installed!

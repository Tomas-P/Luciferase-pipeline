#!/bin/bash
# save the current directory
here=$(pwd)

# Check if python3 is installed,
# and install it if it is not.
which python3 && echo Python 3 installed || sudo apt-get install python3 && echo Python 3 pip installed;

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

# download imagej to the home folder
curl -O https://downloads.imagej.net/fiji/latest/fiji-linux64.zip

# unpack the archive, yielding a Fiji.app folder
unzip fiji-linux64.zip

# delete the zip file
rm fiji-linux64.zip

# go back to the starting directory
cd $here

# Announce completion
echo Dependencies have been installed!
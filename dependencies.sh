#!/bin/bash

apt-get install python3
apt-get install python3-pip
apt-get install default-jdk
apt-get install wget
apt-get install git

oldpos=$(pwd)
apt-get install wget
cd ~
wget https://downloads.imagej.net/fiji/latest/fiji-linux64.zip
unzip fiji-linux64.zip

pip3 install numpy
pip3 install matplotlib
pip3 install Cython

env JAVA_HOME=/usr/lib/jvm/default-java

pip3 install PyJnius

cd $oldpos
if [ ! -f "./luciferase.py"]; then
	git clone https://github.com/Tomas-P/Luciferase-pipeline.git
fi

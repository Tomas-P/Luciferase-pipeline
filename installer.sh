#!/usr/bin/bash

apt-get install -y wget git python3 python3-tk python3-pip default-jdk
pip3 install numpy matplotlib Cython
export JAVA_HOME=/usr/lib/jvm/default-java
pip3 install PyJnius
here=$(pwd)
cd $HOME
wget https://downloads.imagej.net/fiji/latest/fiji-linux64.zip
unzip fiji-linux64.zip
rm fiji-linux64.zip
cd $here
git clone https://github.com/Tomas-P/Luciferase-pipeline.git

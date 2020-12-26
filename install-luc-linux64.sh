#!/bin/bash

cd $HOME

if test ! -d LuciferasePipeline
then
	mkdir  LuciferasePipeline
fi

cd LuciferasePipeline

wget "https://github.com/Tomas-P/Luciferase-pipeline/archive/master.zip"

unzip "master.zip"

mv Luciferase-pipeline-master/* .

rmdir "Luciferase-pipeline-master"

rm "master.zip"

pkexec apt-get install python3 python3-pip python3-venv python3-tk default-jdk -y

python3 -m venv .

source bin/activate

pip3 install -r requirements.txt

deactivate

wget "https://downloads.imagej.net/fiji/latest/fiji-linux64.zip"

unzip "fiji-linux64.zip"

wget "https://download.java.net/java/GA/jdk15.0.1/51f4f36ad4ef43e39d0dfdbaf6549e32/9/GPL/openjdk-15.0.1_linux-x64_bin.tar.gz"

tar -xzf "openjdk-15.0.1_linux-x64_bin.tar.gz"

ls
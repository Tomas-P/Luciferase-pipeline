#!/bin/bash
echo "Installing pipeline in current folder"
folder=$(echo https://github.com/Tomas-P/Luciferase-pipeline/raw/master)
here=$(pwd)
mkdir Segment_Algorithms
cd Segment_Algorithms
sa_folder=$(echo $folder/Segment_Algorithms)
wget $sa_folder/Arabadopsis.py
wget $sa_folder/Other.py
wget $sa_folder/Setaria.py
cd $here
wget $folder/analysis.py
wget $folder/background.py
wget $folder/constants.py
wget $folder/dependencies.sh
wget $folder/filtering.py
wget $folder/main.py
wget $folder/measure.py
wget $folder/options.py
wget $folder/segment.py
sudo chmod +x dependencies.sh
./dependencies.sh

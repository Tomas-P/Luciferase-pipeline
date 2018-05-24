# Luciferase-pipeline

A pipeline made using ImageJ and Python to analyze images created using the luciferase enzyme inserted into plants.
The goal is to have one program that can be run with minimal user input.
I now have a pipeline I consider complete, invoked by running run_me.py
This plugin takes a folder of images, a set of ROIs created in the ImageJ RoiManager, and a folder to place output in.
It outputs a .csv file in the folder for output that contains the mean and median gray value for each plant in the image
at each stack position.
I think I can write a program that takes this .csv file and produces a figure from it.

The scripts in the repository have the following dependencies:
* tkinter
* pandas
* numpy
* matplotlib
* os.path

Of these, pandas, numpy, and matplotlib are not in the standard library. You should be able to install them through pip.
I have created scripts to install these libraries, but use the install scripts at your own risk, I have not tested them.

## Citations
I need to cite ImageJ plugins used, matplotlib, possibly numpy, possilby pandas.

## How to use
To be written. The program is unfinished.

## How to set up
Install ImageJ. Install this programs dependencies. Further steps to be written. The program is unfinished.

## License
I have not decided yet. I will update this page when I do.

## Overview
The deprecated folder contains the old way of doing things.
luciferase.py contains helpful functionality for this program.
Rest to be written.

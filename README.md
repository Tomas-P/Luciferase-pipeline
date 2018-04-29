# Luciferase-pipeline

A pipeline made using ImageJ and Python to analyze images created using the luciferase enzyme inserted into plants.
The goal is to have one program that can be run with minimal user input.
At present, I have an ImageJ plugin I wrote in Python.
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

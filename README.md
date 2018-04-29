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
I have created scripts to install these libraries, but use the install scripts at your own risk, I have not tested them.

##How to use
Run the run_me.py program.
Answer the prompt about whether you want the median or average values.
Wait for the ImageJ program to launch, then answer any relevant prompts originating from ImageJ.
Wait until all ImageJ operations finish.
Answer the "select .csv with data" prompt.
Wait for the program to finish.

##How to set up.
Install ImageJ.
Download the repository.
Create an RoiSet.zip file for your dataset.
Go into the Tomas_Pipeline.py plugin and change the 25 to the number of images in you data set.

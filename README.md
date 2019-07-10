# Luciferase-pipeline

An automated pipeline for analyzing luciferase imaging data using Python and ImageJ.

## Features
* Automatic generation of regions of interest
* User defined experimental groups
* Option to use custom regions of interest
* Option to normalize data set against max value by roi
* Simple GUI
* Saves input parameters for future reference
* Outputs measurements by experimental group in csv file
* Outputs graph of each experimental group
* Outputs graph of each group's average values
* Independent of ImageJ's position in filesystem
* Independent of dataset's positions in filesystem
* Fast
* Reproducible results

## Dependencies
* numpy
* matplotlib
* PyJnius
* Python 3.5
    * Should I list the python standard library or the modules used?
* Fiji(Fiji Is Just ImageJ)

## Installation
1. Install Python 3.5 or later from https://www.python.org/
    * Make sure to include pip in your install
2. Install Fiji from http://fiji.sc/
3. Follow the PyJnius install instructions for your OS at https://pyjnius.readthedocs.io/en/stable/installation.html
4. Use pip to install numpy and matplotlib
5. Download the code from this repository into a folder on your computer

## Running
Run the luciferase.py script under Python 3.5 or later.


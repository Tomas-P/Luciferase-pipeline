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
* Time based X axis based on user input of first image time and inteval between succesive images
* Reproducible results

## Dependencies
* numpy
* matplotlib
* PyJnius
* Python 3.5
    * Should I list the python standard library or the modules used?
* Fiji(Fiji Is Just ImageJ)

## Installation
You can try to download and run the `installer.sh` script with a root user account.
Alternatively, install the following by hand before downloading the repo
through git or other means:


* Fiji (Fiji Is Just ImageJ)
* JDK (try using default-jdk first)
* Python 3 (python3)
   * pip (python3-pip)
   * tkinter (python3-tk)
   * Numpy \[numpy\]
   * Matplotlib \[matplotlib\]
   * PyJnius \[PyJnius\] *make sure you set JAVA_HOME before installing*
   


## Running
Run the luciferase.py script under Python 3.5 or later.


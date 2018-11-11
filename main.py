#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:03:58 2018

@author: tomas
"""

from os import path
import subprocess as sub
from constants import CONSTANTS
from matplotlib import pyplot
import analysis
import options

def filterprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("filtering.py")],stdout=sub.PIPE)

def segmentprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("segment.py")],stdout=sub.PIPE)

def measure_data():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("measure.py")],stdout=sub.PIPE)

def measure_background():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("background.py")],stdout=sub.PIPE)


def setup():
    fp = filterprocess()
    sp = segmentprocess()
    line = fp.stdout.readline().decode()
    while not line.startswith("Filtering complete, stack saved"):
        line = fp.stdout.readline().decode()
    fp.terminate()
    print("Filtering Process Complete")
    print(sp.stdout.readline().decode())
    sp.terminate()
            


def measurement():
    md = measure_data()
    mb = measure_background()
    print(md.stdout.readline().decode())
    print(mb.stdout.readline().decode())
    md.terminate()
    mb.terminate()


def groups_of_interest():
    try:
        return list(map(int, input("Any interesting groups?").split(',')))
    except ValueError:
        return None


def grid():
    return analysis.grid_from_data(analysis.get_data())

def main():
    options.options() # make sure options are set
    pyplot.xlabel("Time")
    pyplot.ylabel("Intensity")
    pyplot.title("Plant group average intensity over time")
    setup()
    measurement()
    analysis.graph_all_group_averages()
    pyplot.legend()
    pyplot.show()
    analysis.graph_all_groups_seperately()
    
    
if __name__ == '__main__':
    main()

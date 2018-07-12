#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 16:03:58 2018

@author: tomas
"""

from os import path
import subprocess as sub
from constants import CONSTANTS
from time import sleep
from matplotlib import pyplot
import analysis
import options

def filterprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("filtering.py")])

def segmentprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("segment.py")])

def measure_data():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("measure.py")])

def measure_background():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("background.py")])


def setup():
    fp = filterprocess()
    sp = segmentprocess()
    sleep(5 * 60)
    fp.terminate()
    sp.terminate()


def measurement():
    md = measure_data()
    mb = measure_background()
    sleep(3 * 60)
    md.terminate()
    mb.terminate()


def groups_of_interest():
    try:
        return list(map(int, input("Any interesting groups?").split(',')))
    except ValueError:
        return None


def grid():
    return analysis.grid_from_measurements(analysis.get_measurements())


def main():
    options.getoptions() # make sure options are set
    pyplot.xlabel("Time")
    pyplot.ylabel("Intensity")
    pyplot.title("Plant group average intensity over time")
    setup()
    measurement()
    analysis.graph()
    pyplot.legend()
    n_groups, g_size = analysis.get_group_info()
    my_grid = grid()
    pyplot.show()
    group_numbers = groups_of_interest()
    
    
    for group_number in group_numbers:
        lbound = group_number * g_size
        ubound = lbound + g_size
        g = analysis.reduce_group(analysis.extract_group(my_grid,lbound,ubound))
        pyplot.plot(g)
        pyplot.title("Group {} plants".format(group_number))
        pyplot.xlabel("Time")
        pyplot.ylabel("Intensity")
        pyplot.show()
    
if __name__ == '__main__':
    main()
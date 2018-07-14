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
import json

def filterprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("filtering.py")])

def segmentprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("segment.py")])

def measure_data():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("measure.py")])

def measure_background():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("background.py")])


def setup(pause=False):
    fp = filterprocess()
    if not options.getoptions()["user roi"]:
        sp = segmentprocess()
        sleep(4 * 60)
        fp.terminate()
        if pause: # if inspecting the rois is desired
            sp.wait() # wait for the user to close this ImageJ
        else: #otherwise, halt this ImageJ
            sp.terminate()
    else:
        sleep(4 * 60)
        fp.terminate()


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
    opts = options.getoptions() # make sure options are set
    pause = opts["pause"]
    pyplot.xlabel("Time")
    pyplot.ylabel("Intensity")
    pyplot.title("Plant group average intensity over time")
    setup(pause)
    measurement()
    analysis.graph()
    pyplot.legend()
    n_groups, g_size = analysis.get_group_info()
    my_grid = grid()
    pyplot.show()
    group_numbers = groups_of_interest()
    
    if not opts["user groups"]:
        for group_number in group_numbers:
            lbound = group_number * g_size
            ubound = lbound + g_size
            g = analysis.extract_group(my_grid,lbound,ubound)
            pyplot.plot(g)
            pyplot.title("Group {} plants".format(group_number))
            pyplot.xlabel("Time")
            pyplot.ylabel("Intensity")
            pyplot.show()
    else:
        with open(opts["group file"]) as ghandle:
            gbounds = json.load(ghandle)
        for group_number in group_numbers:
            lbound = gbounds[group_number][0]
            ubound = gbounds[group_number][1]
            g = analysis.extract_group(my_grid,lbound,ubound)
            pyplot.plot(g)
            pyplot.title("Group {} plants".format(group_number))
            pyplot.xlabel("Time")
            pyplot.ylabel("Intensity")
            pyplot.show()
    
if __name__ == '__main__':
    main()
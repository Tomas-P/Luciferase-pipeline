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
import json
import numpy
from functools import reduce

def filterprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("filtering.py")],stdout=sub.PIPE)

def segmentprocess():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("segment.py")],stdout=sub.PIPE)

def measure_data():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port1", "--run", path.abspath("measure.py")],stdout=sub.PIPE)

def measure_background():
    return sub.Popen([CONSTANTS.IMAGEJ,"-port2", "--run", path.abspath("background.py")],stdout=sub.PIPE)


def setup(pause=False):
    fp = filterprocess()
    if not options.getoptions()["user roi"]:
        sp = segmentprocess()
        if pause:
            line = fp.stdout.readline().decode()
            while not line.startswith("Filtering complete, stack saved"):
                line = fp.stdout.readline().decode()
            fp.terminate()
            print(sp.stdout.readline().decode())
            sp.communicate()
        else:
            line = fp.stdout.readline().decode()
            while not line.startswith("Filtering complete, stack saved"):
                line = fp.stdout.readline().decode()
            fp.terminate()
            print(sp.stdout.readline().decode())
            sp.terminate()
            
    else:
        print(fp.stdout.readline().decode())
        fp.terminate()


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
            subgroup_def = gbounds[group_number]
            subs = []
            for lower,upper in subgroup_def:
                sub = analysis.extract_group(my_grid,lower,upper)
                subs.append(sub)
            group = reduce(lambda a,b : numpy.concatenate((a,b),axis=1), subs)
                
            pyplot.plot(group)
            pyplot.title("Group {} plants".format(group_number))
            pyplot.xlabel("Time")
            pyplot.ylabel("Intensity")
            pyplot.show()
    
if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 12:56:45 2018

@author: tomas
"""

from xml.etree import ElementTree as et
from pandas import read_csv
from numpy import ndarray
from matplotlib import pyplot

def get_tree():
    return et.parse('info.xml')

def get_name(tree):
    return tree.findtext("csv")

def get_background_name(tree):
    return tree.findtext("bgcsv")

def plants_per_slice(csv):
    
    for i in range(len(csv)):
        if csv.Slice[i] > 1:
            return i

def to_2_dimensions(csv):
    grid = {}
    for i in range(len(csv)):
        grid.setdefault(i % plants_per_slice(csv),[]).append(csv.iloc[i])
    return grid

def make_array(grid):
    arr = ndarray((len(grid),len(grid[0])))
    for i in grid:
        for j, data in enumerate(grid[i]):
            arr[i,j] = (data.Area * data.Mean) / (data.Area * (data["%Area"] / 100))
    
    return arr.T

def extract_group(grid,lower_bound,upper_bound):
    return grid[...,lower_bound : upper_bound]

def reduce_group(group):
    return list(map(lambda timepoint : sum(timepoint) / len(timepoint), group))

def graph():
    csvname = get_name(get_tree())
    table = read_csv(csvname)
    grid = to_2_dimensions(table)
    arr = make_array(grid)
    group_tree = et.parse('groups.xml')
    groups = group_tree.findall("group")
    graph_grids = []
    for group in groups:
        lower = int(group.findtext('lower'))
        higher = int(group.findtext('higher'))
        g_group = extract_group(arr, lower, higher)
        graph_grids.append(g_group)
    
    reduced = map(reduce_group, graph_grids)
    for i,group in enumerate(reduced):
        pyplot.plot(group,label="Group {}".format(i))
    
    background = read_csv(get_background_name(get_tree()))
    bgpoints = []
    for i in range(len(background)):
        bgpoints.append(background.Mean[i])
    
    pyplot.plot(bgpoints, label="Background Region Average")
    return None

if __name__ == '__main__':
    graph()
    pyplot.legend()
    pyplot.show()
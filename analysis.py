#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 13:15:12 2018

@author: tomas
"""

import numpy as np
import pandas as pd
import json
from matplotlib import pyplot


def get_measurements() -> pd.DataFrame:
    return pd.read_csv("measurements.csv")


def get_background() -> pd.DataFrame:
    return pd.read_csv("background.csv")


def count_plants(measurements :pd.DataFrame) -> int:
    i = 0
    row = measurements.iloc[i]
    while row.Slice == 1:
        i +=1
        row = measurements.iloc[i]
    return i


def count_slices(measurements :pd.DataFrame) -> int:
    return max(measurements.Slice)


def makegrid(slices :int,plants :int)->np.ndarray:
    return np.zeros((slices,plants))


def grid_dict(measures :pd.DataFrame, plant_count) -> dict:
    grid = {}
    for i in range(len(measures)):
        grid.setdefault(i % plant_count,[]).append(measures.iloc[i])
    return grid


def grid_from_measurements(measures :pd.DataFrame) -> np.ndarray:
    slices = count_slices(measures)
    plants = count_plants(measures)
    grid = makegrid(slices,plants)
    g = grid_dict(measures, plants)
    
    for key in g:
        for i,data in enumerate(g[key]):
            grid[int(i),int(key)] = float((data.Area * data.Mean) / (data.Area * (data["%Area"] / 100)))
    
    return grid


def grid_from_background(bg :pd.DataFrame) -> np.ndarray:
    values = []
    for i in range(len(bg)):
        values.append(bg.iloc[i].Mean)
    return np.array(values)


def get_group_info():
    with open("options.json") as opt:
        options = json.load(opt)
    num_groups = options["group count"]
    group_size = options["group member count"]
    return (num_groups, group_size)


def extract_group(grid,lower_bound,upper_bound):
    return grid[:,lower_bound:upper_bound]


def reduce_group(group):
    return list(map(lambda timepoint : sum(timepoint) / len(timepoint),group))


def extract_all_groups(grid,group_size,group_count):
    groups = []
    for i in range(group_count):
        l_bound = i * group_size
        u_bound = l_bound + group_size
        group = extract_group(grid,l_bound,u_bound)
        groups.append(group)
    return groups


def reduce_all_groups(groups):
    return list(map(reduce_group, groups))


def graph():
    measures = get_measurements()
    background = get_background()
    measure_grid = grid_from_measurements(measures)
    background_grid = grid_from_background(background)
    n_g, g_s = get_group_info()
    groups = reduce_all_groups(extract_all_groups(measure_grid,g_s,n_g))
    for i,group in enumerate(groups):
        pyplot.plot(group,label="Group {}".format(i))
    pyplot.plot(background_grid, label="Background")
    
    
if __name__ == '__main__':
    graph()
    pyplot.legend()
    pyplot.show()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 10:52:09 2018

@author: tomas
"""

import pandas as pd
import numpy as np
import json
from matplotlib import pyplot

def get_background() -> pd.DataFrame:
    return pd.read_csv("artifacts/background.csv")

def get_data() -> pd.DataFrame:
    return pd.read_csv("artifacts/measurements.csv")

def get_options() -> dict:
    with open("config/options.json") as options:
        return json.load(options)

def count_plants(data :pd.DataFrame)->int:
    i = 0
    row = data.iloc[i]
    while row.Slice == 0:
        i += 1
        row = data.iloc[i]
    return i

def count_slices(data :pd.DataFrame)->int:
    return max(data.Slice) + 1

def count_groups(data :pd.DataFrame)->int:
    return max(data.Group_Number)+1

def isolate_group(data, group)->pd.DataFrame:
    return data[data.Group_Number == group]

def make_grid(slices :int, plants :int)->np.ndarray:
    return np.zeros((slices,plants),dtype=float)

def make_dict_grid(data :pd.DataFrame, plant_count :int)->dict:
    grid = {}
    for i in range(len(data)):
        grid.setdefault(i % plant_count, []).append(data.iloc[i])
    return grid

def grid_from_data(data :pd.DataFrame) -> np.ndarray:
    slices = count_slices(data)
    plants = count_plants(data)
    grid = make_grid(slices,plants)
    dg = make_dict_grid(data, plants)
    
    for key in dg:
        for i,data in enumerate(dg[key]):
            numerator = data.Area * data.Mean
            denominator = (data.Area * data.Area_Fraction) / 100.0
            grid[int(i),int(key)] = float(numerator / denominator)
    
    return grid

def grid_from_background(background :pd.DataFrame) -> np.ndarray:
    values = []
    for i in range(len(background)):
        values.append(background.Mean[i])
    return np.array(values)

def average_group(group :np.ndarray) -> list:
    average = lambda timepoint : sum(timepoint) / len(timepoint)
    return list(map(average, group))

def group_averages():
    
    data = get_data()
    
    groups = []
    
    for i in range(0,count_groups(data)):
        g = isolate_group(data,i)
        try:
            avg = average_group(grid_from_data(g))
            groups.append((i,avg))
        except ValueError:
            pass
    return groups
    

def graph_all_group_averages():
    group_lines = group_averages()
    background_line = grid_from_background(get_background())
    pyplot.plot(background_line,label="Background")
    for number,group in group_lines:
        if number != 0:
            pyplot.plot(group,label="Group {}".format(number))
        else:
            pyplot.plot(group,label="Unclassified")

def graph_all_groups_seperately():
    groups = {}
    data = get_data()
    for i in range(count_groups(data)):
        try:
            groups[i] = grid_from_data(isolate_group(data,i))
        except ValueError as e:
            print("There was an issue with group",i,"with error:",e)
    for key in groups:
        group = groups[key]
        pyplot.plot(group)
        if key != 0:
            pyplot.title("Group {}".format(key))
        else:
            pyplot.title("Unclassified")
        pyplot.show()

if __name__ == '__main__':
    graph_all_group_averages()
    pyplot.legend()
    pyplot.show()
    

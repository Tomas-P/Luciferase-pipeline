#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 11:13:34 2018

@author: tomas
"""

from ImageJ_gateway import String, ij
from pandas import DataFrame
import options

def get_stack():
    name = "artifacts/stack.tif"
    filename = String(name)
    return ij.ImagePlus(filename)

def get_rois():
    name = "artifacts/RoiSet.zip"
    filename = String(name)
    rm = ij.plugin.frame.RoiManager()
    rm.runCommand(String("Open"),filename)
    rois = rm.getRoisAsArray()
    rm.close()
    return rois

def get_groups():
    name = "config/GroupDefinitions.zip"
    filename = String(name)
    command = String("Open")
    rm = ij.plugin.frame.RoiManager()
    rm.runCommand(command,filename)
    rois = rm.getRoisAsArray()
    rm.close()
    return rois

def contains(outer,inner):
    inner_points = inner.getContainedPoints()
    return all(outer.contains(point.x,point.y) for point in inner_points)

def measure_data():
    stack = get_stack()
    rois = get_rois()
    groups = get_groups()
    measurements = []
    ij.IJ.run(String("Set Measurements..."),
              String("area mean area_fraction stack redirect=None decimal=3"))
    row = 0
    
    for i in range(stack.getImageStackSize()):
        for roi in rois:
            
            roi_data = {}
            
            stack.setRoi(roi)
            group_number = 0
            
            for j,group in enumerate(groups):
                if contains(group,roi):
                    group_number = j + 1
                    break
            
            stats = roi.getStatistics()
            
            roi_data["Mean"] = stats.mean
            roi_data["Area_Fraction"] = stats.areaFraction
            roi_data["Group_Number"] = group_number
            roi_data["Area"] = stats.area
            roi_data["Slice"] = i
            
            measurements.append(roi_data)
            row += 1
            print(roi_data)
            
        ij.IJ.run(stack,String("Next Slice [>]"),String(""))
        

    return DataFrame(measurements)

def measure_background():
    assert options.options_defined()
    bg = options.get_options()["background"]
    bx = bg["bx"]
    by = bg["by"]
    width = bg["width"]
    height = bg["height"]
    stack = get_stack()
    measurements = []
    for i in range(stack.getImageStackSize()):
        bg_data = {}
        stack.setRoi(bx,by,width,height)
        stats = stack.getStatistics()
        bg_data["Mean"] = stats.mean
        bg_data["Slice"] = i
        measurements.append(bg_data)
    return DataFrame(measurements)
        
if __name__ == '__main__':
    background = measure_background()
    print(background)
    data = measure_data()
    print(data)

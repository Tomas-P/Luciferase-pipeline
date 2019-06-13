#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 13:37:23 2019

@author: tomas
"""

import ui
import operations

import math
import pandas
from matplotlib import pyplot
import os


if __name__ == '__main__':
    
    ui.UserInterface.interface()
    ui.UserInterface.save("parameters.txt")
    if not ui.UserInterface.existing_roi:
        rois = operations.generate_rois(ui.UserInterface.mask)
    else:
        rois = operations.open_archive(ui.UserInterface.existing_roi)
    mask = operations.open_mask(ui.UserInterface.mask)
    stack = operations.open_stack(ui.UserInterface.folder)
    data = operations.process(stack, mask)
    groups = operations.open_archive(ui.UserInterface.group_file)
    areas = operations.affiliate(groups, rois)
    background = operations.measure_background(
        data,ui.UserInterface.bg_bx,
        ui.UserInterface.bg_by,ui.UserInterface.bg_width,
        ui.UserInterface.bg_height
        )

    measurements = operations.measure_data(data,areas)

    operations.save_rois(rois, ui.UserInterface.save_roi_name)

    for groupkey in measurements:
        group = measurements[groupkey]
        g_avgs = [sum(group[i]) / len(group[i]) for i in range(len(group))]
        if groupkey != -1:
            pyplot.plot(g_avgs,label="Group {}".format(groupkey))
        else:
            pyplot.plot(g_avgs,label="Unclassified")
        
    pyplot.legend()
    pyplot.title("Average Group Brightness over Time")
    pyplot.xlabel("Position in stack (eg Time)")
    pyplot.ylabel("Brightness - adjusted")

    pyplot.plot(background, label="Background")
    pyplot.show()

    try:
        os.mkdir("output")
    except FileExistsError:
        pass

    for gkey, gvalues in measurements.items():
        frame = pandas.DataFrame(gvalues)
        frame = frame.T
        frame.to_excel("output/group_{}.xlsx".format(gkey),index=False,header=False)

    for groupkey in measurements:
        group = measurements[groupkey]
        pyplot.plot(group.values())
        pyplot.title("Group {}".format(groupkey))
        pyplot.xlabel("Time")
        pyplot.ylabel("Brightness")
        pyplot.show()
        

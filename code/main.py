#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:57:27 2018

@author: tomas
"""

import subprocess as sub
from xml.etree import ElementTree as et
from os.path import abspath
import graph
from matplotlib import pyplot


def graph_groups():
    # get program info
    info = et.parse("info.xml")
    # get the name of ImageJ
    ij_folder = info.findtext("imagej")
    imagej_name = ij_folder + "ImageJ-linux64"
    # Run the ImageJ plug-in
    sub.run([imagej_name, '--run', abspath("Tomas_Plugin.py")])
    # Do the math and work to create the graph
    graph.graph()
    # create the graph legend , assuming the time to execute
    # is linear for the number of images.
    pyplot.legend()
    # display the graph
    pyplot.show()

def groups_of_interest():
    return map(int, input("Any interesting groups?").split(','))

def get_group_element(group_number):
    group_tree = et.parse('groups.xml')
    for element in group_tree.findall("group"):
        if int(element.findtext("number")) == group_number:
            return element

def get_array():
    return graph.make_array(graph.to_2_dimensions(graph.read_csv(graph.get_name(graph.get_tree()))))



# Graph the information
if __name__ == '__main__':
    graph_groups()
    
    group_nums = groups_of_interest()
    plant_grid = get_array()
    groups = {}
    loc = 1
    for group_number in group_nums:
        group_elem = get_group_element(group_number)
        lower = int(group_elem.findtext("lower"))
        higher = int(group_elem.findtext("higher"))
        group = graph.extract_group(plant_grid,lower,higher)
        groups[group_number] = group
    
    for group_number in groups:
        print("group",group_number)
        pyplot.plot(groups[group_number])
        pyplot.show()
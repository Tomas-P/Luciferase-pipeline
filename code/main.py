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

def main():
    info = et.parse("info.xml")
    ij_folder = info.findtext("imagej")
    imagej_name = ij_folder + "ImageJ-linux64"
    sub.run([imagej_name, '--run', abspath("Tomas_Plugin.py")])
    graph.graph()
    pyplot.legend()
    pyplot.show()

if __name__ == '__main__':
    main()
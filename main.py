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
import analysis

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


if __name__ == "__main__":
    setup()
    measurement()
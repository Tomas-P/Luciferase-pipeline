#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 13:15:12 2018

@author: tomas
"""

import numpy as np
import pandas as pd

def get_measurements():
    return pd.read_csv("measurements.csv")

def get_background():
    return pd.read_csv("background.csv")


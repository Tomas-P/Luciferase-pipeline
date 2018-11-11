#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 10:07:43 2018

@author: tomas
"""
from os import path as _path
class CONSTANTS:
    
    ARABADOPSIS = 0
    SETARIA = 1
    OTHER = 2
    SEEDLING = 3
    IMAGEJ = _path.expanduser("~/Fiji.app/ImageJ-linux64")
    
    def __setattr__(self,name,value):
        raise TypeError("Constants cannot be altered!")
    

CONSTANTS = CONSTANTS()

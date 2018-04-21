# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 20:35:38 2018

@author: Tomas
"""

import subprocess as sub
import config
import folder

def imagej_name():
    configuration = config.configuration()
    imagej_folder = folder.Folder(configuration[config.IMAGEJ])
    return imagej_folder.search('ImageJ-')[0]

def run(commands='',*args,**kwargs):
    program = imagej_name() + ' ' + commands if commands!='' else imagej_name()
    return sub.Popen(program,*args,**kwargs)

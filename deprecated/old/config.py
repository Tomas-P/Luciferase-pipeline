# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 18:29:49 2018

@author: Tomas
"""

DATA,ROI,RAW,IMAGEJ = 'data','roi','raw','imagej'

import json
from os.path import isfile
import tkinter as tk
from tkinter.filedialog import askdirectory as askdir

def update(collection,tag,func):
    collection[tag] = func()

def ui():
    config = {}
    window = tk.Tk()
    tk.Button(window,
              text="Ok",
              command=window.destroy).pack(side=tk.BOTTOM)
    tk.Button(window,
              text="choose the folder with your data images",
              command=lambda:update(config,DATA,askdir)
              ).pack(fill=tk.X)
    tk.Button(window,
              text="choose the folder with your roi images",
              command=lambda:update(config,ROI,askdir)
              ).pack(fill=tk.X)
    tk.Button(window,
              text="choose the folder with your raw images",
              command=lambda:update(config,RAW,askdir)
              ).pack(fill=tk.X)
    tk.Button(window,
              text="choose the folder with your imagej installation",
              command=lambda:update(config,IMAGEJ,askdir)
              ).pack(fill=tk.X)
    window.mainloop()
    return config

def load(filename):
    with open(filename) as config:
        return json.load(config)

def save(settings,filename):
    with open(filename, 'w') as config:
        json.dump(settings,config)

def configuration(filename=None):
    if filename is None:
        filename = __file__[:__file__.rfind('\\')]+'\\' + 'config.json'
    if isfile(filename):
        return load(filename)
    else:
        prefs = ui()
        save(prefs,filename)
        return prefs

if __name__ == '__main__':
    configuration()

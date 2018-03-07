# -*- coding: utf-8 -*-

import glob
import tkinter
from tkinter import ttk
from tkinter.filedialog import askdirectory as askdir
import json
from skimage.io import imread

#constants
IMAGEJ = 'imagej'
RAW = 'raw'
DATA = 'data'
ROI = 'roi'

def to_int(string):
    "concatenate all numeric characters and convert them to an integer"
    numstring = ''.join(char for char in string if char.isnumeric())
    return int(numstring)

class Folder:
    "Represents a folder"
    def __init__(self,name):
        self.name = name
        self.files = [file.replace('\\','/') for file in glob.glob(name + '/*')]
    def only_files(self)->bool:
        return all(file[-4]=='.' for file in self.files)
    def sort(self,key_func=to_int):
        self.files.sort(key=key_func)
    def next_image(self):
        for file in self.files:
            yield (file, imread(file))
    def search(self,flag):
        return [file for file in self.files if flag in file]


def config(file='config.json',folder="C:/Users/Tomas/Documents/Luciferase/"):
    file = folder + file
    def exists():
        try:
            c = open(file)
        except FileNotFoundError:
            return False
        c.close()
        return True
    def ui():
        conf = {}
        root = tkinter.Tk()
        bt = ttk.Button
        def func(tag):
            conf[tag] = askdir()
        bt(root,text="Apply",command=root.destroy).pack(side=tkinter.BOTTOM)
        bt(root,
           text="Choose the folder with your data images",
           command=lambda:func(DATA)).pack(fill=tkinter.X)
        bt(root,
           text="Choose the folder with your ROI images",
           command=lambda:func(ROI)).pack(fill=tkinter.X)
        bt(root,
           text="Choose the folder with your raw images",
           command=lambda:func(RAW)).pack(fill=tkinter.X)
        bt(root,
           text="Choose the folder with your ImageJ installation",
           command=lambda:func(IMAGEJ)).pack(fill=tkinter.X)
        root.mainloop()
        return conf
    def load():
        with open(file) as conf:
            return json.load(conf)
    def save(settings):
        with open(file,'w') as conf:
            json.dump(settings,conf)
    if exists():
        return load()
    cnfg = ui()
    save(cnfg)
    return cnfg


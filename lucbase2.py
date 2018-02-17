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

class ImageData:
    "Represents an image"
    def __init__(self,data_array_name,data_array,roi_array_name,roi_array):
        self.data = data_array
        self.data_name = data_array_name
        self.roi = roi_array
        self.roi_name = roi_array_name
    def get_pixel(self,x,y):
        pixel = {'x':x,
                 'y':y,
                 'data?':self.roi[x][y],
                 'value':self.data[x][y]
                }
        return pixel
    def next_pixel(self):
        xlen = len(self.data)
        ylen = len(self.data[0])
        for k in range(xlen):
            for j in range(ylen):
                yield self.get_pixel(k,j)
    def median(self):
        midpoint = lambda ls:ls[int(len(ls)/2)]
        vals = [pixel['value'] for pixel in self.next_pixel()]
        vals.sort()
        return midpoint(vals)
    def data_median(self):
        "finds the median of data pixels in an image."
        midpoint = lambda ls:ls[int(len(ls)/2)]
        vals = [pixel['value'] for pixel in self.next_pixel() if pixel['data?']]
        vals.sort()
        return midpoint(vals)
    def mean(self):
        "finds the mean of value of an image."
        total = self.data.sum()
        return total / (len(self.data) * len(self.data[0]))
    def data_mean(self):
        "Finds the mean of data in the image."
        total = 0
        datapoints = 0
        for pixel in self.next_pixel():
            if pixel['data?']:
                total += pixel['value']
                datapoints += 1
        return total / datapoints

def config(file='config.json',folder="C:/Users/Tomas/Desktop/TimeLabColleen/Luciferase/"):
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

if __name__ == '__main__':
    # more to check the module works than anything else
    cnf = config()
    imagej = Folder(cnf[IMAGEJ])
    raws = Folder(cnf[RAW])
    data = Folder(cnf[DATA])
    rois = Folder(cnf[ROI])
    data.sort(to_int)
    rois.sort(to_int)
    #assert len(data.files)==len(rois.files)
    d_iter = data.next_image()
    r_iter = rois.next_image()
    for i in range(len(data.files)):
        dname, darr = next(d_iter)
        rname, rarr = next(r_iter)
        im = ImageData(dname,darr,rname,rarr)
        print(im.data_name,im.roi_name)
        print("means")
        print(im.data_mean())
        print(im.mean())
        print("medians")
        print(im.data_median())
        print(im.median())
        print('---')

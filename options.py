#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:48:24 2018

@author: tomas
"""

import tkinter as tk
from tkinter.filedialog import askdirectory
from constants import CONSTANTS
import json
from os.path import isfile


def user_inteface():
    
    options = {}
    
    
    rwindow = tk.Tk()
    
    text = tk.StringVar(value="Folder with images")
    
    getdir_button = tk.Button(rwindow,text="Browse",command = lambda : text.set(askdirectory(title="Folder with images")))
    
    getdir_entry = tk.Entry(rwindow, textvariable=text)
    
    selection_algorithim = tk.IntVar()
    
    s_alg_label = tk.Label(rwindow,text="Roi selection algorithim")
    
    arabadopsis_button = tk.Radiobutton(master=rwindow,
                                        variable=selection_algorithim,
                                        value=CONSTANTS.ARABADOPSIS,
                                        text="Arabadopsis",
                                        padx=20)
    
    setaria_button = tk.Radiobutton(master=rwindow,
                                    variable=selection_algorithim,
                                    value=CONSTANTS.SETARIA,
                                    text="Setaria",
                                    padx=20)
    
    other_button = tk.Radiobutton(master=rwindow,
                                  variable=selection_algorithim,
                                  value=CONSTANTS.OTHER,
                                  text="Other",
                                  padx=20)
    
    donebutton = tk.Button(rwindow,text="Done",command=rwindow.destroy)
    
    bx,by,width,height = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
    
    bx_slider = tk.Scale(rwindow,from_=0,to=2048,orient=tk.HORIZONTAL,variable=bx)
    
    by_slider = tk.Scale(rwindow,from_=0,to=2048,orient=tk.HORIZONTAL,variable=by)
    
    width_slider = tk.Scale(rwindow,from_=0,to=500,orient=tk.HORIZONTAL,variable=width)
    
    height_slider = tk.Scale(rwindow,from_=0,to=500,orient=tk.HORIZONTAL,variable=height)
    
    bx_label = tk.Label(rwindow,text="bx")
    by_label = tk.Label(rwindow,text="by")
    width_label = tk.Label(rwindow,text="width")
    height_label = tk.Label(rwindow, text="height")
    
    bglabel = tk.Label(rwindow,text="Where to measure the background?")
    
    top_label = tk.Label(rwindow, text="Pipeline Options")
    
    preserve = tk.BooleanVar()
    
    preserve_switch = tk.Checkbutton(rwindow,
                                     text="Check to preserve options.json after the pipeline finished.",
                                     variable=preserve,
                                     onvalue=True,
                                     offvalue=False)
    
    top_label.grid(row=0)
    
    getdir_entry.grid(row=1,column=0)
    getdir_button.grid(row=1,column=1)
    
    s_alg_label.grid(row=2,column=0)
    
    arabadopsis_button.grid(row=2,column=1)
    setaria_button.grid(row=3,column=1)
    other_button.grid(row=4,column=1)
    
    bglabel.grid(row=5)
    
    bx_label.grid(row=6,column=0)
    bx_slider.grid(row=6,column=1)
    
    by_label.grid(row=7,column=0)
    by_slider.grid(row=7,column=1)
    
    width_label.grid(row=8,column=0)
    width_slider.grid(row=8,column=1)
    
    height_label.grid(row=9,column=0)
    height_slider.grid(row=9,column=1)
    
    preserve_switch.grid(row=10,columnspan=2)
    
    donebutton.grid(row=11)
    
    rwindow.mainloop()
    
    options["images"] = text.get()
    options["selection algorithim"] = selection_algorithim.get()
    options["background"] = {"bx" : bx.get(),
           "by" : by.get(),
           "width" : width.get(),
           "height" : height.get()}
    options["preserve"] = preserve.get()
    
    return options


def save_options(options):
    with open("options.json","w") as optfile:
        json.dump(options,optfile)

def read_options():
    with open("options.json") as optfile:
        options = json.load(optfile)
    
    return options

def getoptions():
    if isfile("options.json"):
        return read_options()
    else:
        options = user_inteface()
        save_options(options)
        return options

if __name__ == '__main__':
    getoptions()
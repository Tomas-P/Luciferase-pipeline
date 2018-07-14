#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 09:48:24 2018

@author: tomas
"""

import tkinter as tk
from tkinter.filedialog import askdirectory, askopenfilename
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
    
    user_def_roi = tk.BooleanVar()
    user_def_groups = tk.BooleanVar()
    
    udroi = tk.Checkbutton(rwindow,text="User defined rois",variable=user_def_roi,onvalue=True,offvalue=False)
    udgroup = tk.Checkbutton(rwindow,text='User defined groups',variable=user_def_groups,onvalue=True,offvalue=False)
    
    rwidth, rheight = tk.IntVar(), tk.IntVar()
    roi_w_slider = tk.Scale(rwindow,from_=0,to=200,variable=rwidth,orient=tk.HORIZONTAL)
    roi_h_slider = tk.Scale(rwindow,from_=0,to=200,variable=rheight,orient=tk.HORIZONTAL)
    
    num_groups,member_count = tk.IntVar(),tk.IntVar()
    ng_slider = tk.Scale(rwindow,from_=1,to=30,variable=num_groups,orient=tk.HORIZONTAL)
    mc_slider = tk.Scale(rwindow,from_=1,to=50,variable=member_count,orient=tk.HORIZONTAL)
    nglabel = tk.Label(rwindow,text="number of groups")
    mclabel = tk.Label(rwindow,text="group member count")
    
    top_label.grid(row=0)
    
    getdir_entry.grid(row=1,column=0)
    getdir_button.grid(row=1,column=1)
    
    s_alg_label.grid(row=2,column=0)
    
    arabadopsis_button.grid(row=2,column=1)
    setaria_button.grid(row=3,column=1)
    other_button.grid(row=4,column=1)
    
    bglabel.grid(row=5,columnspan=2)
    
    bx_label.grid(row=6,column=0)
    bx_slider.grid(row=6,column=1)
    
    by_label.grid(row=7,column=0)
    by_slider.grid(row=7,column=1)
    
    width_label.grid(row=8,column=0)
    width_slider.grid(row=8,column=1)
    
    height_label.grid(row=9,column=0)
    height_slider.grid(row=9,column=1)
    
    #preserve_switch.grid(row=10,columnspan=2)
    udgroup.grid(row=10,column=0)
    udroi.grid(row=10,column=1)
    
    roi_w_slider.grid(row=11,column=1,columnspan=2)
    roi_h_slider.grid(row=12,column=1,columnspan=2)
    tk.Label(text="roi width").grid(row=11, column=0)
    tk.Label(text="roi height").grid(row=12, column=0)
    
    tk.Label(rwindow,text="Group attributes").grid(row=13,columnspan=2)
    nglabel.grid(row=14,column=0)
    ng_slider.grid(row=14,column=1,columnspan=2)
    
    mclabel.grid(row=15,column=0)
    mc_slider.grid(row=15,column=1,columnspan=2)
    
    pause = tk.BooleanVar(value=False)
    tk.Checkbutton(rwindow,variable=pause,onvalue=True,offvalue=False,text="Pause at steps").grid(row=16)
    
    donebutton.grid(row=17)
    
    rwindow.mainloop()
    
    if user_def_roi.get() or user_def_groups.get():
        window2 = tk.Tk()
        roiname = tk.StringVar(value="Choose the roi archive")
        groupname = tk.StringVar(value="Choose the group list file")
        roientry = tk.Entry(window2,textvariable=roiname)
        groupentry = tk.Entry(window2,textvariable=groupname)
        roibutton = tk.Button(window2,text="Browse(ROI)",command=lambda:roiname.set(askopenfilename(title="Select Roi archive")))
        groupbutton = tk.Button(window2,text="Browse(Group)",command=lambda:groupname.set(askopenfilename(title="Select group definition file")))
        donebut = tk.Button(window2,text="Done",command=window2.destroy)
        
        tk.Label(window2,text="Get definitions").grid(row=0,columnspan=2)
        roientry.grid(row=1,column=0)
        roibutton.grid(row=1,column=1)
        groupentry.grid(row=2,column=0)
        groupbutton.grid(row=2,column=1)
        donebut.grid(row=3)
        
        window2.mainloop()
        
    options["images"] = text.get()
    options["selection algorithm"] = selection_algorithim.get()
    options["background"] = {"bx" : bx.get(),
           "by" : by.get(),
           "width" : width.get(),
           "height" : height.get()
           }
    options["rwidth"] = rwidth.get()
    options["rheight"] = rheight.get()
    options["group count"] = num_groups.get()
    options["group member count"] = member_count.get()
    options["user roi"] = user_def_roi.get()
    options["user groups"] = user_def_groups.get()
    options["pause"] = pause.get()
    
    if options["user roi"] or options["user groups"]:
        options["roi file"] = roiname.get()
        options["group file"] = groupname.get()
    
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

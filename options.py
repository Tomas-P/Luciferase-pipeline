#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 13:57:08 2018

@author: tomas
"""

import tkinter as tk
from tkinter import filedialog as fd
from os.path import exists
import json
from constants import CONSTANTS as consts

def options_defined() -> bool:
    return exists("config/options.json")

def get_options() -> dict:
    with open("config/options.json") as options:
        return json.load(options)

def set_options(settings :dict):
    with open("config/options.json","w") as options:
        json.dump(settings, options)

def ask_user_input():
    options = {}
    root = tk.Tk()
    root.title("Options")
    
    # have the user specify which folder their images are in
    folder_var = tk.StringVar()
    
    
    folder_label = tk.Label(root,text="Folder with images")
    folder_button = tk.Button(root,
                              command=lambda:folder_var.set(fd.askdirectory(title="Choose Folder")),
                              text="Choose Folder")
    
    folder_entry = tk.Entry(root,textvariable=folder_var)
    
    # have the user specify the size of the ROIs
    rwidth,rheight = tk.IntVar(),tk.IntVar()
    
    width_label = tk.Label(root,text="Roi width")
    height_label = tk.Label(root,text="Roi height")
    width_slider = tk.Scale(root,from_=1,to=200,variable=rwidth,orient=tk.HORIZONTAL)
    height_slider = tk.Scale(root,from_=1,to=200,variable=rheight,orient=tk.HORIZONTAL)
    
    
    # have the user choose which algorithm to use
    
    segment_var = tk.IntVar()
    
    segment_label = tk.Label(root,text="Segmentation algorithm")
    arabidopsis = tk.Radiobutton(root,variable=segment_var,text="Arabidopsis",value=consts.ARABADOPSIS)
    other = tk.Radiobutton(root,variable=segment_var,text="Other",value=consts.OTHER)
    setaria = tk.Radiobutton(root,variable=segment_var,text="Setaria",value=consts.SETARIA)
    seedling = tk.Radiobutton(root,variable=segment_var,text="Seedling",value=consts.SEEDLING)
    
    finish = tk.Button(root,text="Done",command=root.destroy)
    
    # describing background region to measure
    # bx : leftmost x
    # by : topmost y
    # width and height should be self-explanatory
    bx,by,bwidth,bheight=tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
    bx_label = tk.Label(root,text="leftmost x of background")
    bx_slider = tk.Scale(root,from_=0,to=1000,variable=bx,orient=tk.HORIZONTAL)
    
    by_label = tk.Label(root,text="topmost y of background")
    by_slider = tk.Scale(root,from_=0,to=1000,variable=by,orient=tk.HORIZONTAL)
    
    bwidth_label = tk.Label(root,text="width of background")
    bwidth_slider = tk.Scale(root,from_=0,to=1000,variable=bwidth,orient=tk.HORIZONTAL)
    
    bheight_label = tk.Label(root,text="height of background")
    bheight_slider = tk.Scale(root,from_=0,to=1000,variable=bheight,orient=tk.HORIZONTAL)
    
    # ask the user if custom rois are to be used, and if so, which:
    use_custom_roi = tk.BooleanVar()
    custom_roi = tk.StringVar()
    custom_roi_check = tk.Checkbutton(root,variable=use_custom_roi,text="Use custom ROIS")
    custom_roi_entry = tk.Entry(root,textvariable=custom_roi)
    custom_roi_button = tk.Button(root,text="Choose ROIs",command=lambda:custom_roi.set(fd.askopenfilename(title="Choose your ROI archive")))
    
    # Arrange all elements on the window
    folder_label.grid(row=0,column=0)
    folder_button.grid(row=0,column=1)
    folder_entry.grid(row=0,column=2)
    
    width_label.grid(row=1,column=0)
    width_slider.grid(row=1,column=1)
    height_label.grid(row=2,column=0)
    height_slider.grid(row=2,column=1)
    
    segment_label.grid(row=3)
    arabidopsis.grid(row=4)
    setaria.grid(row=5)
    other.grid(row=6)
    seedling.grid(row=7)
    
    bx_label.grid(row=8,column=0)
    bx_slider.grid(row=8,column=1)
    
    by_label.grid(row=9,column=0)
    by_slider.grid(row=9,column=1)
    
    bwidth_label.grid(row=10,column=0)
    bwidth_slider.grid(row=10,column=1)
    
    bheight_label.grid(row=11,column=0)
    bheight_slider.grid(row=11,column=1)
    
    custom_roi_check.grid(row=12,column=0)
    custom_roi_entry.grid(row=12,column=1)
    custom_roi_button.grid(row=12,column=2)
    finish.grid(row=13)
    
    # run the UI
    root.mainloop()
    
    # aquire the variables as regular objects
    foldername = folder_var.get()
    segmentation = segment_var.get()
    bg_x = bx.get()
    bg_y = by.get()
    bg_width = bwidth.get()
    bg_height = bheight.get()
    roi_width = rwidth.get()
    roi_height = rheight.get()
    
    options["images"] = foldername
    options["selection algorithm"] = segmentation
    options["background"] = {"height":bg_height,
           "by" : bg_y,
           "width" : bg_width,
           "bx" : bg_x
           }
    options["rheight"] = roi_height
    options["rwidth"] = roi_width
    options["use custom roi"] = use_custom_roi.get()
    options["custom roi"] = custom_roi.get()
    
    
    return options

def options() -> dict:
    if options_defined():
        return get_options()
    else:
        my_options = ask_user_input()
        set_options(my_options)
        return my_options
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:56:24 2019

@author: tomas
"""

import tkinter as tk
from tkinter import filedialog as fd
from os import environ

def request_folder(prompt :str) -> str:
    window = tk.Tk()
    
    folder = fd.askdirectory(
            master=window,
            title=prompt,
            initialdir = environ["HOME"] + "/Fiji.app"
            )
    
    window.destroy()
    
    return folder + '/'



class LabeledScale(tk.Frame):
    
    def __init__(self, master, min_v :int, max_v :int, label :str, var :tk.IntVar):
        
        tk.Frame.__init__(self, master)
        
        scale = tk.Scale(self,
                              from_ = min_v,
                              to = max_v,
                              orient = tk.HORIZONTAL,
                              variable = var)
        
        text = tk.Label(self, text=label)
        
        self.var = var
        
        down = tk.Button(
                self,
                text="-",
                command=lambda:self.var.set(
                        self.var.get() - 1))
        
        up = tk.Button(
                self,
                text="+",
                command=lambda:self.var.set(
                        self.var.get() + 1))
        
        text.grid(row=0,column=0,columnspan=2)
        
        down.grid(row=1,column=0,columnspan=1)
        
        up.grid(row=1,column=1,columnspan=1)
        
        scale.grid(row=2,column=0,columnspan=2)
    
    def get(self):
        
        return self.var.get()


class FileEntry(tk.Frame):
    
    def __init__(self, master, text:str, var:tk.StringVar, folder:bool=False, save:bool=False):
        
        tk.Frame.__init__(self,master)
        
        label = tk.Label(self, text=text)
        
        entry = tk.Entry(self, textvariable=var)
        
        if folder and save:
            
            raise Exception("Making new folders is outside the mission parameters")
            
        elif folder:
            func = lambda:var.set(fd.askdirectory())
            
        elif save:
            func = lambda:var.set(fd.asksaveasfilename())
            
        else:
            func = lambda:var.set(fd.askopenfilename())
        
        button = tk.Button(self, text=text, command=func)
        
        self.var = var
        
        label.grid(row=0,column=0)
        entry.grid(row=0,column=1)
        button.grid(row=0,column=2)
    
    def get(self):
        
        return self.var.get()

class UserInterface:
    
    # The goal was to give these variables values that were either reasonable
    # defaults or to give them values which would behave as false values if
    # otherwise unset
    
    folder = ''
    mask = ''
    
    # bg stands for background
    
    bg_bx = 0
    bg_by = 0
    bg_width = 100
    bg_height = 200
    
    existing_roi = ''
    
    save_roi_name = ''
    
    group_file = ''
    
    roi_height = 10
    roi_width = 10
    
    @classmethod
    def save(cls, filename):
        with open(filename, 'a') as handle:
            
            txt = """Folder\n{}\nMask\n{}\nbg_bx\n{}\n
            bg_by\n{}\nbg width\n{}\nbg_height\n{}\n
            existing roi\n{}\nsave roi name
            \n{}\ngroup file\n{}\nroi width\n{}\n
            roi height\n{}\n\n\n\n""".format(cls.folder,
            cls.mask,cls.bg_bx,cls.bg_by,
            cls.bg_width,cls.bg_height,
            cls.existing_roi,cls.save_roi_name,
            cls.group_file, cls.roi_width,cls.roi_height)
            
            handle.write(txt)
    
    @classmethod
    def interface(cls):
        
        window = tk.Tk()
        
        # we have to define tk variables to store tk values because thats how
        # tkinter operates
        bx,by,bwidth,bheight = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
        
        folder,mask = tk.StringVar(), tk.StringVar()
        
        existing = tk.StringVar()
        save_roi = tk.StringVar()
        groups = tk.StringVar()
        
        rheight, rwidth = tk.IntVar(), tk.IntVar()
        
        # _e suffix used for FileEntrys, _s suffix used for LabeledScales
        
        folder_e = FileEntry(window, "folder with data images", folder, True)
        
        mask_e = FileEntry(window, "image for segmentation", mask)
        
        bx_s = LabeledScale(window, 0, 200, "background left x", bx)
        
        by_s = LabeledScale(window, 0, 200, "background top y", by)
        
        bwidth_s = LabeledScale(window, 1, 200, "background width",bwidth)
        
        bheight_s = LabeledScale(window, 1, 200, "background height", bheight)
        
        existing_e = FileEntry(window, "existing roi archive", existing)
        
        save_roi_e = FileEntry(window, "file to save rois in", save_roi, save=True)
        
        groups_e = FileEntry(window, "groups as rois", groups)
        
        rwidth_s = LabeledScale(window, 10, 100, "roi width", rwidth)
        
        rheight_s = LabeledScale(window, 10, 90, "roi height", rheight)
        
        use_exists, use_save, = tk.BooleanVar(), tk.BooleanVar()
        
        exists_check = tk.Checkbutton(window, variable=use_exists, text="Use an existing roi archive")
        
        save_check = tk.Checkbutton(window, variable=use_save, text="save generated rois")
        
        end = tk.Button(window, text="Done", command=window.destroy)
        
        folder_e.grid(row=0,columnspan=3)
        mask_e.grid(row=1,columnspan=3)
        bx_s.grid(row=2,column=0)
        by_s.grid(row=2,column=1)
        bwidth_s.grid(row=3,column=0)
        bheight_s.grid(row=3,column=1)
        rwidth_s.grid(row=4,column=0)
        rheight_s.grid(row=4,column=1)
        existing_e.grid(row=5,column=0,columnspan=3)
        save_roi_e.grid(row=6,columnspan=3)
        groups_e.grid(row=7,columnspan=3)
        exists_check.grid(row=8,column=0)
        save_check.grid(row=8,column=1)
        end.grid(row=9)
        
        window.mainloop()
        
        cls.folder = folder.get()
        cls.mask = mask.get()
        cls.bg_bx = bx.get()
        cls.bg_by = by.get()
        cls.bg_width = bwidth.get()
        cls.bg_height = bheight.get()
        if use_exists.get():
            cls.existing_roi = existing.get()
        if use_save.get():
            cls.save_roi_name = save_roi.get()
        
        cls.group_file = groups.get()
        
        cls.roi_height = rheight.get()
        
        cls.roi_width = rwidth.get()
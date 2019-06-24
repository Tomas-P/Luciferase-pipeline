#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:56:24 2019

@author: tomas
"""

import tkinter as tk
from tkinter import filedialog as fd
from clock import Clock



class LabeledScale(tk.Frame):
    
    def __init__(self, master, min_v :int, max_v :int, label :str):
        
        tk.Frame.__init__(self, master)

        self.var = tk.IntVar()
        
        scale = tk.Scale(self,
                              from_ = min_v,
                              to = max_v,
                              orient = tk.HORIZONTAL,
                              variable = self.var)
        
        text = tk.Label(self, text=label)
        
        
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

class BackgroundSliders(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.x = LabeledScale(self, 0, 2000, "bx")
        self.y = LabeledScale(self, 0, 2000, "by")
        self.width = LabeledScale(self, 1, 500, "width")
        self.height = LabeledScale(self, 1, 500, "height")

        lbl = tk.Label(self, text="comparison region")

        lbl.grid(row=0)
        self.x.grid(row=1,column=0)
        self.y.grid(row=1,column=1)
        self.width.grid(row=2,column=0)
        self.height.grid(row=2,column=1)

    def get(self) -> tuple:

        return self.x.get(), self.y.get(), self.width.get(), self.height.get()


class FileEntry(tk.Frame):
    
    def __init__(self, master, text:str, folder:bool=False, save:bool=False):
        
        tk.Frame.__init__(self,master)

        self.var = tk.StringVar()
        
        label = tk.Label(self, text=text)
        
        entry = tk.Entry(self, textvariable=self.var)
        
        if folder and save:
            
            raise Exception("Making new folders is outside the mission parameters")
            
        elif folder:
            func = lambda:self.var.set(fd.askdirectory())
            
        elif save:
            func = lambda:self.var.set(fd.asksaveasfilename())
            
        else:
            func = lambda:self.var.set(fd.askopenfilename())
        
        button = tk.Button(self, text=text, command=func)
        
        
        label.grid(row=0,column=0)
        entry.grid(row=0,column=1)
        button.grid(row=0,column=2)
    
    def get(self):
        
        return self.var.get()


class Optional(tk.Frame):

    def __init__(self, master, text :str):

        tk.Frame.__init__(self, master)

        self.var = tk.BooleanVar()

        self.check = tk.Checkbutton(
            self,
            text=text,
            variable=self.var
            )

        self.check.grid()

    def get(self):

        return self.var.get()

class RoiOptions(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        self.existing_roi = FileEntry(self, "existing roi archive")
        self.use_existing_roi = Optional(self, "use existing roi archive")

        self.groups = FileEntry(self, "file with groups")

        self.save_name = FileEntry(self, "name to save rois", save=True)
        self.use_save_name = Optional(self, "save generated rois")

        self.existing_roi.grid(row=0,column=0)
        self.use_existing_roi.grid(row=0,column=1)

        self.save_name.grid(row=1,column=0)
        self.use_save_name.grid(row=1,column=1)

        self.groups.grid(row=2)

    def get(self):

        return {'use existing' : self.use_existing_roi.get(),
                'existing' : self.existing_roi.get(),
                'groups' : self.groups.get(),
                'save rois' : self.use_save_name.get(),
                'roi save file' : self.save_name.get()
                }

class UserInterface(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        self.__background = BackgroundSliders(self)
        self.__rois = RoiOptions(self)
        self.__normalize = Optional(self, "normalize data")
        self.__folder = FileEntry(self, "folder with data images", True)
        self.__mask = FileEntry(self, "segmentation image")
        self.__but = tk.Button(self, text="Ready", command=master.destroy)
        self.__align = Optional(self, "align using SIFT")
        self.__align.var.set(True)
        self.__start_time = Clock(self, "ZT time start time")
        self.__interval = Clock(self, "Time between captures")
                                

        self.__folder.grid(row=0)
        self.__mask.grid(row=1)
        self.__normalize.grid(row=0,column=1)
        self.__align.grid(row=1,column=1)
        self.__background.grid(row=3,column=0)
        self.__start_time.grid(row=3,column=1)
        self.__rois.grid(row=4,column=0)
        self.__interval.grid(row=4,column=1)
        self.__but.grid(row=5)

    @property
    def image_folder(self):

        return self.__folder.get()

    @property
    def mask(self):

        return self.__mask.get()

    @property
    def roi_settings(self):

        return self.__rois.get()

    @property
    def background_bounds(self):

        return self.__background.get()

    @property
    def normalize(self):

        return self.__normalize.get()

    @property
    def align(self):

        return self.__align.get()

    @property
    def start_time(self):

        return self.__start_time.time

    @property
    def interval(self):

        return self.__interval.time

    def save(self, filename):

        with open(filename, 'a') as params:

            params.write("\n\n\n")
            params.write("folder " + self.image_folder + '\n')
            params.write("mask " + self.mask + '\n')
            params.write("roi " + str(self.roi_settings) + "\n")
            params.write("background " + str(self.background_bounds) + "\n")
            params.write("normalize " + str(self.normalize) + "\n")
            params.write("align " + str(self.align) + "\n")


if __name__ == '__main__':

    base = tk.Tk()
    interface = UserInterface(base)
    interface.pack()
    

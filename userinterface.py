import tkinter as tk
from tkinter import filedialog
import json

from paramnames import Pname

class Labeled(tk.Frame):
    X = None

    def __init__(self, master, text, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.lbl = tk.Label(self, text=text)
        self.widget = self.X(self, *args, **kwargs)
        self.lbl.pack(side=tk.TOP)
        self.widget.pack(side=tk.BOTTOM)

class FileEntry(tk.Frame):

    def __init__(self, master, labeltxt, textvar, function):
        tk.Frame.__init__(self, master)
        self.lbl = tk.Label(self,text = labeltxt)
        self.entry = tk.Entry(self, textvariable=textvar)
        f = lambda : textvar.set(function())
        self.button = tk.Button(self, text = labeltxt, command = f)
        self.lbl.grid(row=0,column=0)
        self.entry.grid(row=0,column=1)
        self.button.grid(row=0,column=2)

    @staticmethod
    def getfunction(folder=False, save=False):
        if folder:
            return filedialog.askdirectory
        elif save:
            return filedialog.asksaveasfilename
        else:
            return filedialog.askopenfilename

class Clock(tk.Frame):

    def __init__(self, master, hour_var, minute_var):
        tk.Frame.__init__(self, master)
        self.hour = tk.Scale(self,
                             label="hour",
                             from_=0,
                             to=24,
                             variable=hour_var,
                             orient=tk.HORIZONTAL
                             )
        self.minute = tk.Scale(self,
                               label="minute",
                               from_=0,
                               to=60,
                               variable=minute_var,
                               orient=tk.HORIZONTAL
                               )
        self.hour.pack(side=tk.TOP)
        self.minute.pack(side=tk.BOTTOM)


class LabeledClock(Labeled):
    X = Clock

class UserInterface(tk.Frame):

    def __init__(self, master):

        tk.Frame.__init__(self, master)

        # for anyone complaining that this is a monstrosity,
        # do you really think an intermediate representation
        # would be any better?
        self.parameters = {
            Pname.DATADIR.value : tk.StringVar(),
            Pname.MASK.value : tk.StringVar(),
            Pname.GROUPS.value : tk.StringVar(),
            Pname.NORM.value : tk.BooleanVar(),
            Pname.ALIGN.value : tk.BooleanVar(value=True),
            Pname.USE_EXIST.value : tk.BooleanVar(),
            Pname.SAVE_GEN.value : tk.BooleanVar(),
            Pname.EXIST_ROI.value : tk.StringVar(),
            Pname.NEW_ROI.value : tk.StringVar(),
            Pname.BG.value : tk.StringVar(),
            Pname.START.value : {
                Pname.HOUR.value : tk.IntVar(),
                Pname.MINUTE.value : tk.IntVar(),
                },
            Pname.INTERVAL.value : {
                Pname.HOUR.value : tk.IntVar(),
                Pname.MINUTE.value : tk.IntVar()
                },
            }
            
        self.getfolder = FileEntry(self,
                                   "Folder with data",
                                   self.parameters[Pname.DATADIR.value],
                                   FileEntry.getfunction(True)
                                   )
        self.getmask = FileEntry(self,
                                 "Image for segmentation",
                                 self.parameters[Pname.MASK.value],
                                 FileEntry.getfunction()
                                 )
        self.getgroups = FileEntry(self,
                                   "Group archive",
                                   self.parameters[Pname.GROUPS.value],
                                   FileEntry.getfunction()
                                   )
        self.background = FileEntry(self,
                                    "Background file",
                                    self.parameters[Pname.BG.value],
                                    FileEntry.getfunction()
                                    )
        self.use_existing = tk.Checkbutton(self,
                                           text="Use existing ROIs?",
                                           variable=self.parameters[Pname.USE_EXIST.value],
                                           )
        self.save_gen = tk.Checkbutton(self,
                                       text="Save generated ROIs?",
                                       variable=self.parameters[Pname.SAVE_GEN.value],
                                       )
        self.align = tk.Checkbutton(self,
                                    text="Align using SIFT?",
                                    variable=self.parameters[Pname.ALIGN.value],
                                    )
        self.normalize = tk.Checkbutton(self,
                                        text="Normalize data?",
                                        variable=self.parameters[Pname.NORM.value]
                                        )
        self.extant_roi_archive = FileEntry(self,
                                "Archive with existing ROIs",
                                self.parameters[Pname.EXIST_ROI.value],
                                FileEntry.getfunction()
                                )
        self.new_roi_archive = FileEntry(self,
                                         "Archive to save generated ROIs",
                                         self.parameters[Pname.NEW_ROI.value],
                                         FileEntry.getfunction(save=True)
                                         )
        self.start = LabeledClock(self,
                                  "start time",
                                  hour_var=self.parameters[Pname.START.value][Pname.HOUR.value],
                                  minute_var=self.parameters[Pname.START.value][Pname.MINUTE.value],
                                  )
        self.interval = LabeledClock(self,
                                     "interval",
                                     hour_var=self.parameters[Pname.INTERVAL.value][Pname.HOUR.value],
                                     minute_var=self.parameters[Pname.INTERVAL.value][Pname.MINUTE.value]
                                     )
        self.confirm = tk.Button(self,text="Done",command=master.destroy)
        self.cancel = tk.Button(self,text="Cancel",command=exit)
        
        self.getfolder.grid(row=0,columnspan=3)
        self.getmask.grid(row=1,columnspan=3)
        self.getgroups.grid(row=2,columnspan=3)
        self.background.grid(row=3,columnspan=3)
        self.use_existing.grid(row=4,column=0)
        self.save_gen.grid(row=4,column=1)
        self.align.grid(row=5,column=0)
        self.normalize.grid(row=5,column=1)
        self.extant_roi_archive.grid(row=8,columnspan=3)
        self.new_roi_archive.grid(row=9,columnspan=3)
        self.start.grid(row=10,column=0)
        self.interval.grid(row=10,column=1)
        self.confirm.grid(row=11,column=0)
        self.cancel.grid(row=11,column=1)
        
    def get_parameters(self):
        new = {}
        for name in self.parameters:
            if isinstance(self.parameters[name], dict):
                new[name] = {subname : self.parameters[name][subname].get() for subname in self.parameters[name]}
            else:
                new[name] = self.parameters[name].get()
        return new

def ask_user():
    t = tk.Tk()
    interface = UserInterface(t)
    interface.pack()
    t.mainloop()
    return interface.get_parameters()

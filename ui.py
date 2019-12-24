import tkinter as tk
from tkinter import filedialog
import json


class LabeledX(tk.Frame):
    X = None

    def __init__(self, master, text, *args, **kwargs):

        tk.Frame.__init__(self, master)
        
        self.lbl = tk.Label(self, text=text)

        self.widget = self.X(self, *args, **kwargs)

        self.lbl.pack(side=tk.LEFT)

        self.widget.pack(side=tk.LEFT)


class LabeledSpinbox(LabeledX):
    X = tk.Spinbox


class LabeledEntry(LabeledX):
    X = tk.Entry


class LabeledScale(LabeledX):
    X = tk.Scale


class FileEntry(tk.Frame):

    def __init__(self, master, text, textvar, folder=False, save=False):
        tk.Frame.__init__(self, master)
        self.entry = LabeledEntry(self, text, textvariable=textvar)

        self.folder = folder
        self.save = save
        function = self.get_function()

        self.button = tk.Button(self,
                                text=text,
                                command=lambda:textvar.set(function())
                                )
        self.entry.pack(side=tk.LEFT)
        self.button.pack(side=tk.RIGHT)

    def get_function(self):
        if self.folder:
            return filedialog.askdirectory
        elif self.save:
            return filedialog.asksaveasfilename
        else:
            return filedialog.askopenfilename

class Clock(tk.Frame):

    def __init__(self, master, text, hour_var, minute_var):

        tk.Frame.__init__(self, master)

        self.__h = hour_var
        self.__m = minute_var

        self.__hour = LabeledSpinbox(self,
                                     "hour",
                                     from_=0,to=24,
                                     textvariable=self.__h
                                     )
        self.__minute = LabeledSpinbox(self,
                                       "minute",
                                       from_=0,
                                       to=60,
                                       textvariable=self.__m)
        self.__label = tk.Label(self, text=text)

        self.__label.grid(row=0)
        self.__hour.grid(row=1)
        self.__minute.grid(row=2)

    @property
    def hour(self):
        return int(self.__h.get())

    @property
    def minute(self):
        return int(self.__m.get())

        

class Parameters:

    def __init__(self):
        self.folder = tk.StringVar()
        self.mask = tk.StringVar()
        self.groups = tk.StringVar()
        self.normalize = tk.BooleanVar()
        self.align = tk.BooleanVar()
        self.align.set(True)
        self.existing_rois = tk.StringVar()
        self.rois_savename = tk.StringVar()
        self.use_existing_rois = tk.BooleanVar()
        self.save_generated_rois = tk.BooleanVar()
        # b is short for background
        # the next four are bounds for a comparison region
        self.bx = tk.StringVar()
        self.by = tk.StringVar()
        self.b_width = tk.StringVar()
        self.b_height = tk.StringVar()
        self.start_hour = tk.IntVar()
        self.start_minute = tk.IntVar()
        self.interval_hours = tk.IntVar()
        self.interval_minutes = tk.IntVar()
        

    def to_dict(self):
        return {
            "folder" : self.folder.get(),
            "maskfile" : self.mask.get(),
            "groupfile" : self.groups.get(),
            "normalize" : self.normalize.get(),
            "align" : self.align.get(),
            "existing rois" : self.existing_rois.get(),
            "filename to save rois" : self.rois_savename.get(),
            "use existing rois" : self.use_existing_rois.get(),
            "save generated rois" : self.save_generated_rois.get(),
            "background" : {
                "bx" : self.bx.get(),
                "by" : self.by.get(),
                "width" : self.b_width.get(),
                "height" : self.b_height.get()
                },
            "start time" : {
                "hour" : self.start_hour.get(),
                "minute" : self.start_minute.get()
                },
            "interval" : {
                "hours" : self.interval_hours.get(),
                "minutes" : self.interval_minutes.get(),
                }
            }

    def saveas(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file)
    

class UserInterface(tk.Frame):

    def __init__(self, master, params):

        tk.Frame.__init__(self, master)

        self.params = params
        self.folder = FileEntry(self,"folder with data",self.params.folder,True)
        self.mask = FileEntry(self,"segmentation image",self.params.mask)
        self.groups = FileEntry(self,"experimental groups",self.params.groups)
        self.normalize = tk.Checkbutton(self,
                                        text="normalize data",
                                        variable=self.params.normalize
                                        )
        self.align = tk.Checkbutton(self,
                                    text="align using SIFT",
                                    variable=self.params.align
                                    )
        self.existing = tk.Checkbutton(self,
                                       text="use existing rois",
                                       variable=self.params.use_existing_rois
                                       )
        self.save_gen = tk.Checkbutton(self,
                                       text="save generated rois",
                                       variable=self.params.save_generated_rois
                                       )
        self.extant_rois = FileEntry(self,
                                     "existing rois",
                                     self.params.existing_rois
                                     )
        self.save_rois_to = FileEntry(self,
                                      "save generated rois as",
                                      self.params.rois_savename,
                                      save=True
                                      )
        self.bx = LabeledSpinbox(self,
                                 "background bx",
                                 textvariable=self.params.bx
                                 )
        self.by = LabeledSpinbox(self,
                                 "background by",
                                 textvariable=self.params.by
                                 )
        self.b_width = LabeledSpinbox(self,
                                      "background width",
                                      textvariable=self.params.b_width
                                      )
        self.b_height = LabeledSpinbox(self,
                                       "background height",
                                       textvariable=self.params.b_height
                                       )
        self.start_clock = Clock(self,
                                 "start time",
                                 params.start_hour,
                                 params.start_minute
                                 )
        self.interval_clock = Clock(self,
                                    "interval between captures",
                                    params.interval_hours,
                                    params.interval_minutes
                                    )
        self.finish = tk.Button(self, text="Done", command=master.destroy)

        self.halt = tk.Button(self, text="Cancel", command=lambda:exit())
        
        self.setup()

    def setup(self):
        
        self.folder.grid(columnspan=3)
        self.mask.grid(columnspan=3)
        self.groups.grid(columnspan=3)

        self.align.grid()
        self.normalize.grid()
        self.existing.grid()
        self.save_gen.grid()

        self.extant_rois.grid(columnspan=3)
        self.save_rois_to.grid(columnspan=3)

        self.bx.grid(columnspan=2)
        self.by.grid(columnspan=2)
        self.b_width.grid(columnspan=2)
        self.b_height.grid(columnspan=2)

        self.start_clock.grid()
        self.interval_clock.grid()

        self.finish.grid(row=15,column=0)
        self.halt.grid(row=15,column=1)

    def parameters(self):

        return self.params

if __name__ == '__main__':
    t = tk.Tk()
    p = Parameters()
    ui = UserInterface(t, p)
    ui.pack()
    t.mainloop()
    

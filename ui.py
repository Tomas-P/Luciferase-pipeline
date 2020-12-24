
import tkinter as tk
from tkinter import filedialog
from parameter import Param
from datetime import datetime

class Labeled(tk.Frame):
    X = None

    def __init__(self, master, text, *args, **kwargs):
        tk.Frame.__init__(self, master)
        self.lbl = tk.Label(self, text=text)
        self.widget = self.X(self, *args, **kwargs)
        self.lbl.pack(side=tk.LEFT)
        self.widget.pack(side=tk.RIGHT)

class LabeledEntry(Labeled):
    X = tk.Entry

class FileEntry(tk.Frame):

    def __init__(self,master, txt, var, func):
        tk.Frame.__init__(self,master)
        label = tk.Label(self, text = txt)
        entry = tk.Entry(self, textvariable=var)
        f = lambda : var.set(func())
        button = tk.Button(self, text = txt, command = f)
        label.grid(row=0,column=0)
        entry.grid(row=0,column=1)
        button.grid(row=0,column=2)

    @staticmethod
    def getfunc(which :Param):
        if which == Param.DATA:
            return filedialog.askdirectory
        elif which == Param.MASK or which == Param.GROUPING or which == Param.BACKGROUND:
            return filedialog.askopenfilename
        elif which == Param.ROI:
            def toggle(to_generate):
                if to_generate:
                    return filedialog.asksaveasfilename
                else:
                    return filedialog.askopenfilename

            return toggle
        return

class UserInterface(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self,master)
        self.args = {
            Param.BACKGROUND : tk.StringVar(),
            Param.DATA : tk.StringVar(),
            Param.MASK : tk.StringVar(),
            Param.GROUPING : tk.StringVar(),
            Param.GENERATE : tk.BooleanVar(value=True),
            Param.ROI : tk.StringVar(),
            Param.NORM : tk.BooleanVar(value=False),
            Param.INIT : tk.StringVar(),
            Param.ELAPSED : tk.StringVar(),
            }
        background = FileEntry(self,
                               "background zone",
                               self.args[Param.BACKGROUND],
                               FileEntry.getfunc(Param.BACKGROUND)
                               )
        data = FileEntry(self,
                         "data folder",
                         self.args[Param.DATA],
                         FileEntry.getfunc(Param.DATA)
                         )
        mask = FileEntry(self,
                         "segmentable image",
                         self.args[Param.MASK],
                         FileEntry.getfunc(Param.MASK)
                         )
        groups = FileEntry(self,
                           "group archive",
                           self.args[Param.GROUPING],
                           FileEntry.getfunc(Param.GROUPING)
                           )
        generate = tk.Checkbutton(self,
                                  text="generate ROI selections?",
                                  variable=self.args[Param.GENERATE],
                                  )
        def roifunc():
            toggle = FileEntry.getfunc(Param.ROI)
            return toggle(self.args[Param.GENERATE].get())
        
        roi = FileEntry(self,
                        "ROI selection archive name",
                        self.args[Param.ROI],
                        lambda : (roifunc()())
                        )
        normalize = tk.Checkbutton(self,
                                   text="normalize data?",
                                   variable=self.args[Param.NORM],
                                   )
        init = LabeledEntry(self,
                            "time of first image capture",
                            textvariable=self.args[Param.INIT])

        elapsed = LabeledEntry(self,
                               "time elapsed between photographs, in hours",
                               textvariable=self.args[Param.ELAPSED])

        confirm = tk.Button(self, text="Done", command=master.destroy)
        cancel = tk.Button(self, text="Cancel", command=exit)
        
        background.grid(row=0)
        data.grid(row=1)
        mask.grid(row=2)
        groups.grid(row=3)
        generate.grid(row=4)
        roi.grid(row=5)
        normalize.grid(row=6)
        init.grid(row=7)
        elapsed.grid(row=8)
        confirm.grid(row=9, column=0)
        cancel.grid(row=9, column = 1)

    def get(self):
        new = {}
        for name in self.args:
            new[name] = self.args[name].get()
        return new

    def log(self):
        arguments = self.get()
        now = datetime.now()
        with open("Usagelog.txt", "a") as log:
            log.write("-----\n")
            log.write(str(now) + '\n')
            log.write(str(arguments) + "\n")
        return

def ask_user():
    t = tk.Tk()
    interface = UserInterface(t)
    interface.pack()
    t.mainloop()
    interface.log()
    return interface.get()

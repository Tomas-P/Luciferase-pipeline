
import tkinter as tk
from tkinter import filedialog
from labeled import LabeledSpinbox, LabeledEntry, LabeledScale

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

    

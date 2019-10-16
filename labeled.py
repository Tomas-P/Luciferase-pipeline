import tkinter as tk

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


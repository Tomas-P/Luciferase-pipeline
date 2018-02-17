# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:59:19 2018

@author: Tomas
"""


class ImageJ:

    location = "C:\\Users\\Tomas\\Documents\\Fiji.app\\"
    from subprocess import PIPE
    from subprocess import run as __run
    from multiprocessing import Process as __Process

    @classmethod
    def run(cls, commands, os="Windows",bits=64):
        if os=="Windows" and bits==64:
            name = "ImageJ-win64.exe"
        elif os=="Windows" and bits==32:
            name = "ImageJ-win64.exe"
        elif os=="Linux" and bits==64:
            name = "ImageJ-linux64"
        elif os=="Linux" and bits==32:
            name = "ImageJ-linux32"
        program = cls.location + name
        program_args = program + ' ' + commands
        return cls.__run(program_args, stdout=cls.PIPE)
    
    @classmethod
    def update_location(cls, new_location):
        cls.location = new_location

    @classmethod
    def do(cls, commands, os="Windows", bits=64):
        p = cls.__Process(target=cls.run,args=(commands,os,bits))
        p.start()
        return p
        
def editor():
    from tkinter import Tk,Text,Button,StringVar
    base = Tk()
    text_var = StringVar(base)
    textbox = Text(base)
    textbox.pack()
    Button(base,command=lambda:text_var.set(textbox.get("0.0","end")),text="save").pack()
    Button(base,command=base.destroy,text="exit").pack()
    base.mainloop()
    return text_var.get()

def prepare(macro:str)->str:
    def oneline_ize(string):
        return ''.join(string.split('\n'))
    def reqoute(string):
        return string.replace('''"''',"'")
    m = reqoute(oneline_ize(macro))
    return '--headless -eval "{0}"'.format(m)

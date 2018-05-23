# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 19:20:21 2018

@author: Tomas
"""

import glob



class Folder:
    
    def __init__(self,name):
        self.name = name
        self.files = [item.replace('\\',
                                   '/') for item in glob.glob(name+'/*')]
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self,key):
        return self.files[key]
    
    @staticmethod
    def concat_digits(filename:str)->int:
        return int(''.join(char for char in filename if char in '0123456789'))
    
    def sort(self):
        self.files.sort(key=self.concat_digits)
    
    def search(self,flag):
        return [file for file in self.files if flag in file]
    
    def only_files(self):
        for item in self.files:
            if item[-4] != '.':
                return False
        return True

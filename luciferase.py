import json
from os.path import isfile
import glob

class Config:
    
    IMAGEJ = 'imagej'
    DATA = 'data'
    CSV = 'csv'
    GROUP_SIZE = 'group size'
    GROUP_COUNT = 'group_count'
    
    @classmethod
    def __ui(cls)->dict:
        from tkinter.filedialog import askdirectory
        
        config = {}
        
        config[cls.DATA] = askdirectory(title="choose the folder with your images")
        config[cls.IMAGEJ] = askdirectory(title="choose the imagej folder")
        config[cls.CSV] = askdirectory(title="choose the folder where you will save the .csv file")
        
        valid_input= False
        
        size_prompt = "how many plants are in each group? "
        count_prompt = "how many groups are in the experiment? "
        while not valid_input:
            try:
                config[cls.GROUP_SIZE] = int(input(size_prompt))
                config[cls.GROUP_COUNT] = int(input(count_prompt))
            except ValueError:
                print("you seem to have entered invalid input")
                continue
            
            valid_input = True
        
        return config
    
    def __init__(self,imagej,data,csv,g_size,g_count):
        self.imagej = imagej
        self.data = data
        self.csv = csv
        self.group_size = g_size
        self.group_count = g_count
    
    @classmethod
    def readfile(cls,filename='config.json'):
        with open(filename) as fhandle:
            config = json.load(fhandle)
        
        imagej = config[cls.IMAGEJ]
        data = config[cls.DATA]
        csv = config[cls.CSV]
        group_size = config[cls.GROUP_SIZE]
        group_count = config[cls.GROUP_COUNT]
        
        return cls(imagej,data,csv,group_size,group_count)
    
    @classmethod
    def fromui(cls):
        config = cls.__ui()
        imagej = config[cls.IMAGEJ]
        data = config[cls.DATA]
        csv = config[cls.CSV]
        group_size = config[cls.GROUP_SIZE]
        group_count = config[cls.GROUP_COUNT]
        
        return cls(imagej,data,csv,group_size,group_count)
    
    def save(self,filename='config.json'):
        config = {}
        config[self.IMAGEJ] = self.imagej
        config[self.DATA] = self.data
        config[self.CSV] = self.csv
        config[self.GROUP_SIZE] = self.group_size
        config[self.GROUP_COUNT] = self.group_count
        
        with open(filename,'w') as fhandle:
            json.dump(config,fhandle)
    
    @classmethod
    def auto(cls,filename='config.json'):
        if isfile(filename):
            return cls.readfile(filename)
        else:
            config = cls.fromui()
            config.save(filename)
            return config

class Folder:
    
    def __init__(self,foldername):
        self.name = foldername
        self.files = sorted([file.replace('\\','/') for file in glob.glob(foldername + '/*')])
    
    def search(self,name_fragment):
        return [item for item in self.files if name_fragment in item]
    
    def __getitem__(self,key):
        return self.files[key]
    
    def __len__(self):
        return len(self.files)

class ImageJ:
    
    import subprocess as sub
    
    @staticmethod
    def get_name(config :Config)->str:
        ijfolder = Folder(config.imagej)
        return ijfolder.search('ImageJ-')[0]
    
    def __init__(self,name):
        self.name = name
        self.exe = Folder(name).search('ImageJ-')[0]
    
    def run(self,commands='',*args,**kwargs):
        program = self.exe if commands == '' else self.exe + ' ' + commands
        return self.sub.Popen(program,*args,**kwargs)

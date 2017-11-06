from skimage.io import imread
import glob
import tkinter
from tkinter import ttk, filedialog


def update(tag, collection, function):
    '''update collection at tag with the output of function()'''
    collection[tag] = function()

class Pixel(dict):
    "Store data associated with a pixel"
    def get_data(self, xpos, ypos, segment_array, data_array):
        "Aquire all relevant information and use it to update the Pixel object."
        self['x'] = xpos #position
        self['y'] = ypos
        #checking for correct type
        if not isinstance(segment_array[xpos][ypos], bool):
            raise TypeError(f'''An invalid value of {segment_array[xpos][ypos]} exists at the current
position in the segmentation array at ({xpos},{ypos}).''')
        self['data'] = segment_array[xpos][ypos] #update with whether data
        self['value'] = data_array[xpos][ypos] #update with value

class Folder:
    '''stores the names of files in a folder and the folder path.
Gives the ability to read in images one at a time from the folder
and can locate files in the folder with any given extension. Does not work for
folders with subfolders.'''
    def __init__(self, foldername):
        self.foldername = foldername
        self.files = [file.replace('\\','/') for
                      file in glob.glob(foldername + '/*')]
        #sort the files to ensure their orderly occurence
        self.files.sort()
        if all((file[-4]=='.' for file in self.files)):
            self.only_files = True
        else:
            self.only_files = False

    def next_image(self):
        '''takes the imagename in the relevant position
and reads the image into memory as a NamedImage object.
Raises an error if not all files have an extension.'''
        assert self.only_files is True
        for file in self.files:
            yield NamedImage(file)

    def locate_filetype(self, ext):
        "Returns all filenames with a specific extension in the folder."
        return [file for file in self.files if file.endswith(ext)]

class NamedImage:
    "contains an image as an array and the filename of that image."
    def __init__(self, imagename):
        self.name = imagename
        self.array = imread(imagename)

class Config(dict):
    '''A class used to store such information as
    * the folder in which raw images are
    * the folder containing the imagej installation
    * the folder in which proccessed images will be kept
    * the folder in which segmentation images (images that show which pixels
    are actual data) will be kept.
    This information is stored-long term as a file designated by
    the class constant CONFIGFILE. Try to avoid making more instances
    of this class than nessesary.
    '''
    CONFIGFILE = 'config.json'
    
    def file_exists(self, file=CONFIGFILE):
        "a function to check if the config file exists."
        #check if the file exists
        try:
            conf = open(file)

        #if it doesn't, return False
        except FileNotFoundError:
            return False
            # the return statement should
            # make the function exit and not run any more code

        #if it does exist, close the file and return True
        conf.close()
        return True

    def ui(self):
        "Implements a crude user interface to set config values."
        root = tkinter.Tk()
        ttk.Button(root,
                   text="Click here when you are satified with your selections.",
                   command=root.destroy).pack()
        for item in ['data images','ROI images','raw images','ImageJ installation']:
            ttk.Button(root,
                       text=f"Choose the folder with your {item}",
                       command=lambda:update(item,
                                             self,
                                             filedialog.askdirectory
                                             )
                       ).pack()
        root.mainloop()

    def load(self, file=CONFIGFILE):
        "load information from the relevant file."
        with open(file) as conf:
            data = json.load(conf)
        for key,value in data.items():
            self[key] = value

    def write(self, file=CONFIGFILE):
        "Write information to the relevant file."
        writable = {}
        for key,value in self.items():
            writable[key] = value
        with open(file, 'w') as confile:
            json.dump(writable, confile)

    def __init__(self, file=CONFIGFILE):
        "Initializes an object of the Config class."
        if self.file_exists(file): # check if the config file exists
            self.load(file) #if it does, we can load in the info with ease
        else:               #otherwise
            self.ui()       #get the revelant info
            self.write(file)#save the information for later

def midpoint(ls):
    "finds the object at the aproximate midpoint of a list"
    return ls[int(len(ls)/2)]

class ImageData:
    '''A class that stores an image's data and it's segmenation.
It can also give pixel by pixel access, or do some simple calculations.'''
    def __init__(self, named_data, named_roi):
        '''creates an ImageData object based on a data NamedImage and
an roi NamedImage.'''
        self.data = named_data.array
        self.data_name = named_data.name
        self.roi = named_roi.array
        self.roi_name = named_roi.name

    def next_pixel(self):
        """Yields the next pixel in the image going left to right, top to bottom.
I hope."""
        for i,row in enumerate(self.data):
            for j in range(len(self.data[0])):
                pix = Pixel()
                pix.get_data(i, j, self.roi, self.data)
                yield pix

    def median(self):
        "finds the median value of an image."
        vals = [pixel['value'] for pixel in
                self.next_pixel()]
        vals.sort()
        return midpoint(vals)

    def data_median(self):
        "finds the median of data pixels in an image."
        vals = [pixel['value'] for pixel in self.next_pixel() if pixel['data']]
        vals.sort()
        return midpoint(vals)

    def mean(self):
        "finds the mean of value of an image."
        total = image.data.sum()
        return total / (len(image.data) * len(image.data[0]))

    def data_mean(self):
        "Finds the mean of data in the image."
        total = 0
        datapoints = 0
        for pixel in self.next_pixel():
            if pixel['data']:
                total += float(pixel['value'])
                datapoints += 1
        return total / datapoints

    def mode(self):
        "Find the mode of the entire image."
        counts = {}
        for pixel in self.next_pixel():
            if pixel['value'] not in counts:
                counts[pixel['value']] = 1
            else:
                counts[pixel['value']] += 1

        md = max(counts.values())
        for key,value in counts:
            if value==md:
                return key

    def data_mode(self):
        "Find the mode of the data in the image."
        counts = {}
        for pixel in self.next_pixel():
            if pixel['data'] and not pixel['value'] in counts.keys():
                counts[pixel['value']] = 1
            elif pixel['data'] and pixel['value'] in counts.keys():
                counts[pixel['value']] += 1

        md = max(counts.values())
        for key, value in counts:
            if value==md:
                return key

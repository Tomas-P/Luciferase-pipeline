from skimage.io import imread
from tkinter import Tk, BOTTOM, Button, filedialog
import glob
import json
from subprocess import run

# functions for the config class GUI
def get_rois():
    global global_rois_directory
    global_rois_directory = filedialog.askdirectory()

def get_data_images():
    global global_data_directory
    global_data_directory = filedialog.askdirectory()

def get_ImageJ():
    global global_imagej_directory
    global_imagej_directory = filedialog.askdirectory()

def get_raw_images():
    global global_raws_directory
    global_raws_directory = filedialog.askdirectory()

    
class PixelHolder(dict):
    # stores data associated with a pixel
    def get_data(self, xpos, ypos, segment_array, data_array):
        # the x position of the pixel
        self['x'] = xpos
        # the y position of the pixel
        self['y'] = ypos
        # wether the pixel represents data

        # set the is data flag to true if the position is true
        if segment_array[xpos][ypos] == True:
            # I think the representation that gets loaded in is
            # an array of True or False
            # because of the use of the PIL.Image().convert() method
            # in a different script to make the ROI segmentations black and white
            self['is data'] = True
        # set the is data flag to true if the position is false or 0 (also deals with multiple representations)
        elif segment_array[xpos][ypos] == False:
            # 
            self['is data'] = False
        else:
            # a section that was used for debugging
            # it is here to tell the programmer that an invalid value was found in the segmentation array, and what that value was
            raise ValueError("Something is wrong. The value of the current position is {0}".format(segment_array[xpos][ypos]))
        # what data the pixel holds
        self['data'] = data_array[xpos][ypos]
        self['black'] = data_array[xpos][ypos] == 255

class Folder():
    # stores the names of files in an image
    def __init__(self, foldername):
        self.foldername = foldername
        self.files = [file.replace('\\', '/') for file in glob.glob(foldername + '/*')]
        self.files.sort()
        self.only_files = True
        for file in self.files:
            if file[-4] != '.':
                self.only_files = False
    def read_in_next_image(self):
        # reads the next image in self.files into memory
        # this is a generator function
        for file in self.files:
            yield ImageWithName(file)

class ImageWithName:
    # keeps together an image with it's name
    def __init__(self, imagename):
        self.array = imread(imagename)
        self.name = imagename

class Config:
    # stores config information
    # like which file has the config info

    def check_config_file_exists_works(self, config_filename='config.json'):
        try: # check if the file exist
            conf = open(config_filename, 'r')
        except: # the file doesn't exist
            return False 
        else: # the file exists
            conf.close() # has to be done if there is no with statement
            return True

    def do_setup(self, config_filename='config.json'):
        # dictionary object to hold key information
        config_data = {}
        # interactive prompts for easy setup
        # using the tkinter library
        # the reason I'm using(some would say abusing) the global namespace
        # is to get information OUT from the tkinter window in a way that might
        # work. It is crude, I do admit that.
        #creating the window and forming all of the buttons on it
        root = Tk()
        Button(root, text="Click here when you are happy with your selections", command=root.destroy).pack(side=BOTTOM)
        Button(root, text="Choose the folder with your data images", command=get_data_images).pack()
        Button(root, text="Choose the folder with your ImageJ installation", command=get_ImageJ).pack()
        Button(root, text="Choose the folder with your ROI selection images", command=get_rois).pack()
        Button(root, text="Choose the folder with your raw data images", command=get_raw_images).pack()
        # essentially, the program will not continue until the mainloop is finished
        root.mainloop()
        
        # giving the object the information needed for the configuration
        config_data['ImageJ folder'] = global_imagej_directory
        config_data['Data images'] = global_data_directory
        config_data['ROI images'] = global_rois_directory
        config_data['raw folder'] = global_raws_directory
        
        # actually writing the information to a file
        with open(config_filename, 'w') as conf:
            json.dump(config_data, conf)

    def load_info(self):
        with open('config.json', 'r') as conf:
            return json.load(conf)

    def __init__(self, special_config=False):
        if special_config is not False: # someone used specialty settings
            self.config_data =  special_config

        elif self.check_config_file_exists_works(): # the config has already been done
            self.config_data =  self.load_info() # load in the configuration

        else: # config has not been done yet
            self.do_setup() # set up the config
            self.config_data = self.load_info() # load in the new configuration

    def reset_config(self, config_filename='config.json'):
        # to be called if the user wants a full reset of the config file
        if not self.check_config_file_exists_works(): #check to see if it doesn't exist
            pass # function should exit here, as there is nothing to do
            # pass is only here for syntax reasons
        else: # the file does exist
            # deletes the file
            # using shell=True may create security issues
            # but this is an image analysis program
            run('DEL {0}'.format(config_filename), shell=True) 

class ImageDataPoints:
    # a class that stores data from an image and its ROI image
    
    def __init__(self, named_data, named_roi):
        # takes two ImageWithName arguments, the first is the
        # data, the second is the ROI image, both are arrays which are passed in
        self.data = named_data
        self.roi = named_roi

    def average_data_ignore_black(self):
        # averages pixels identified as data that are not
        # black and therefore have data
        total = 0
        for pixel in self.generate_each_pixel_in_order():
            if pixel['is data'] == True and pixel['black'] == False: # nondata and black pixels are ignored
                total += pixel['data']
        return total / sum((1 for i in self.generate_each_pixel_in_order() if i['is data'] == True and i['black'] == False))

    def average_data(self):
        # averages pixels identified as data
        total = 0
        for pixel in self.generate_each_pixel_in_order():
            if pixel['is data'] == True:
                # call float to prevent overflow errors
                # which are caused because numpy wants to be
                # fast
                total += float(pixel['data'])
        return total / sum((1 for i in self.generate_each_pixel_in_order() if i['is data'] == True))
    
    def generate_each_pixel_in_order(self):
        # yields the next pixel in the image, reading right to left, top to bottom
        for i in range(len(self.data.array)):
            for j in range(len(self.data.array[0])):
                pix = PixelHolder()
                pix.get_data(i, j, self.roi.array, self.data.array)
                yield pix

# run largely to test whether the module works             
if __name__ == '__main__':
    # initiallizing the Config object should only happen once
    configuration = Config()

    # putting the folder information into memory
    datas = Folder(configuration.config_data['Data images'])
    ROIs = Folder(configuration.config_data['ROI images'])
    ImageJ_folder = Folder(configuration.config_data['ImageJ folder'])

    #  The following is a demonstration of the code working
    #  It works like so:
    #  iterate through each data image object, and in each iteration,
    #
    #  print what position in the list of files is currently being used
    #  read in the correct ROI image object based on the position
    #  check that the ROI image object is unique
    #  create the object that integrates the ROI and data information
    #  increment the position variable by one
    #  print the average of the values of all pixels in the image identified as data,
    #  followed by the average of the values of all the pixels identified as data that are not black

    
    i = 0 # used to remember the position in the set of files
    ids = [] # used to remember if roi objects are unique
    for data in datas.read_in_next_image(): # iterating through each data object
        print(i) # printing the position
        if i == 0: # read in the first image in the case that the position is in the initial location
            roi = next(ROIs.read_in_next_image())
            
        else: # if the position is not in the initial location
            for j in range(i): # iterate forward and create the roi object at the correct possition
                roi = next(ROIs.read_in_next_image())

        if id(roi) in ids: # check that the roi object is unique and therefore is not a duplicate of a previous image
            raise Exception('Using an image ROI for multiple images should not occur') # raise an exception if the roi is the same as a previous roi
            # becuase you don't want to accidentally analyze plant data with the wrong dataset about where they are
        
        elif id(roi) not in ids: # if the roi object is unique
            ids.append(id(roi)) # append its signature to the list of ids for future comparison
            
        # if this is reached, everything is in order
        Image = ImageDataPoints(data, roi) # create the object that associates the data and Region Of Interest (ROI) information
        i += 1 # increment the position in the list by one. Important to getting the correct ROI image to be used
        avg = Image.average_data()
        blk = Image.average_data_ignore_black()
        print(avg, blk)

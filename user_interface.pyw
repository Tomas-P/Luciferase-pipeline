import tkinter as tk
from tkinter import ttk
import time
import multiprocessing as multi


def filtering(prep, contrast):
    import image_filtering as im_filter
    from contrast_filtering import contrast_filter

    if prep:
        config = im_filter.Config()
        imagej = im_filter.Folder(config.config_data['ImageJ folder'])
        data = im_filter.Folder(config.config_data['Data images'])
        macro_folder = im_filter.finding_macro_dir(imagej)
        im_filter.Preproccess(macro_folder, data.foldername, imagej.foldername)

    if contrast:
        contrast_filter()

       
def data_gather():
    data_window = tk.Tk()
    contrast = tk.IntVar()
    preps = tk.IntVar()
    #prevent anything from running too early
    contrast.set(0)
    preps.set(0)
    enhance_contrast = ttk.Checkbutton(data_window,
                                       text='enhance the image contrast in ImageJ',
                                       variable=contrast,
                                       offvalue=0,
                                       onvalue=1)
    enhance_contrast.pack(fill=tk.X)

    
    prep = ttk.Checkbutton(data_window,
                           text='filter noise from the images',
                           variable=preps,
                           offvalue=0,
                           onvalue=1)
    prep.pack(fill=tk.X)
    cont = ttk.Button(data_window,
                      text="Continue",
                      command=data_window.destroy)
    cont.pack(side=tk.BOTTOM)
    data_window.mainloop()
    filtering(preps.get(),contrast.get())


def find_rois():
    import roi_script_early_version as rsev
    config = rsev.Config()
    ImageJ = rsev.Folder(config.config_data['ImageJ folder'])
    data_ims = rsev.Folder(config.config_data['Data images'])
    roi_ims = rsev.Folder(config.config_data['ROI images'])
    for i, file in enumerate(data_ims.files):
        comms = rsev.write_ImageJ_commands(ImageJ,
                ["open('{0}');".format(file.replace(
                '/', '\\\\')),
                 "run('Statistical Region Merging', 'q=25 showaverages');",
                 "saveAs('Tiff', '{0}\\\\roi{1}.tif');".format(roi_ims.foldername.replace(
                '/', '\\\\'), i)
                 ])
        rsev.run(comms, shell=True)

    from roi_converter import convert_all_rois as roi_convert
    roi_convert(config)


def analysis():
    from simple_analysis import analyze
    analyze()

# make sure the folders are there when they are needed
from data_storing_objects import Config
conf = Config()
# remove the object from the namespace because it will never be needed again
del conf

window1 = tk.Tk()

explain = ttk.Label(window1,
                      text="Click the buttons to do various tasks")
explain.pack(fill=tk.X,side=tk.TOP)

fil = tk.IntVar()

filter1 = ttk.Checkbutton(window1,
                          text="filter out noise",
                          variable=fil)
filter1.pack(fill=tk.X)

roi = tk.IntVar()

rois = ttk.Checkbutton(window1,
                       text="find Regions of Interest",
                       variable=roi)
rois.pack(fill=tk.X)

anly = tk.IntVar()

analy = ttk.Checkbutton(window1,
                        text="analyze images",
                        variable=anly)
analy.pack(fill=tk.X)

action = ttk.Button(window1,
                    text="Begin",
                    command=window1.destroy)
action.pack(side=tk.BOTTOM)

window1.mainloop()

#check if fil is one
if fil.get():
    # if so, filter out the noise
    data_gather()

#check if roi is one
if roi.get():
    # if so, find the regions of interest
    find_rois()

#check if anly is one
if anly.get():
    # if so, analyze the images
    analysis()

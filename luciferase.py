#!/usr/bin/python3

import glob
import math
import os
import platform
from pathlib import Path
import tkinter as tk
from tkinter import filedialog as fd
from matplotlib import pyplot
import numpy
import jnius_config as jconf
import ui

def prep_env():
    # set up the environment so that jnius can be successfully imported
    runsys = platform.system()
    if runsys == "Linux":
        os.environ["JAVA_HOME"] = "/usr/lib/jvm/default-java"
    elif runsys == "Windows":
        os.environ["JAVA_HOME"] = r"C:\Program Files\Java\jdk-13.0.1"
        os.environ["PATH"] += r"C:\Program Files\Java\jdk-13.0.1\bin;"
        os.environ["PATH"] += r"C:\Program Files\Java\jdk-13.0.1\bin\server;"
        os.environ["PATH"] += r"C:\Program Files\Java\jdk-13.0.1\lib;"
    else:
        raise Exception("{runsys} is unsupported by the pipeline")


def locate_jars() -> list:
    # find the jar files associated with ImageJ
    home = Path("~").expanduser()
    ijfolder = next(home.glob("**/Fiji.app"))
    alljars = [str(p) for p in ijfolder.glob("**/*.jar")]
    return alljars


prep_env()
jconf.add_classpath(*locate_jars())

# makes the java bridge
import jnius

# creates the ImageJ application so that its operations succeed
ImageJ = jnius.autoclass('net.imagej.ImageJ')
imagej = ImageJ()

# gives access to the ImageJ classes needed for the pipeline
IJ = jnius.autoclass('ij.IJ')
ImagePlus = jnius.autoclass('ij.ImagePlus')
FolderOpener = jnius.autoclass('ij.plugin.FolderOpener')
# ImageJ classes only understand java strings
# thus, the input strings have to converted to java strings
# in order to give desired output
String = jnius.autoclass('java.lang.String')
SIFT_Align = jnius.autoclass('SIFT_Align')
Macro = jnius.autoclass('ij.Macro')
WindowManager = jnius.autoclass('ij.WindowManager')
ImageCalculator = jnius.autoclass('ij.plugin.ImageCalculator')
Roi = jnius.autoclass('ij.gui.Roi')
PolygonRoi = jnius.autoclass('ij.gui.PolygonRoi')
RATSQuadtree = jnius.autoclass('RATSQuadtree')
RATS_ = jnius.autoclass("RATS_")
RoiManager = jnius.autoclass("ij.plugin.frame.RoiManager")

# adds a more convenient alias for WindowManager.
# WindowManager is a static class anyway (no instances)
# so this shouldn't cause any problems
WM = WindowManager

def close(image :ImagePlus):
    """Closes the input image. """
    image.changes = False
    image.close()


def ijrun(image :ImagePlus,arg1 :str,arg2 :str):
    """This function is used to run any command that
can be accomplished by IJ.run, but it automatically
converts python strings into java strings, saving some
typing."""
    IJ.run(image, String(arg1), String(arg2))

def open_stack(foldername :str) -> ImagePlus:
    """Opens a folder of images as a stack, and displays it.
Displaying images helps to ensure that operations on them are
successful due to design quirks of the ImageJ operations."""
    stack = FolderOpener.open(String(foldername))
    stack.show()
    return stack

def open_image(filename :str) -> ImagePlus:
    """Opens an image and displays it for the same reason"""
    image = ImagePlus(String(filename))
    image.show()
    return image

def enhance_contrast(image :ImagePlus, stack:bool=False):
    """Increases the contrast of an image.
The image is modified in place."""
    if stack:
        # because plants are measured in the stack, we want to
        # avoid distorting measurements
        ijrun(image,"Enhance Contrast...","saturated=0.3 process_all")
    else:
        # In the segmentation process, we only care about the locations
        # of plants, not their value, so equalizing to increase the
        # visiblity of weak plants is appropriate
        ijrun(image,"Enhance Contrast...","saturated=0.3 equalize")

def median(image :ImagePlus, stack:bool=False):
    """Runs a median filter on an image.
The image is modified in place."""
    if stack:
        ijrun(image,"Median...","radius=2 stack")
    else:
        ijrun(image,"Median...","radius=2")

def minimum(image :ImagePlus, stack:bool=False):
    """Runs a minimum filter on an image.
The image is modified in place."""
    if stack:
        ijrun(image,"Minimum...","radius=2 stack")
    else:
        ijrun(image,"Minimum...","radius=2")

def subtract_background(image :ImagePlus, stack:bool=False):
    """Subtracts the background from an image.
The image is modified in place."""
    if stack:
        ijrun(image,"Subtract Background...","rolling=50 stack")
    else:
        ijrun(image,"Subtract Background...","rolling=50")

def align(stack :ImagePlus) -> ImagePlus:
    """uses SIFT to register the image sequence together, correcting drift.
The image sequence is consumed and a new, aligned stack is produced."""
    sifter = SIFT_Align()
    arg=String("initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")

    # SIFT_Align has a bizarre property where it checks the macro argument,
    # so the macro argument has to be set to pre-empt the arguments dialog

    Macro.setOptions(arg)
    sifter.run(arg)

    # As far as I can tell, SIFT_Align puts its output as the new current image.
    # If there was a more robust way to do this, I would

    aligned = WM.getCurrentImage()

    close(stack)

    WM.getWindow(String("Log")).hide()

    aligned.show()

    return aligned
    
def improve(image :ImagePlus, stack:bool=False):
    """Does a set of operations in place on the image
that emphasize signal and reduce noise.
The image is modified in place."""
    enhance_contrast(image,stack)
    median(image,stack)
    subtract_background(image,stack)

def skeletonize(mask :ImagePlus):
    """reduces the image to a map of its structure.
Modifies the image in place.
requires an 8-bit mask.
"""
    ijrun(mask,"Skeletonize","")

def rat(image :ImagePlus) -> ImagePlus:
    """Runs the RATS plugin on the input image.
Consumes the input image and outputs the resulting image."""
    arg = String("noise=25 lambda=3 min=410")
    Macro.setOptions(arg)
    rat = RATS_()
    rat.setup(arg,image)
    proc = image.getProcessor()
    rat.run(proc)
    mask = WM.getCurrentImage()
    mask.show()
    close(image)
    return mask

def get_brights(image :ImagePlus) -> list:
    """ Get all of the bright points in the image.
    Does not modify or consume the input image. """

    points = []

    for x in range(image.width):

        for y in range(image.height):

            if image.getPixel(x,y)[0]:

                points.append((x,y))

    return points

def wand(image :ImagePlus, points :list) -> list:
    """Applies the wand tool to all of the points listed,
and adds unique entries to the output list.
Does not modify or consume the input image."""

    rois = []

    for x,y in points:

        IJ.doWand(image, x, y, 0, String("4-connected"))

        roi = image.getRoi()

        if not any(map(lambda r : r.equals(roi), rois)):

            rois.append(roi)

    return rois


def generate_rois(image :ImagePlus) -> list:
    """ Generate the rois from the image.
This function handles all steps except for opening.
Consumes input image."""
    improve(image)
    mask = rat(image)
    minimum(mask)
    skell = mask.duplicate()
    skell.show()
    skeletonize(skell)
    brights = get_brights(skell)
    close(skell)
    rois = wand(mask, brights)
    close(mask)

    return rois

def save_rois(rois :list, file :str):
    """ Saves all of the rois in the list to
the file represented by the filename. """
    rm = RoiManager(False)

    for roi in rois:

        rm.addRoi(roi)

    rm.runCommand(String("Save"), String(file))

    rm.close()


def measure_rois(stack :ImagePlus, rois :list) -> dict:
    """Measure each roi for each position in the stack,
putting that information into a dictionary where the rois
are the keys and the values are lists of the measurements,
in particular the mean value of the roi at that slice position.
Does not consume or modify input image."""

    measurements = {}

    for region in rois:

        measurements[region] = []
    
    for i in range(stack.stackSize):

        # stack slices are 1-indexed
        stack.setSlice(i + 1)

        for region in rois:

            stack.setRoi(region)

            mean = stack.roi.statistics.mean

            measurements[region].append(mean)

    stack.setSlice(1) # reset the stack position for anyone measuring afterward

    return measurements

def open_archive(file :str) -> list:
    """Opens an archive of rois as a list of rois."""

    rm = RoiManager(False)

    rm.runCommand(String("Open"),String(file))

    rois = rm.roisAsArray

    rm.close()

    return rois

def contains(outer :Roi, inner :Roi) -> bool:
    "Check if the outer roi contains the inner roi."

    polygon = inner.getPolygon()

    return all(map(outer.contains, polygon.xpoints, polygon.ypoints))

def affiliate(groups :list, rois :list) -> dict:
    """ Create a dictionary that collects all rois belonging
    to a key that corresponds to a group's position in the input list."""
    areas = {}

    for roi in rois:

        unused = True

        for i,group in enumerate(groups):

            if contains(group, roi):

                areas.setdefault(i, []).append(roi)
                unused = False
                break

        if unused:

            # Rois not affiliated with any group go into the list
            # affilated with the key of -1
            areas.setdefault(-1, []).append(roi)

    return areas

def normalize(roi :list):
    """Normalizes the measurements of an roi by dividing all measurements
by the greaterst measurement (max value). Modifies the list in place."""
    greatest = max(roi)

    for i,item in enumerate(roi):

        roi[i] = item / greatest
            
def measure_background(stack:ImagePlus,x:int,y:int,width:int,height :int)->list:
    """ Measures the background region as defined by the inputs.
Does not modify or consume the input image."""

    stack.setRoi(x, y, width, height)

    values = []

    for i in range(stack.stackSize):

        stack.setSlice(i + 1)

        roi = stack.getRoi()

        values.append(roi.statistics.mean)

    stack.setSlice(1) # got to reset the stack's position
    
    return values


def set_xticks(timepoint_count, h_interval):
    IBT = 10 # stands for Images Between Ticks: the # of images between each tick on the x axis
    pyplot.xticks(ticks=numpy.arange(0,timepoint_count + 1, IBT),labels=numpy.arange(0,timepoint_count * h_interval + h_interval,h_interval * IBT))

def get_params() -> ui.Parameters:
    base = tk.Tk()
    params = ui.Parameters()
    interface = ui.UserInterface(base, params)
    interface.pack()
    base.mainloop()
    parameters = interface.parameters()
    parameters.saveas("last_params.json")
    return parameters

def get_rois(params :ui.Parameters) -> list:
    if params.use_existing_rois.get():
        rname = params.existing_rois.get()
        rois = open_archive(rname)
    else:
        maskname = params.mask.get()
        mask = open_image(maskname)
        rois = generate_rois(mask)
        if params.save_generated_rois.get():
            saveto = params.rois_savename.get()
            save_rois(rois, saveto)
    return rois

def get_stack(params :ui.Parameters) -> ImagePlus:
    stack = open_stack(params.folder.get())
    improve(stack, True)
    if params.align.get():
        stack = align(stack)
    return stack

def get_background(stack :ImagePlus, params :ui.Parameters) -> list:
    "thin wrapper around measure_background with to decrease clutter"
    return measure_background(
        stack,
        int(params.bx.get()),
        int(params.by.get()),
        int(params.b_width.get()),
        int(params.b_height.get())
        )

def organize_info(groups, measurements):
    "organize the measurements by group and time"
    org = affiliate(groups, measurements.keys())
    data = {}
    for group in org:
        for roi in org[group]:
            data.setdefault(group, []).append(measurements[roi])
    for group in data:
        # you need the time axis in the right place
        data[group] = numpy.array(data[group]).T
    
    return data



def reset_folders():
    try:
        os.mkdir("graphs")
    except FileExistsError:
        pass
    try:
        os.mkdir("spreadsheets")
    except FileExistsError:
        pass
    existing = glob.glob("graphs/*") + glob.glob("spreadsheets/*")
    for file in existing:
        os.remove(file)

def get_hour_interval(params):
    return params.interval_hours.get() + (params.interval_minutes.get() / 60)

def save_all_sheets(data):
    "save all the information as csv files"
    groups = sorted(data.keys())
    for group in groups:
        array = data[group]
        numpy.savetxt(f"spreadsheets/group{group}.csv", array, delimiter=',')

def plot_summary(data,background,s_hour:int,s_min:int,xtick,normalize_data=False):
    "plot the graph that summarizes the entirety of the data set"
    if normalize_data:
        normalize(background)
        for group in data:
            pyplot.plot(data[group].mean(1) / data[group].max(),
                        label=f"group {group}")
        pyplot.title("Normalized gray values vs. Time")
        pyplot.ylabel("normalized average plant gray value")
    else:
        for group in data:
            pyplot.plot(data[group].mean(1),
                        label=f"group {group}")
        pyplot.title("Gray values vs Time")
        pyplot.ylabel("Average plant gray value")
    xtick()
    pyplot.plot(background, label="background", color="black")
    pyplot.xlabel(f"Time elapsed since start time of {s_hour}:{s_min} in hours")
    pyplot.legend()
    pyplot.savefig("graphs/summary.png")
    pyplot.show()

def plot_groups(data, normalize,start_hour,start_minute,xtick):
    "plot the graph of each group in the data set"
    for group in sorted(data):
        if normalize:
            pyplot.plot(data[group] / data[group].max())
            xtick()
            pyplot.title(f"Group {group}" if group!=-1 else "Unclassified")
            pyplot.ylabel("Normalized plant gray value")
            pyplot.xlabel(f"Time elapsed since start time of {start_hour}:{start_minute}")
        else:
            pyplot.plot(data[group])
            xtick()
            pyplot.title(f"Group {group}" if group!=-1 else "Unclassified")
            pyplot.ylabel("Plant gray value")
            pyplot.xlabel(f"Time elapsed since start time of {start_hour}:{start_minute}")
        pyplot.savefig(f"graphs/group{group}.png")
        pyplot.show()


def main():
    "run the program"
    params = get_params()
    reset_folders()
    groups = open_archive(params.groups.get())
    stack = get_stack(params)
    rois = get_rois(params)
    background = get_background(stack, params)
    measurements = measure_rois(stack, rois)
    close(stack)
    data = organize_info(groups, measurements)
    save_all_sheets(data)
    hour_interval = get_hour_interval(params)
    xpoints = len(data[0])
    xticks = lambda:set_xticks(xpoints, hour_interval)
    plot_summary(data,
                 background,params.start_hour.get(),
                 params.start_minute.get(),
                 xticks,
                 params.normalize.get()
                 )
    plot_groups(data,
                params.normalize.get(),
                params.start_hour.get(),
                params.start_minute.get(),
                xticks
                )
    return data


if __name__ == '__main__':
    data = main()
    

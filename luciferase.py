#!/usr/bin/python3

import glob
import math
import os
import tkinter as tk
from tkinter import filedialog as fd
from matplotlib import pyplot
import numpy
import jnius_config as jconf
import ui

# setup environment for the java bridge
os.environ['JAVA_HOME'] = "/usr/lib/jvm/default-java"
jconf.add_classpath(*glob.glob("/home/tomas/Fiji.app/**/*.jar",recursive=True))

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
        # because plants are identified in the s
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

    stack.setRoi(x,y,width,height)

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

def main():

    base = tk.Tk()

    interface = ui.UserInterface(base)

    interface.pack()

    base.mainloop()

    interface.save("parameters.txt")

    stack = open_stack(interface.image_folder)

    timepoint_count = stack.stackSize

    img = open_image(interface.mask)

    groups = open_archive(interface.roi_settings['groups'])

    if interface.roi_settings['use existing']:

        rois = open_archive(interface.roi_settings['existing'])

        close(img)

    else:

        rois = generate_rois(img)

    if interface.roi_settings['save rois']:

        save_rois(rois, interface.roi_settings['roi save file'])

    del img

    improve(stack, True)

    if interface.align:

        stack = align(stack)

        WM.getWindow(String("Log")).hide()

    measurements = measure_rois(stack, rois)

    background = measure_background(stack, *interface.background_bounds)

    close(stack)

    del stack

    if interface.normalize:

        for roi in measurements:

            normalize(measurements[roi])

        normalize(background)

    groupings = affiliate(groups, measurements.keys())

    data = {}

    for group in groupings:

        for roi in groupings[group]:

            data.setdefault(group, []).append(measurements[roi])

    try:

        os.mkdir("output")

    except FileExistsError:

        pass

    try:

        os.mkdir("graphs")

    except FileExistsError:

        pass

    ofiles = glob.glob("output/*")
    gfiles = glob.glob("graphs/*")

    if len(ofiles) > 0:

        for of in ofiles:
            os.remove(of)

    if len(gfiles) > 0:
            
        for gf in gfiles:
            os.remove(gf)
    
    for group in data:

        # causes the data to be organized in an easily graphable way
        data[group] = numpy.array(data[group]).T

        numpy.savetxt("output/group{}.csv".format(group), data[group], delimiter=',')

        lbl = "Unclassified" if group == -1 else "Group {}".format(group)

        pyplot.plot(data[group].mean(1), label=lbl)

    pyplot.plot(background, label="Background", color="black")

    pyplot.legend()

    title = "Normalized Intensity" if interface.normalize else "Intensity"

    pyplot.title(title)

    h_interval = interface.interval[0] + (interface.interval[1] / 60)

    set_xticks(timepoint_count, h_interval)

    pyplot.xlabel("Hours after {}:{} {}".format(*interface.start_time))

    pyplot.ylabel("Normalized Intensity" if interface.normalize else "Intensity")

    pyplot.savefig("graphs/summary.png")

    pyplot.show()

    for group in sorted(data.keys()):

        pyplot.plot(data[group])

        set_xticks(timepoint_count, h_interval)

        pyplot.title("Group {}".format(group) if group >= 0 else "Unclassified")

        pyplot.xlabel("Time or Slice Position")

        pyplot.ylabel("Normalized Intensity" if interface.normalize else "Intensity")

        pyplot.savefig("graphs/group{}.png".format(group) if group >= 0 else "graphs/unclassified.png")

        pyplot.show()

if __name__ == '__main__':

    main()

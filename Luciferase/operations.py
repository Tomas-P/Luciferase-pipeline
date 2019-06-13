#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 13:41:43 2019

@author: tomas
"""

from IJ_setup import ImageJ,IJ,ImagePlus,FolderOpener,String,SIFT_Align,Macro,WindowManager,\
ImageCalculator,Roi,PolygonRoi,RATSQuadtree,RATS_,RoiManager, imagej

set_current = WindowManager.setTempCurrentImage
get_current = WindowManager.getCurrentImage

def ijrun(image, arg1, arg2):
    IJ.run(image, String(arg1), String(arg2))

def close(image :ImagePlus):
    image.changes = False
    image.close()

def open_mask(maskname:str) -> ImagePlus:
    """ Create a mask based on the image refered to by the filename """
    image = ImagePlus(String(maskname))
    
    set_current(image)
    
    ijrun(image, "Enhance Contrast...", "saturated=0.3 equalize")
    ijrun(image, "Median...", "radius=2")
    ijrun(image, "Subtract Background...", "rolling=50")
    
    arg = String("noise=25 lambda=3 min=410")
    Macro.setOptions(arg)
    
    rat = RATS_()
    rat.setup(arg, image)
    
    proc = image.getProcessor()
    
    rat.run(proc)
    
    mask = get_current()
    
    set_current(mask)
    
    ijrun(mask, "Minimum...", "radius=2")
    
    close(image)
    
    return mask

def open_stack(foldername :str) -> ImagePlus:
    """ Open all images in the named folder as a stack"""
    stack = FolderOpener.open(String(foldername))
    set_current(stack)
    return stack

def align(stack :ImagePlus) -> ImagePlus:
    set_current(stack)
    sift = SIFT_Align()
    Macro.setOptions(
        String("initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")
        )
    sift.run(
        String("initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")
        )
    aligned = get_current()
    
    set_current(aligned)
    
    close(stack)
    
    return aligned

def apply_mask(stack :ImagePlus, mask :ImagePlus) -> ImagePlus:
    ic = ImageCalculator()
    applied = ic.run(
            String("AND create stack"),
            stack,
            mask
            )
    set_current(applied)
    return applied

def process(stack :ImagePlus, mask :ImagePlus) -> ImagePlus:
    """ Conduct all of the processing required to prepare the images for data extraction"""
    
    set_current(stack)
    ijrun(stack, "Enhance Contrast...", 'saturated=0.3 equalize process_all')
    ijrun(stack, 'Median...', 'radius=2 stack')
    ijrun(stack, "Subtract Background...", "rolling=50 stack")
    stack = align(stack)
    log = WindowManager.getWindow(String("Log"))
    log.hide()
    stack.show()
    mask.show()
    filt = apply_mask(stack, mask)
    close(stack)
    close(mask)
    
    return filt

def skeletonize(image :ImagePlus):
    ijrun(image, "Skeletonize", "")

def get_brights(mask :ImagePlus) -> list:
    "Locates all bright pixels"
    pixels = []
    for x in range(mask.width):
        for y in range(mask.height):
            if mask.getPixel(x,y)[0]:
                pixels.append((x,y))

    return pixels

def wand_all(image, points):
    "gets all non-duplicate results of applying the wand tool to each point for the image"
    rois = []
    for x,y in points:
        IJ.doWand(image, x, y, 0, "4-connected")
        r = image.getRoi()
        if not any(map(lambda roi : roi.equals(r), rois)):
            rois.append(r)
    return rois

def generate_rois(maskname:str) -> list:
    " Generate rois from an image file "
    mask = open_mask(maskname)
    m2 = mask.duplicate()
    set_current(m2)
    skeletonize(m2)
    brights = get_brights(m2)
    close(m2)
    rois = wand_all(mask, brights)
    close(mask)
    
    return rois

def open_archive(filename:str) -> list:
    "open a group or roi archive"
    rm = RoiManager(False)
    rm.runCommand(String("Open"),String(filename))
    rois = rm.getRoisAsArray()
    rm.close()
    return rois


def contains(outer, inner) -> bool:
    "checks if the `outer` ROI contains the `inner` ROI"
    polygon = inner.getPolygon()
    return all(map(outer.contains, polygon.xpoints, polygon.ypoints))


def affiliate(groups :list, rois :list) -> dict:
    '''Creates a dictionary that puts all rois belonging to a group
    in a list as the value associated with a key that corresponds to
    a group's position in the input list'''
    areas = {}
    for roi in rois:
        unused = True
        for i,group in enumerate(groups):
            if contains(group, roi):
                areas.setdefault(i, []).append(roi)
                unused = False
                break
        if unused:
            # ROIs not affiliated with any group go into the list
            # affilated with the key of -1.
            areas.setdefault(-1, []).append(roi)
    return areas

def measure_background(seq :ImagePlus,bx,by,bwidth,bheight) -> list:
    "Measure the intensity of the background region of the sequence"
    set_current(seq)
    seq.setRoi(bx,by,bwidth,bheight)
    bg = []

    for t in range(seq.getStackSize()):
        seq.setSlice(t + 1)
        bg.append(seq.getStatistics().mean)

    return bg

def measure_data(data :ImagePlus, grouped_rois :dict) -> dict:
    """ measures the data from the image sequence.
    outputs a dictionary of experimental groups to a dictionary of
    time points to a list of adjusted intensities for the rois in that group
    at that time """

    # the outer layer is a dict, where the keys are the experimenal group.
    # and the values are dicts where the keys are points in time,
    # and the values are lists of mean non-zero value for each roi in
    # the relevant time point and experimental group

    measurements = {}

    for t in range(data.getStackSize()):
        data.setSlice(t + 1)

        for j, area in grouped_rois.items():
            for roi in area:
                data.setRoi(roi)
                stats = roi.statistics
                val = stats.mean * stats.area * stats.areaFraction / 100
                measurements.setdefault(j, {}).setdefault(t, []).append(val)

    return measurements

def save_rois(rois :list, archivename :str):
    "save an roi set to a file"
    rm = RoiManager(False)
    for r in rois:
        rm.addRoi(r)
    rm.runCommand(String("Save"),String(archivename))
    rm.close()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 11:55:42 2019

@author: tomas
"""

from ui import request_folder
import glob
import os
import jnius_config

ijfolder = request_folder("Please provide your ImageJ folder")
os.environ["JAVA_HOME"] = glob.glob(ijfolder + "/**/jdk*/", recursive=True)[0]
jnius_config.add_classpath(*glob.glob(ijfolder+"**/*.jar",recursive=True))

import jnius

ImageJ = jnius.autoclass("net.imagej.ImageJ")

# this line makes the visuals work -- and most operations
imagej = ImageJ()

# classes used in the pipeline
IJ = jnius.autoclass('ij.IJ')
ImagePlus = jnius.autoclass('ij.ImagePlus')
FolderOpener = jnius.autoclass('ij.plugin.FolderOpener')
String = jnius.autoclass('java.lang.String')
SIFT_Align = jnius.autoclass('SIFT_Align')
Macro = jnius.autoclass('ij.Macro')
WindowManager = jnius.autoclass('ij.WindowManager')
ImageCalculator = jnius.autoclass('ij.plugin.ImageCalculator')
Roi = jnius.autoclass('ij.gui.Roi')
PolygonRoi = jnius.autoclass('ij.gui.PolygonRoi')
RATSQuadtree = jnius.autoclass('RATSQuadtree')
RATS_ = jnius.autoclass("RATS_")
RoiManager = jnius.autoclass('ij.plugin.frame.RoiManager')
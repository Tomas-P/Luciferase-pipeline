from ij import IJ
from ij.plugin.frame import RoiManager
from ij.gui import OvalRoi
import glob
from xml.etree import ElementTree as et
import sys

def xmltree():
	script_file = sys.argv[0]
	folder = script_file[:script_file.rfind('/')]+'/'
	xfile = folder + 'info.xml'
	return et.parse(xfile)

rm = RoiManager()
IJ.run("Set Measurements...", "area_fraction redirect=None decimal=3")

xtree = xmltree()

image = IJ.openImage(sorted(glob.glob(xtree.findtext('images') + '*'))[0])
IJ.run(image,"Enhance Contrast...","saturated=0.3 equalize")
IJ.run(image,"Median...","radius=2")
IJ.run(image,"Subtract Background...", "rolling=50")

IJ.run(image, "Robust Automatic Threshold Selection", "noise=25 lambda=3 min=410")
image = IJ.getImage()

size = int(xtree.findtext('roi_size'))
minimum = float(xtree.findtext('roi_min_percent_area'))

for x in range(0,image.getWidth(),size):
	for y in range(0,image.getHeight(),size):
		roi = OvalRoi(x,y,size,size)
		image.setRoi(roi)
		if image.getRoi().getStatistics().areaFraction > minimum:
			rm.addRoi(roi)

rm.runCommand("Save",xtree.findtext("ROI_archive"))
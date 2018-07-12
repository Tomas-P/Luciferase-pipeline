import sys
from ij import ImagePlus,IJ
from ij.plugin.frame import RoiManager

def folder():
	script = sys.argv[0]
	return script[:script.rfind('/')]

def open_stack():
	filename = folder() + "/stack.tif"
	return ImagePlus(filename)

def open_roi_archive():
	rm = RoiManager()
	filename = folder() + "/RoiSet.zip"
	rm.runCommand("Open", filename)
	return rm

def measure():
	stack = open_stack()
	rm = open_roi_archive()
	IJ.run("Set Measurements...", "area mean area_fraction stack redirect=None decimal=3")
	for i in range(stack.getImageStackSize()):
		rm.runCommand(stack,"Measure")
		IJ.run(stack, "Next Slice [>]", "")
	IJ.saveAs("Results", folder() + "/measurements.csv")

if sys.argv[0].endswith("measure.py"):
	measure()
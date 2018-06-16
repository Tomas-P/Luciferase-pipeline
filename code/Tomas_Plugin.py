from ij import IJ
from ij.plugin.frame import RoiManager
from ij.plugin import ImageCalculator
from xml.etree import ElementTree as et
import glob
import sys

def make_mask(image):
	IJ.run(image, "Robust Automatic Threshold Selection", 
	"noise=25 lambda=3 min=410")
	mask = IJ.getImage()
	IJ.run(mask, "16-bit", "")
	IJ.run(mask, "Multiply...", "value=257") # 255 * 257 == 65535 == 2**16-1
	return mask


def open_sequence(xml_tree):
	foldername = xml_tree.findtext("images")
	filename = sorted(glob.glob(foldername+'*'))[0]
	IJ.run("Image Sequence...","open={} sort".format(filename))
	stack = IJ.getImage()
	IJ.run(stack, "Enhance Contrast...", 
	"saturated=0.3 equalize process_all")
	IJ.run(stack, "Median...", "radius=2 stack")
	return stack
	
def xmltree():
	script_file = sys.argv[0]
	folder = script_file[:script_file.rfind('/')]+'/'
	xfile = folder + 'info.xml'
	return et.parse(xfile)

def apply_mask(im_calc,stack, mask):
	image = im_calc.run("AND create stack", stack, mask)
	return image

def set_measurements():
	IJ.run("Set Measurements...",
	"area mean area_fraction stack redirect=None decimal=3")

def measure(roi_manager, stack):
	for i in range(stack.getImageStackSize()):
		roi_manager.runCommand(stack,"Measure")
		IJ.run(stack, "Next Slice [>]", "")

def save_results(filename):
	IJ.saveAs("Results", filename)

def open_rois(tree):
	roi_set = tree.findtext("ROI_archive")
	rm = RoiManager()
	rm.runCommand("Open", roi_set)
	return rm

def main():
	xtree = xmltree()
	calc = ImageCalculator()
	stack = open_sequence(xtree)
	mask = make_mask(stack)
	mask.show()
	filtered = apply_mask(calc,stack, mask)
	filtered.show()
	roi_manager = open_rois(xtree)
	measure(roi_manager, filtered)
	save_results(xtree.findtext("csv"))
	print("Complete")

main()

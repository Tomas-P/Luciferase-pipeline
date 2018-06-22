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
	IJ.run(stack, "Subtract Background...", "rolling=50 stack")
	return stack

def SIFT_register(stack):
	IJ.run(stack, "Linear Stack Alignment with SIFT", "initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")
	return IJ.getImage()

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

def get_background_comparison(stack, tree):
	# The background mean is the only important thing
	IJ.run("Set Measurements...", "mean stack redirect=None decimal=3")
	# read in the selection info from the xml tree
	bx,by,width, height = eval(tree.findtext("bg"))
	# create a rectangular selection
	stack.setRoi(bx,by,width,height)
	# measure the selection in each slice
	for i in range(stack.getImageStackSize()):
		IJ.run(stack, "Measure", "")
		IJ.run(stack, "Next Slice [>]", "")
	# save the results
	IJ.saveAs("Results", tree.findtext("bgcsv"))
	# clean up for the actual program
	IJ.run("Clear Results", "")
	
def main():
	xtree = xmltree()
	calc = ImageCalculator()
	proto_stack = open_sequence(xtree)
	stack = SIFT_register(proto_stack)
	get_background_comparison(stack, xtree)
	mask = make_mask(stack)
	mask.show()
	filtered = apply_mask(calc,stack, mask)
	filtered.show()
	set_measurements()
	roi_manager = open_rois(xtree)
	measure(roi_manager, filtered)
	save_results(xtree.findtext("csv"))
	roi_manager.close()

main()
IJ.run("Close All", "")
IJ.selectWindow("Results")
IJ.run("Close")
IJ.selectWindow("Log")
IJ.run("Close")
IJ.run("Quit")

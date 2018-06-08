import sys
from xml.etree import ElementTree as et
import glob
from ij import IJ
from ij.plugin.frame import RoiManager

#Take a folder name and open all images in that folder as a stack
def folder_to_stack(foldername):
	file1 = sorted(map(lambda x : x.replace('\\','/'), glob.glob(foldername + '/*')))[0]
	IJ.run("Image Sequence...",
	"open={} sort".format(file1)
	)
	return IJ.getImage()

# Take an image stack and run SIFT on it
def register(stack):
	IJ.run(stack,"Linear Stack Alignment with SIFT","initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size64 maximum_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")
	return IJ.getImage()

#Run the median filter on a stack
def median(stack):
	IJ.run(stack,"Median...", "radius=2 stack")
	return IJ.getImage()

#Open the zip file with the selections
def get_rois(roi_archive):
	rm = RoiManager();
	success = rm.runCommand("Open",roi_archive)
	return rm #return the RoiManager for later use

#Do your measurements for each image in the stack
def measure_stack(stack,images_in_stack,roi_manager):
	IJ.run("Set Measurements...", "mean median stack redirect=None decimal=3")
	for i in range(images_in_stack):
		roi_manager.runCommand(stack,"Measure")
		IJ.run(stack, "Next Slice [>]", "")

# Save the measurements in a csv file
def save_results(result_filename):
	IJ.saveAs("Results", result_filename)
	return None

def main():
	name = sys.argv[0]
	folder = name[:name.rfind('/')]
	print(folder)
	tree = et.parse(folder + '/info.xml')
	out = tree.findtext('csv')
	image_foldername = tree.findtext('images')
	roi_archive = tree.findtext('ROI_archive')
	print(out,image_foldername,roi_archive)
	
	stack = folder_to_stack(image_foldername)
	stack = register(stack)
	stack = median(stack)
	rm = get_rois(roi_archive)
	measure_stack(stack,stack.getImageStackSize(),rm)
	save_results(out)
	print("Done")

main()

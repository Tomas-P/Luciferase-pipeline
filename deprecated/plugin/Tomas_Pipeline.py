import glob
import os
from ij import IJ
from ij.plugin.frame import RoiManager

#Have the user choose a folder
def choose_folder():
	return IJ.getDir("Which folder of images should I operate on?")

#Check if a folder already exists
def folder_exists(foldername):
	return os.path.isdir(foldername)

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

#Get the archive file from the user
def get_zip():
	zip_file = IJ.getFilePath("Select the ROI archive")
	return zip_file

#Do your measurements for each image in the stack
def measure_stack(stack,images_in_stack,roi_manager):
	IJ.run("Set Measurements...", "mean median stack redirect=None decimal=3")
	for i in range(images_in_stack):
		roi_manager.runCommand(stack,"Measure")
		IJ.run(stack, "Next Slice [>]", "")

#Ask the user for a folder to save measurements in
def get_measurement_folder():
	return IJ.getDir("Select the folder you want the stack measurements stored in")

# Save the measurements in a csv file
def save_results(result_folder):
	result_name = result_folder + "Tomas_Pipeline_Measurements.csv"
	IJ.saveAs("Results", result_name)
	return None

f = choose_folder()
zfile = get_zip()
m_folder = get_measurement_folder()
s = folder_to_stack(f)
s = register(s)
s = median(s)
rm = get_rois(zfile)
measure_stack(s,s.getImageStackSize(),rm)
save_results(m_folder)

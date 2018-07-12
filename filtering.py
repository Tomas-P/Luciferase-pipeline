import sys

# make sure context is correct
assert sys.version.startswith("2.7.1")

from ij import IJ
from ij.plugin.frame import RoiManager
from ij.plugin import ImageCalculator
import json
import glob

def get_options():
	script = sys.argv[0]
	folder = script[:script.rfind("/")] + "/"
	optfilename = folder + "options.json"
	optfile = open(optfilename)
	options = json.load(optfile)
	optfile.close()
	return options

def open_sequence(options):
	folder = str(options[u"images"])
	filename = sorted(glob.glob(folder + "/*"))[0]
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

def make_mask(image):
	IJ.run(image, "Robust Automatic Threshold Selection", 
	"noise=25 lambda=3 min=410")
	mask = IJ.getImage()
	IJ.run(mask, "16-bit", "")
	IJ.run(mask, "Multiply...", "value=257") # 255 * 257 == 65535 == 2**16-1
	IJ.run(mask, "Median...", "radius=2") # remove some of the noise
	return mask

def apply_mask(im_calc,stack, mask):
	image = im_calc.run("AND create stack", stack, mask)
	return image
	
def main():
	script = sys.argv[0]
	folder = script[:script.rfind("/")] + "/"
	ic = ImageCalculator()
	options = get_options()
	seq = open_sequence(options)
	seq.show()
	aligned = SIFT_register(seq)
	aligned.show()
	mask = make_mask(seq)
	mask.show()
	stack = apply_mask(ic, aligned, mask)
	stack.show()
	IJ.save(stack, folder + "stack.tif")
	return stack


if sys.argv[0].endswith("filtering.py"):
	stack = main()
	stack.show()


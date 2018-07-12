from ij import IJ
from ij.gui import PointRoi
from ij.gui import Roi
from ij.plugin.frame import RoiManager
from math import sqrt
import json
import sys
import glob

def getinputs():
	here = sys.argv[0]
	folder = here[:here.rfind('/')]
	folder = folder[:folder.rfind('/')] + '/'
	try:
		optfile = open(folder + 'options.json')
	except:
		here = sys.argv[0]
		folder = here[:here.rfind('/')]+'/'
		optfile = open(folder + "options.json")
	options = json.load(optfile)
	optfile.close()
	return (sorted(glob.glob(str(options[u'images']) + '/*'))[0], int(options[u"rwidth"]), int(options[u"rheight"]))

def getmask(filename):
	image = IJ.openImage(filename)
	image.show()
	IJ.run(image, "Enhance Contrast...", "saturated=0.3 equalize")
	IJ.run(image, "Subtract Background...", "rolling=50")
	IJ.run(image, "Median...", "radius=2")
	IJ.run(image, "Robust Automatic Threshold Selection", "noise=25 lambda=3 min=410")
	mask = IJ.getImage()
	return mask

def distance(pixel1, pixel2):
	xpart = (pixel1[0] - pixel2[0])**2
	ypart = (pixel1[1] - pixel2[1])**2
	return sqrt(xpart + ypart)

def get_region_pixels(image, width, height, startx, starty):
	pixels = []
	for x in range(startx, startx + width):
		for y in range(starty, starty + height):
			if image.getPixel(x,y)[0]:
				pixels.append((x,y,image.getPixel(x,y)[0]))

	return pixels


def make_roi(pixels):
	xlist = []
	ylist = []
	pcount = len(pixels)
	for x,y,val in pixels:
		xlist.append(x)
		ylist.append(y)

	roi = PointRoi(xlist, ylist, pcount)
	return roi

def get_manager_with_rois():
	filename, rwidth, rheight = getinputs()
	mask = getmask(filename)
	mask.show()
	rm = RoiManager()
	area = rwidth * rheight
	
	for y in range(0,mask.getHeight(),rheight):
		for x in range(0,mask.getWidth(),rwidth):
			region_pixels = get_region_pixels(mask,rwidth,rheight,x,y)
			if len(region_pixels) < area * 0.80:
				continue # skip small ones
				
			roi = make_roi(region_pixels)
			mask.setRoi(roi)

			stats = roi.getStatistics()
			rm.addRoi(roi)
	return rm, mask

def main():
	manager, imageplus = get_manager_with_rois()
	s = sys.argv[0]
	archive = s[:s.rfind('/')] + "/RoiSet.zip"
	manager.runCommand("Save", archive)
	manager.runCommand(imageplus, "Show All with labels")
	return manager

if sys.argv[0].endswith("Other.py"):
	main()

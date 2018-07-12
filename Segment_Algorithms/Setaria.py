
from ij import IJ
from ij.gui import PolygonRoi
from ij.gui import Roi
from ij.plugin.frame import RoiManager
from math import sqrt
import sys
import json
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

def get_border_pixels(image, pixels):
	border_pixels = []
	getpixel = lambda x,y : image.getPixel(x,y)[0]

	for pixel in pixels:
		x = pixel[0]
		y = pixel[1]
		ncount = 0

		if getpixel(x + 1, y):
			ncount += 1
		if getpixel(x - 1, y):
			ncount += 1
		if getpixel(x, y + 1):
			ncount += 1
		if getpixel(x, y - 1):
			ncount += 1
		if getpixel(x + 1, y + 1):
			ncount += 1
		if getpixel(x - 1, y - 1):
			ncount += 1
		if getpixel(x - 1, y + 1):
			ncount += 1
		if getpixel(x + 1, y - 1):
			ncount += 1

		if ncount < 8:
			border_pixels.append(pixel)

	return border_pixels

def sort_pixels(pixels):
	sorted_pixels = [pixels[0]]

	while pixels:

		dist = 1000
		prev = sorted_pixels[-1]
		next = None
	
		for p in pixels:
			if distance(p, prev) < dist:
				next = p
				dist = distance(p, prev)

		sorted_pixels.append(next)
		pixels.remove(next)

	return sorted_pixels

def make_roi(sorted_pixels):
	xlist = []
	ylist = []
	pcount = len(sorted_pixels)
	for x,y,val in sorted_pixels:
		xlist.append(x)
		ylist.append(y)

	roi = PolygonRoi(xlist, ylist, pcount, PolygonRoi.POLYGON)
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
			if not region_pixels:
				continue # skip empty ones
			border_pixels = get_border_pixels(mask,region_pixels)
			if not border_pixels:
				# we know this region is not empty
				# we also know this region has no 
				# boundaries.
				# Therefore, all of this region is an Roi
				
				# add the area to the roi manager
				r = Roi(x,y,rwidth,rheight)
				mask.setRoi(r)
				if r.getStatistics().areaFraction == 100:
					rm.addRoi(r)
					
				# proceed normally with the rest of the image
				continue
			sorted_pixels = sort_pixels(border_pixels)
			roi = make_roi(sorted_pixels)
			mask.setRoi(roi)

			stats = roi.getStatistics()
			if stats.areaFraction > 90 and stats.area > 1.0/16.0 * area:
				rm.addRoi(roi)
	return rm, mask

def main():
	manager, imageplus = get_manager_with_rois()
	s = sys.argv[0]
	archive = s[:s.rfind('/')] + "/RoiSet.zip"
	manager.runCommand("Save", archive)
	manager.runCommand(imageplus, "Show All with labels")
	return manager

if sys.argv[0].endswith("Setaria.py"):
	main()

#IJ.run("Quit") # only needed if made part of pipeline

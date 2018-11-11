from __future__ import division
import sys
script = sys.argv[0]
folder = script[:script.rfind('/')]
sys.path.append(folder)
from __init__ import getinputs, getmask
from Setaria import sort_pixels
from ij import ImagePlus,IJ
from ij.plugin import ContrastEnhancer
from ij.plugin.filter import BackgroundSubtracter
from ij.plugin.filter import RankFilters
from ij.gui import PolygonRoi
from ij.plugin.frame import RoiManager


class Point(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __truediv__(self,scalar):
		return Point(self.x / scalar, self.y / scalar)

	def __floordiv__(self,scalar):
		return Point(self.x // scalar, self.y // scalar)

	def __str__(self):
		return "({0},{1})".format(self.x,self.y)

	def __eq__(self,other):
		return self.x == other.x and self.y == other.y

	def int_coords(self):
		self.x = int(self.x)
		self.y = int(self.y)

	def access(self,image_plus):
		return image_plus.getPixel(self.x,self.y)[0]

	def left(self):
		return Point(self.x - 1, self.y)

	def right(self):
		return Point(self.x + 1, self.y)

	def up(self):
		return Point(self.x, self.y - 1)

	def down(self):
		return Point(self.x, self.y + 1)


def open_image(filename):
	image = ImagePlus(filename)
	ce = ContrastEnhancer()
	bsub = BackgroundSubtracter()
	rf = RankFilters()
	ce.equalize(image)
	ip = image.getProcessor()
	bsub.rollingBallBackground(ip, 50.0, False, False, False, False, False)
	image.setProcessor(ip)
	rf.rank(ip,2.0,rf.MEDIAN)
	image.setProcessor(ip)
	return image

def make_mask(image):
	IJ.run(image, "Robust Automatic Threshold Selection", "noise=25 lambda=3 min=410")
	return IJ.getImage()

def process_region(image, bx, by, width, height):
	
	left,right = bx, bx + width
	top,bottom = by, by + height # top left origin, don't question it
	points = [Point(x,y) for x in range(left,right) for y in range(top,bottom)]
	points = filter(lambda p : p.access(image) > 0, points)
	for p in points:
		isborder1 = p.left().x==left or p.right().x==right or p.up().y==top or p.down().y==bottom
		isborder2 = p.left().access(image)==0 or p.right().access(image)==0 or p.up().access(image)==0 or p.down().access(image)==0
		if not (isborder1 or isborder2):
			points.remove(p)
	
	if len(points) == 0:
		return None
	
	def to_s_point(point):
		return (point.x,point.y)
	def from_s_point(s_point):
		return Point(s_point[0],s_point[1])

	points = map(to_s_point,points)
	points = sort_pixels(points)
	points = map(from_s_point,points)
	xlist = map(lambda p : p.x, points)
	ylist = map(lambda p : p.y, points)
	pcount = len(xlist)
	type_ = PolygonRoi.POLYGON
	return PolygonRoi(xlist,ylist,pcount,type_)
	
	
def create_selections():
	filename,width,height = getinputs()
	mask = getmask(filename)
	rm = RoiManager()
	for x in range(0,mask.getWidth(),width):
		for y in range(0,mask.getHeight(),height):
		
			r = process_region(mask, x, y, width, height)
			if r:
				mask.setRoi(r)
				stats = r.getStatistics()
				if stats.area < 0.25 * width * height or stats.mean < 20:
					continue
				rm.addRoi(r)	
	return rm

def main():
	roi_m = create_selections()
	archive = folder + "/artifacts/RoiSet.zip"
	roi_m.runCommand("Save",archive)
	return roi_m

if sys.argv[0].endswith("Arabadopsis.py"):
	main()

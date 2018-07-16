import sys
import json
from ij import IJ, ImagePlus

def folder():
    script = sys.argv[0]
    return script[:script.rfind('/')]

def getoptions():
    filename = folder() + "/options.json"
    fhandle = open(filename)
    opts = json.load(fhandle)
    fhandle.close()
    return opts


def get_bg_bounds(options):
    bounds = options[u"background"]
    bx = bounds[u"bx"]
    by = bounds[u"by"]
    width = bounds[u"width"]
    height = bounds[u"height"]
    return (bx,by,width,height)

def getimage():
    filename = folder() + "/stack.tif"
    return ImagePlus(filename)

def measure(image, bounds):
    image.setRoi(*bounds)
    IJ.run("Set Measurements...", "mean stack redirect=None decimal=3");
    for i in range(image.getImageStackSize()):
        IJ.run(image,"Measure","")
        IJ.run(image,"Next Slice [>]", "")

def main():
    opts = getoptions()
    bounds = get_bg_bounds(opts)
    image = getimage()
    measure(image,bounds)
    IJ.saveAs("Results",folder() + "/background.csv")

if sys.argv[0].endswith("background.py"):
    main()
    print("Background measurements complete and saved")
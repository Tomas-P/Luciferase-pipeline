
from ij import IJ
import sys
import json
import glob

def getinputs():
    here = sys.argv[0]
    folder = here[:here.rfind('/')]
    folder = folder[:folder.rfind('/')] + '/'
    try:
        optfile = open(folder + 'config/options.json')
    except:
        here = sys.argv[0]
        folder = here[:here.rfind('/')]+'/'
        optfile = open(folder + "config/options.json")
        
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
    image.changes = False
    image.close()
    mask = IJ.getImage()
    IJ.run(mask, "Dilate", "")
    return mask

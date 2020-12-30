
from pathlib import Path
import numpy
from matplotlib import pyplot
from parameter import Param
from ui import ask_user
import graph
from imagej import String,ImageJ,IJ,ImagePlus,FolderOpener,SIFT_Align,Macro,\
     WindowManager,WM,ImageCalculator,Roi,PolygonRoi,RatsQuadtree,RATS_,\
     RoiManager,close,ijrun,Our_imagej

def show(func):
    ''' makes returned images be shown, is a decorator.
    one of the wierder things about ImageJ1 APIs is that many
    require images to be displayed in order to function.
    why? who knows. but it has to be accounted for.
    '''
    def wrapped(*args, **kwargs):
        image = func(*args, **kwargs)
        image.show()
        return image
    return wrapped

@show
def openstack(foldername :str) -> ImagePlus:
    return FolderOpener.open(String(foldername))

@show
def openimage(filename :str) -> ImagePlus:
    return ImagePlus(String(filename))

def enhance_contrast(image :ImagePlus, stack=False):
    'increase image contrast in place'
    if stack:
        # enhance contrast one slice at a time so that non-modification
        # of data remains enforced (this command is weird)
        for i in range(1, image.getStackSize() + 1): # stacks start at one
            image.setSlice(i)
            ijrun(image, "Enhance Contrast...", "saturated=0.3")
        image.setSlice(1)
    else: # for segmenting, contrast > preservation of numerical values
        ijrun(image, "Enhance Contrast...", "saturated=0.3 equalize")

def median(image, stack=False):
    ijrun(image, "Median...", ("radius=2 stack" if stack else "radius=2"))

def minimum(image, stack=False):
    ijrun(image, "Minimum...", ("radius=2 stack" if stack else "radius=2"))

def subtract_background(image, stack=False):
    ijrun(image,
          "Subtract Background...",
          "rolling=50 stack" if stack else "rolling=50"
          )

# defaults have to be specified because their absence triggers dialog boxes
# dialog boxes = interaction = no automation
@show
def align(stack) -> ImagePlus:
    "creates new, aligned stack from input"
    sifter = SIFT_Align()
    arg = String(
        "initial_gaussian_blur=1.60 steps_per_scale_octave=3 \
minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 \
feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 \
maximal_alignment_error=25 inlier_ratio=0.05 \
expected_transformation=Rigid interpolate"
        )
    # SIFT_Align checks the macro arg, so it has to be set in order to
    # avoid an argument dialog
    Macro.setOptions(arg)
    sifter.run(arg) # do the work, requires the argument.
    # SIFT_Align puts its output as the new current image.
    aligned = WM.getCurrentImage() # Irritating, but usable.
    # don't need the log window, don't need it in the way to mess things up
    WM.getWindow(String("Log")).hide()
    return aligned

def skeletonize(mask :ImagePlus):
    'skeletonize ops make the image show the structure of what is depicted'
    ijrun(mask, "8-bit")
    ijrun(mask, "Skeletonize")

@show
def rats(image) -> ImagePlus:
    """RATS is a method for dividing images into high and low zones,
    which is useful for segmentation and itentifying plants in photographs."""
    arg = String("noise=25 lambda=3 min=410")
    Macro.setOptions(arg)
    # RATS_ has an odd way of working, but it does, so we permit it.
    rat = RATS_()
    rat.setup(arg,image)
    proc = image.getProcessor()
    rat.run(proc)
    mask = WM.getCurrentImage()
    return mask

@show
def create_mask(filename :str) -> ImagePlus:
    image = openimage(filename)
    enhance_contrast(image)
    subtract_background(image)
    #median(image)
    minimum(image)
    mask = rats(image)
    close(image)
    return mask

@show
def preprocess(stack :ImagePlus, register=True) -> ImagePlus:
    enhance_contrast(stack,True)
    subtract_background(stack, True)
    enhance_contrast(stack,True)
    median(stack,True)
    if register:
        aligned = align(stack)
        return aligned
    else:
        return stack
    

def generate_rois(mask :ImagePlus) -> list:
    skeleton = mask.duplicate()
    skeleton.show()
    skeletonize(skeleton)
    rois = []
    for x in range(skeleton.width):
        for y in range(skeleton.height):
            if skeleton.getPixel(x,y)[0]:
                IJ.doWand(mask, x, y, 0, String("4-connected"))
                roi = mask.getRoi()
                area = roi.getStatistics().area
                if not any(map(lambda r:r.equals(roi),rois)) and area > 25:
                    rois.append(roi)
    close(skeleton)
    return rois

def contains(outer :Roi, inner :Roi) -> bool:
    polygon = inner.getPolygon()
    return all(map(outer.contains, polygon.xpoints, polygon.ypoints))

def loadroi(filename, multiple=True) -> list:
    """open an roi or roi archive file
    and produce a list with all contained rois.
    List has 1 element if a .roi file.
    """
    rm = RoiManager(False)
    rm.runCommand(String("Open"),String(filename))
    if multiple:
        rois = rm.roisAsArray
        rm.close()
        return rois
    else:
        roi = rm.getRoi(0)
        rm.close()
        return [roi]

def saveroi(rois, filename):
    "save a list of roi objects as a zip archive"
    rm = RoiManager(False)
    for roi in rois:
        rm.addRoi(roi)
    rm.runCommand(String("Save"),String(filename))
    rm.close()

def measure(data :ImagePlus, rois :list, background :Roi) -> tuple:
    "measure the rois and background region over the data/time"
    bg = []
    measurements = {}
    for i in range(1, data.getStackSize() + 1):
        data.setSlice(i)
        data.setRoi(background)
        bg_val = data.getStatistics().mean
        bg.append(bg_val)
        for roi in rois:
            data.setRoi(roi)
            val = data.getStatistics().mean
            measurements.setdefault(roi, []).append(val)
    return bg, measurements

def affiliate(measurements :dict, groups :list) -> dict:
    "affiliate roi measurements with groups"
    organized = {}
    for group in groups:
        for roi in measurements:
            if contains(group, roi):
                organized.setdefault(group, []).append(measurements[roi])
    for group in groups:
        organized[group] = numpy.array(organized[group]).T
    return organized



#what the hell is this normalizing against?
# the maximum value of the individual plant
def normalize_group_inplace(affil :dict, group):
    g = affil[group]
    newg = []
    for i in range(len(g[0])):
        newg.append(g[...,i] / g[...,i].max())
    newgarr = numpy.array(newg).T
    affil[group] = newgarr

def normbg(bg):
    arr = numpy.array(bg)
    return arr / arr.max()

def compute(arguments):
    if arguments[Param.GENERATE]:
        mfile = arguments[Param.MASK]
        mask = create_mask(mfile)
        rois = generate_rois(mask)
        saveroi(rois, arguments[Param.ROI])
        close(mask)
    else:
        rois = loadroi(arguments[Param.ROI])
    stack = openstack(arguments[Param.DATA])
    data = preprocess(stack)
    
    background = loadroi(arguments[Param.BACKGROUND])[0]
    bg,ments = measure(data,rois,background)
    groups = loadroi(arguments[Param.GROUPING])

    close(data)
    close(stack)
    
    relation = affiliate(ments, groups)

    if arguments[Param.NORM]:
        for g in groups:
            normalize_group_inplace(relation, g)
        bg = normbg(bg)

    return bg, relation, groups

if  __name__ == '__main__':
    arguments = ask_user()
    bg, relation, groups = compute(arguments)
    graph.saveall(arguments, relation, bg, groups)
    print(arguments)

import numpy
from matplotlib import pyplot
import userinterface
from paramnames import ParameterName
import java_interop
java_interop.setup()
import jnius


# java strings required for some ImageJ operations
String = jnius.autoclass("java.lang.String")

ImageJ = jnius.autoclass("net.imagej.ImageJ")
# must create to make ops succeed,
# and must be created prior to fiji class definitions
# to avoid an exception about an invalid legacy service
imagej = ImageJ()

# Import the following ImageJ classes because they are needed for the pipeline
IJ = jnius.autoclass("ij.IJ")
ImagePlus = jnius.autoclass("ij.ImagePlus")
FolderOpener = jnius.autoclass("ij.plugin.FolderOpener")
SIFT_Align = jnius.autoclass("SIFT_Align")
Macro = jnius.autoclass("ij.Macro")
WindowManager = jnius.autoclass("ij.WindowManager")
WM = WindowManager #short alias, static class -> no problems
ImageCalculator = jnius.autoclass("ij.plugin.ImageCalculator")
Roi = jnius.autoclass("ij.gui.Roi")
PolygonRoi = jnius.autoclass("ij.gui.PolygonRoi")
RATSQuadtree = jnius.autoclass("RATSQuadtree")#required to avoid RATS_ exception
RATS_ = jnius.autoclass("RATS_")
RoiManager = jnius.autoclass("ij.plugin.frame.RoiManager")

def close(image :ImagePlus):
    """close input image."""
    image.changes = False
    image.close()

def ijrun(image :ImagePlus, arg1 :str, arg2 :str):
    """invoke IJ.run, dealing with py to java string conversion"""
    IJ.run(image, String(arg1), String(arg2))

# one quirk of the ImageJ1 APIs is that images may need to be displayed
# for operations to be successful. This is weird, but since the ImageJ2
# APIs don't make sense to me, it is just something we have to deal with

def openstack(foldername :str) -> ImagePlus:
    stack = FolderOpener.open(String(foldername))
    stack.show()
    return stack

def openimage(filename :str) -> ImagePlus:
    image = ImagePlus(String(filename))
    image.show()
    return image

# "in place" means something is modified

def enhance_contrast(image :ImagePlus, stack=False):
    "increase image contrast in place"
    if stack:
        # we don't want to distort the data.
        # The rule about not changing data if normalize and equalize
        # are not selected is only respected when enhancing the contrast
        # of one image at a time. Thus, we have to enhance the contrast
        # of each item in a stack seperately.
        for i in range(1, image.getStackSize() + 1):
            image.setSlice(i)
            ijrun(image, "Enhance Contrast...", "saturated=0.3")
        image.setSlice(1)
    else: # contrast matters more than preserving info when segmenting
        ijrun(image, "Enhance Contrast...", "saturated=0.3 equalize")

def median(image :ImagePlus, stack = False):
    " run median filter (r=2) in place "
    if stack:
        ijrun(image, "Median...", "radius=2 stack")
    else:
        ijrun(image, "Median...", "radius=2")

def minimum(image :ImagePlus, stack = False):
    " run minimum filter (r=2) in place "
    if stack:
        ijrun(image, "Minimum...", "radius=2 stack")
    else:
        ijrun(image, "Minimum...", "radius=2")

def subtract_background(image :ImagePlus, stack = False):
    " subtract background of image in place "
    if stack:
        arg2 = "rolling=50 stack"
    else:
        arg2 = "rolling=50"
    ijrun(image, "Subtract Background...", arg2)

# if you see arguments and you are not entirely sure what they do or
# why they are there, there is a good chance that they are just the
# default arguments for that command. default parameters usually work
# better than most other settings, although they still have to be
# specified explicitly, they cannot be replaced by empty strings
# for one reason or another, usually because unset parameters trigger
# dialog boxes, and those make it so the pipeline is not automatic
# past the initial parameter stage, which goes counter to its goals.

def align(stack :ImagePlus) -> ImagePlus:
    "align stack with SIFT. creates new image, probably does not modify input."
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
    aligned.show() # probably unneccesary, but why take chances?
    return aligned

def skeletonize(mask :ImagePlus):
    "reduces image to map of its structure in place"
    ijrun(mask, "8-bit", "")
    ijrun(mask, "Skeletonize", "")

def rats(image :ImagePlus) -> ImagePlus:
    """Use RATS plugin on the input.
    Creates new image, probably does not change input"""
    arg = String("noise=25 lambda=3 min=410")
    Macro.setOptions(arg) # this one also queries the macro arg, so set it
    # RATS_ has to be invoked in a kind of weird way compared to previous
    # commands. However, it seems to work, and so I don't worry about it.
    rat = RATS_()
    rat.setup(arg,image)
    proc = image.getProcessor()
    rat.run(proc)
    mask = WM.getCurrentImage()
    mask.show()
    return mask

def create_mask(filename :str) -> ImagePlus:
    image = openimage(filename)
    enhance_contrast(image)
    subtract_background(image)
    median(image)
    mask = rats(image)
    close(image)
    return mask

def prep_data(foldername :str) -> ImagePlus:
    data = openstack(foldername)
    enhance_contrast(data, True)
    subtract_background(data, True)
    enhance_contrast(data, True)
    median(data,True)
    return data

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

def save_rois(rois :list, filename :str):
    "save a list of roi objects as a zip archive"
    rm = RoiManager(False)
    for roi in rois:
        rm.addRoi(roi)
    rm.runCommand(String("Save"),String(filename))
    rm.close()

def open_archive(filename :str) -> list:
    "open an archive of roi objects as a list of roi objects"
    rm = RoiManager(False)
    rm.runCommand(String("Open"),String(filename))
    rois = rm.roisAsArray
    rm.close()
    return rois

def open_roi(filename :str) -> Roi:
    "open an roi file as an roi"
    rm = RoiManager(False)
    rm.runCommand(String("Open"),String(filename))
    roi = rm.getRoi(0)
    rm.close()
    return roi

def contains(outer :Roi, inner :Roi) -> bool:
    "check if outer contains inner geometrically"
    polygon = inner.getPolygon()
    return all(map(outer.contains, polygon.xpoints, polygon.ypoints))

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

def analyze(params):
    prepped = prep_data(params[ParameterName.DATADIR.value])
    if params[ParameterName.ALIGN.value]:
        data = align(prepped)
        close(prepped)
    else:
        data = prepped

    if params[ParameterName.USE_EXIST.value]:
        rois = open_archive(params[ParameterName.EXIST_ROI.value])
    else:
        mask = create_mask(params[ParameterName.MASK.value])
        rois = generate_rois(mask)
        if params[ParameterName.SAVE_GEN.value]:
            save_rois(rois, params[ParameterName.NEW_ROI.value])
        close(mask)
    background = open_roi(params[ParameterName.BG.value])
    groups = open_archive(params[ParameterName.GROUPS.value])
    bg_measurements,measurements = measure(data, rois, background)
    close(data)
    grouped = affiliate(measurements, groups)
    return grouped, bg_measurements

def inhours(interval) -> float:
    hour = interval[ParameterName.HOUR.value]
    minute_in_hours = interval[ParameterName.MINUTE.value] / 60
    return hour + minute_in_hours

def times_elapsed(hours :float, tpoints :int):
    return [hours * t for t in range(tpoints)]

def display(organized_data:dict,background_data:list,start,interval,normalized):
    xlabel = "Hours since {0}:{1}".format(
        str(start[ParameterName.HOUR.value]).zfill(2),
        str(start[ParameterName.MINUTE.value]).zfill(2)
        )
    hours = inhours(interval)
    _k = tuple(organized_data.keys())[0]
    _d = organized_data[_k]
    tpoints = len(_d)
    xticks = times_elapsed(hours, tpoints)
    if normalized:
        ylabel = "Normalized (Relative?) Intensity"
    else:
        ylabel = "(Relative?) Intensity"
    for i,key in enumerate(organized_data):
        pyplot.plot(xticks, organized_data[key])
        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)
        pyplot.title(f"Group {i+1}")
        pyplot.show()
    for i,key in enumerate(organized_data):
        pyplot.plot(xticks,organized_data[key].mean(axis=1),label=f"Group {i+1}")
    pyplot.plot(background_data, label="Background")
    pyplot.legend()
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.title("Summary")
    pyplot.show()

def normalize(data :dict):
    "normalize each plant in each group individually in place"
    for group in data:
        newg = []
        g = data[group]
        for i in range(len(g[0])):
            newg.append(g[...,i] / g[...,i].max())
        newgarr = numpy.array(newg).T
        data[group] = newgarr
    return None

def norm_bg(background :list):
    "create a normalized version of the background measurements"
    arr = numpy.array(background)
    return arr / arr.max()

    
def main():
    params = userinterface.ask_user()
    data, background = analyze(params)
    if params[ParameterName.NORM.value]:
        normalize(data)
        background = norm_bg(background)
    display(data,
            background,
            params[ParameterName.START.value],
            params[ParameterName.INTERVAL.value],
            params[ParameterName.NORM.value]
            )
    return None

if __name__ == '__main__':
    main()
    

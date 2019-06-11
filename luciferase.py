import glob
import math
import os
import jnius_config
import tkinter as tk
from tkinter import filedialog as fd
from matplotlib import pyplot
import pandas

def get_imagej_folder():
    window = tk.Tk()
    folder = fd.askdirectory(
        master=window,
        title="Please select your Fiji folder",
        initialdir=os.environ['HOME'] + '/Fiji.app'
        )
    window.destroy()
    return folder + "/"

imagej_folder = get_imagej_folder()
# Need to get ImageJ's java home for its class library
os.environ['JAVA_HOME'] = glob.glob(imagej_folder + '/**/jdk*/',recursive=True)[0]
# Find ALL of the jar files within imagej to have access to all included classes
jnius_config.add_classpath(*glob.glob(imagej_folder+"**/*.jar",recursive=True))

import jnius


ImageJ = jnius.autoclass('net.imagej.ImageJ')

# ImageJ must be initiated in order for most operations to function
imagej = ImageJ()

IJ = jnius.autoclass('ij.IJ')
ImagePlus = jnius.autoclass('ij.ImagePlus')
FolderOpener = jnius.autoclass('ij.plugin.FolderOpener')
String = jnius.autoclass('java.lang.String')
SIFT_Align = jnius.autoclass('SIFT_Align')
Macro = jnius.autoclass('ij.Macro')
WindowManager = jnius.autoclass('ij.WindowManager')
ImageCalculator = jnius.autoclass('ij.plugin.ImageCalculator')
Roi = jnius.autoclass('ij.gui.Roi')
PolygonRoi = jnius.autoclass('ij.gui.PolygonRoi')
RATSQuadtree = jnius.autoclass('RATSQuadtree')
RATS_ = jnius.autoclass("RATS_")
RoiManager = jnius.autoclass('ij.plugin.frame.RoiManager')


def enhance_contrast(stack):
    IJ.run(stack,
           String("Enhance Contrast..."),
           String("saturated=0.3 equalize process_all")
           )

def median(stack):
    IJ.run(stack,
           String("Median..."),
           String("radius=2 stack")
        )

def minimum(stack):
    IJ.run(stack,
           String("Minimum..."),
           String("radius=2 stack")
        )

def open_stack(foldername):
    name = String(foldername)
    stack = FolderOpener.open(name)
    stack.show()
    return stack

def open_image(filename):
    name = String(filename)
    image = ImagePlus(name)
    image.show()
    return image

def subtract_background(stack):
    IJ.run(stack,
           String("Subtract Background..."),
           String("rolling=50 stack")
           )

def align(stack):
    stack.show()
    sifter = SIFT_Align()
    Macro.setOptions(
        String("initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")
        )
    sifter.run(
        String("initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate")
        )
    aligned = WindowManager.getCurrentImage()
    aligned.show()
    stack.changes = False
    stack.close()
    return aligned

def ijrun(image,arg1,arg2):
    IJ.run(image,String(arg1),String(arg2))


def make_mask(image):
    arg = String("noise=25 lambda=3 min=410")
    ijrun(image,"Enhance Contrast...","saturated=0.3 equalize")
    ijrun(image,"Median...","radius=2")
    ijrun(image,"Subtract Background...","rolling=50")
    Macro.setOptions(arg)
    rat = RATS_()
    rat.setup(arg,image)
    proc = image.getProcessor()
    rat.run(proc)
    mask = WindowManager.getCurrentImage()
    image.changes = False
    image.close()
    ijrun(mask,"Minimum...","radius=2")
    ijrun(mask,"16-bit","")
    ijrun(mask,"Multiply...","value=257")
    return mask

def apply_mask(stack,mask):
    ic = ImageCalculator()
    applied = ic.run(
        String("AND create stack"),
        stack,
        mask
        )
    applied.show()
    return applied

def open_as_mask(filename):
    image = open_image(filename)
    return make_mask(image)

def initial_filtering(stack, mask):
    mask.hide()
    enhance_contrast(stack)
    median(stack)
    subtract_background(stack)
    aligned = align(stack)
    mask.show()
    filtered = apply_mask(aligned,mask)
    aligned.changes = False
    aligned.close()
    return filtered

def region(mask,bx,by,width,height):
    mask.setRoi(bx,by,width,height)
    roi = mask.getRoi()
    points = roi.getContainedPoints()
    bright = [p for p in points if mask.getPixel(p.x,p.y)[0]]
    if not bright:
        return None
    if len(bright) == len(points):
        return Roi(bx,by,width,height)
    
    def isborder(point):
        is_top = abs(point.y - by) <= 1
        is_bottom = abs(point.y - (by + height)) <= 1
        is_left = abs(point.x - bx) <= 1
        is_right = abs(point.x - (bx + width)) <= 1
        return is_top or is_bottom or is_left or is_right

    def adj_off(point):
        a = mask.getPixel(point.x - 1,point.y)[0]
        b = mask.getPixel(point.x + 1,point.y)[0]
        c = mask.getPixel(point.x, point.y - 1)[0]
        d = mask.getPixel(point.x, point.y + 1)[0]
        return not (a or b or c or d)

    bright = [b for b in bright if isborder(b) or adj_off(b)]

    if not bright:
        return None

    x_avg = int(sum(b.x for b in bright) / len(bright))
    y_avg = int(sum(b.y for b in bright) / len(bright))

    def angle(point):
        x = point.x - x_avg
        y = point.y - y_avg
        if x == 0 and y > 0:
            return math.pi / 2
        elif x == 0 and y < 0:
            return 3 * math.pi / 2
        elif x > 0 and y >= 0:
            return math.atan(y / x)
        elif x > 0 and y < 0:
            return math.atan(y / x) + 2 * math.pi
        elif x < 0:
            return math.atan(y / x) + math.pi
        elif x==0 and y==0:
            return 0
        else:
            raise Exception("This should be impossible")
    
    bright.sort(key=angle)

    xvals = [point.x for point in bright]
    yvals = [point.y for point in bright]
    polygon = PolygonRoi(xvals,yvals,len(bright),Roi.POLYGON)
    return polygon
    
def locate_plants(mask, plant_width, plant_height, fname=''):
    rm = RoiManager(False)
    for x in range(0,mask.getWidth(),plant_width):
        for y in range(0,mask.getHeight(),plant_height):
            poly = region(mask,x,y,plant_width,plant_height)
            if poly and poly.statistics.area > 100:
                rm.addRoi(poly)
    if fname:
        rm.runCommand(String("Save"), String(fname))
    rois = rm.getRoisAsArray()
    rm.close()
    return rois

class LabeledScale(tk.Frame):

    def __init__(self, master, high, low, label, var):
        tk.Frame.__init__(self, master)
        self.scale = tk.Scale(self,
                              from_=low,
                              to=high,orient=tk.HORIZONTAL,
                              variable=var
                              )
        self.label = tk.Label(self, text=label)
        self.var = var

        self.down = tk.Button(self,
                              text="-",
                              command=lambda:self.var.set(
                                  self.var.get() - 1
                                  )
                              )
        self.up = tk.Button(self,
                            text="+",
                            command=lambda:self.var.set(
                                self.var.get() + 1
                                )
                            )
        

        self.label.pack(side=tk.TOP)
        self.scale.pack(side=tk.BOTTOM)
        self.down.pack(side=tk.LEFT)
        self.up.pack(side=tk.RIGHT)

    def get(self):
        return self.var.get()

class FileEntry(tk.Frame):

    def __init__(self, master, var, text, folder=False, save=False):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text=text)
        self.entry = tk.Entry(self, textvariable=var)
    
        if folder:
            self.button = tk.Button(self,
                                    text=text,
                                    command=lambda:var.set(fd.askdirectory())
                                    )
        elif not save:
            self.button = tk.Button(self,
                                    text=text,
                                    command=lambda:var.set(fd.askopenfilename())
                                    )
        else:
            self.button = tk.Button(self,
                                    text=text,
                                    command=lambda:var.set(fd.asksaveasfilename())
                                    )
        
        self.var = var

        self.label.grid(row=0,column=0)
        self.entry.grid(row=0,column=1)
        self.button.grid(row=0,column=2)

    def get(self):
        return self.var.get()


class UserInterface:
    
    def __init__(self):
        
        self.folder = ''
        self.mask_image = ''
        
        self.roi_width = 0
        self.roi_height = 0
        
        self.background_bx = 0
        self.background_by = 0
        self.background_width = 0
        self.background_height = 0

        self.custom_roi = ''
        self.use_custom_roi = False

        self.save_rois = False
        self.roi_file = ''

        self.group_file = ''

        self.pause = False


    def user_input(self, master):
        root = tk.Toplevel(master)
        bx,by,b_width,b_height = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
        folder,mask = tk.StringVar(),tk.StringVar()
        r_width,r_height = tk.IntVar(),tk.IntVar()
        custom_roi = tk.StringVar()
        use_custom_roi = tk.BooleanVar()

        save_roi = tk.BooleanVar()
        roi_file = tk.StringVar()

        group_file = tk.StringVar()

        group_entry = FileEntry(root, group_file, "File With groups as Rois")

        roi_entry = FileEntry(root, roi_file, "Name file to save Rois in", save=True)
        roi_check = tk.Checkbutton(root, variable=save_roi, text="Save Rois?")

        sequence_entry = FileEntry(root, folder, "Choose folder of data images.", True)
        mask_entry = FileEntry(root, mask, "Choose image for segmentation creation.")

        custom_roi_entry = FileEntry(root, custom_roi, "Choose custom roi file")
        use_custom_box = tk.Checkbutton(root,variable=use_custom_roi, text="Use custom roi file")

        background_label = tk.Label(root, text="Background Comparision Region")
        bx_scale = LabeledScale(root, 200, 1, "bx", bx)
        by_scale = LabeledScale(root, 200, 1, 'by', by)
        b_width_scale = LabeledScale(root, 200, 1, "width", b_width)
        b_height_scale = LabeledScale(root, 200, 1, "height", b_height)

        roi_label = tk.Label(root, text="Region of interest size parameters")
        r_width_scale = LabeledScale(root, 200, 10, "ROI width", r_width)
        r_height_scale = LabeledScale(root, 200, 10, "ROI height", r_height)

        done_button = tk.Button(root,text="Ready to go!",command=master.destroy)

        root.title("Program Options")

        sequence_entry.grid(row=0,columnspan=3)
        mask_entry.grid(row=1,columnspan=3)

        custom_roi_entry.grid(row=2,columnspan=3)
        use_custom_box.grid(row=2,column=3,sticky=tk.W)

        roi_entry.grid(row=3,columnspan=3)
        roi_check.grid(row=3,column=3,sticky=tk.W)

        group_entry.grid(row=4,columnspan=3)

        background_label.grid(row=5,column=0)
        bx_scale.grid(row=6,column=0)
        by_scale.grid(row=7,column=0)
        b_width_scale.grid(row=8,column=0)
        b_height_scale.grid(row=9,column=0)

        roi_label.grid(row=5,column=1)
        r_width_scale.grid(row=6,column=1)
        r_height_scale.grid(row=7,column=1)
        

        done_button.grid(columnspan=3)

        root.mainloop()

        self.folder = folder.get()
        self.mask_image = mask.get()
        
        self.roi_width = r_width.get()
        self.roi_height = r_height.get()
        
        self.background_bx = bx.get()
        self.background_by = by.get()
        self.background_width = b_width.get()
        self.background_height = b_height.get()

        self.custom_roi = custom_roi.get()
        self.use_custom_roi = use_custom_roi.get()

        self.save_rois = save_roi.get()
        self.roi_file = roi_file.get()
        self.group_file = group_file.get()

def get_groups(filename):
    rm = RoiManager(False)
    rm.runCommand(String("Open"),String(filename))
    rois = rm.getRoisAsArray()
    rm.close()
    return rois

# checks if the `outer` ROI contains the `inner` ROI
def contains(outer, inner):
    polygon = inner.getPolygon()
    return all(map(outer.contains, polygon.xpoints, polygon.ypoints))

# Creates a dictionary that puts all rois belonging to a group
# in a list as the value associated with a key that corresponds to
# a group's position in the input list
def affiliate(groups :list, rois :list) -> dict:
    areas = {}
    for roi in rois:
        unused = True
        for i,group in enumerate(groups):
            if contains(group, roi):
                areas.setdefault(i, []).append(roi)
                unused = False
                break
        if unused:
            # ROIs not affiliated with any group go into the list
            # affilated with the key of -1.
            areas.setdefault(-1, []).append(roi)
    return areas


if __name__ == '__main__':
    god = tk.Tk()
    ui = UserInterface()
    ui.user_input(god)
    mask = open_as_mask(ui.mask_image)
    stack = open_stack(ui.folder)
    processed = initial_filtering(stack, mask)
    del stack
    if ui.use_custom_roi:
        get_rois = get_groups
        rois = get_rois(ui.custom_roi)
    elif ui.save_rois:
        rois = locate_plants(mask, ui.roi_width, ui.roi_height,ui.roi_file)
    else:
        rois = locate_plants(mask, ui.roi_width, ui.roi_height)
    groups = get_groups(ui.group_file)
    # each of the areas is an experimental group as defined in the group file
    areas = affiliate(groups, rois)
    # the nature of the measurements dict should be explained
    # the outer layer is a dictionary with the key being the experimental
    # group, and the value being a dictionary where the key is the point in
    # time, and the value is a list of the values of the rois in that
    # experimental group, at that point in time
    measurements = {}
    background = []
    for t in range(processed.getStackSize()):
        processed.setSlice(t + 1)
        processed.setRoi(ui.background_bx,
                         ui.background_by,
                         ui.background_width,
                         ui.background_height)
        background.append(processed.getStatistics().mean)
        for j,area in areas.items():
            for roi in area:
                processed.setRoi(roi)
                value = roi.statistics.mean * roi.statistics.area * roi.statistics.areaFraction / 100
                measurements.setdefault(j, {}).setdefault(t, []).append(value)
    
    # hide the ImageJ windows so that only the graphs are displayed
    log = WindowManager.getWindow(String("Log"))
    log.hide()
    processed.hide()
    mask.hide()

    for groupkey in measurements:
        group = measurements[groupkey]
        g_avgs = [sum(group[i]) / len(group[i]) for i in range(len(group))]
        if groupkey != -1:
            pyplot.plot(g_avgs,label="Group {}".format(groupkey))
            
        else:
            pyplot.plot(g_avgs,label="Unclassified")

    pyplot.plot(background, label="Background")
    pyplot.legend()
    pyplot.title("Average Group Brightness over Time")
    pyplot.xlabel("Time (Sort of)")
    pyplot.ylabel("Brightness")
    pyplot.show()

    try:
        os.mkdir("output")
    except FileExistsError:
        pass
    
    for gkey, gvalues in measurements.items():
        frame = pandas.DataFrame(gvalues)
        frame = frame.T
        frame.to_excel("output/group_{}.xlsx".format(gkey),index=False,header=False)

    for groupkey in measurements:
        group = measurements[groupkey]
        pyplot.plot(group.values())
        pyplot.title("Group {}".format(groupkey))
        pyplot.xlabel("Time")
        pyplot.ylabel("Brightness")
        pyplot.show()

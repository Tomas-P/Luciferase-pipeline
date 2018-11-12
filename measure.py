import sys
from ij import ImagePlus,IJ
from ij.plugin.frame import RoiManager
from ij.measure import ResultsTable
import json

def folder():
    script = sys.argv[0]
    return script[:script.rfind('/')]

def open_stack():
    filename = folder() + "/artifacts/stack.tif"
    return ImagePlus(filename)

def open_roi_archive():
    rm = RoiManager(False)
    optfile = open(folder() + "/config/options.json")
    options = json.load(optfile)
    optfile.close()
    if not options["use custom roi"]:
        filename = folder() + "/artifacts/RoiSet.zip"
    else:
        filename = options["custom roi"]
    rm.runCommand("Open", filename)
    rois = rm.getRoisAsArray()
    rm.close()
    return rois

def open_group_archive():
    rm = RoiManager(False)
    gfilename = folder() + "/config/GroupDefinitions.zip"
    rm.runCommand("Open", gfilename)
    groups = rm.getRoisAsArray()
    rm.close()
    return groups
    

def contains(outer,inner):
    # check if the outer ROI contains the inner Roi
    inner_points = inner.getContainedPoints()
    return all([outer.contains(point.x,point.y) for point in inner_points])


def measure():
    stack = open_stack()
    rois = open_roi_archive()
    groups = open_group_archive()
    table = ResultsTable()
    IJ.run("Set Measurements...", "area mean area_fraction stack redirect=None decimal=3")
    row=0
    stack.show()
    table.show("Results")
    for i in range(stack.getImageStackSize()):
        for roi in rois:
            
            stack.setRoi(roi)
            group_number = 0
            
            for j,group in enumerate(groups):
                if contains(group, roi):
                    group_number = j + 1
                    break
            
            
            stats = roi.getStatistics()
            table.setValue("Mean",row,stats.mean)
            table.setValue("Area_Fraction",row,stats.areaFraction)
            table.setValue("Group_Number",row,group_number)
            table.setValue("Area",row,stats.area)
            table.setValue("Slice",row,i)
            table.show("Results")
            row += 1
        
        IJ.run(stack, "Next Slice [>]", "")
    IJ.saveAs("Results", folder() + "/artifacts/measurements.csv")

if sys.argv[0].endswith("measure.py"):
    measure()
    print("Plant measurements complete and saved")

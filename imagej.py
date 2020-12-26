
import java
java.setup()
import jnius

String = jnius.autoclass('java.lang.String')
ImageJ = jnius.autoclass('net.imagej.ImageJ')
Our_imagej = ImageJ()
IJ1Helper = jnius.autoclass("net.imagej.legacy.IJ1Helper")
IJ = jnius.autoclass('ij.IJ')
ImagePlus = jnius.autoclass('ij.ImagePlus')
FolderOpener = jnius.autoclass('ij.plugin.FolderOpener')
SIFT_Align = jnius.autoclass("SIFT_Align")
Macro = jnius.autoclass("ij.Macro")
WindowManager = jnius.autoclass("ij.WindowManager")
WM = WindowManager
ImageCalculator = jnius.autoclass("ij.plugin.ImageCalculator")
Roi = jnius.autoclass("ij.gui.Roi")
PolygonRoi = jnius.autoclass("ij.gui.PolygonRoi")
# req to avoid RATS_ exception
RatsQuadtree = jnius.autoclass("RATSQuadtree")
RATS_ = jnius.autoclass("RATS_")
RoiManager = jnius.autoclass("ij.plugin.frame.RoiManager")

def close(image :ImagePlus):
    'closes input image'
    image.changes = False
    image.close()

def ijrun(image :ImagePlus, arg1 :str, arg2:str=""):
    'invoke IJ.run, deals with str->String conversion'
    IJ.run(image, String(arg1), String(arg2))

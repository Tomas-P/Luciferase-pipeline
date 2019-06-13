from luciferase import open_image, ijrun, String, Macro, RATS_, WindowManager, IJ, RoiManager
from tkinter.filedialog import askopenfilename

def make_mask(image):
    ijrun(image, "Enhance Contrast...", "saturated=0.3 equalize")
    ijrun(image, "Median...", "radius=2")
    ijrun(image, "Subtract Background...", "rolling=50")
    arg = String("noise=25 lambda=3 min=410")
    Macro.setOptions(arg)
    rat = RATS_()
    rat.setup(arg, image)
    proc = image.getProcessor()
    rat.run(proc)
    mask = WindowManager.getCurrentImage()
    mask.show()
    ijrun(mask, "Minimum...", "radius=2")
    return mask

def skeletonize(mask):
    ijrun(mask, "Skeletonize", "")

def get_brights(mask):
    pixels = []
    for x in range(mask.width):
        for y in range(mask.height):
            if mask.getPixel(x,y)[0]:
                pixels.append((x,y))

    return pixels

def close(imp):
    imp.changes = False
    imp.close()

def wand_all(image, points):
    rois = []
    for x,y in points:
        IJ.doWand(image, x, y, 0, "4-connected")
        r = image.getRoi()
        if not any(map(lambda roi : roi.equals(r), rois)):
            rois.append(r)
    return rois

if __name__ == '__main__':

    image = open_image(askopenfilename())
    image.show()
    mask = make_mask(image)
    mask.show()
    skeletonize(mask)
    brights = get_brights(mask)
    close(mask)
    close(image)
    del mask
    del image
    image = open_image("/home/tomas/Documents/Colleen/Images/2018-09-06_time_course/Pos0/img_000000000_Default_000.tif")
    image.show()
    mask = make_mask(image)
    image.hide()
    wanded = wand_all(mask, brights)
    mask.hide()

    rm = RoiManager()
    for roi in wanded:
        rm.addRoi(roi)

    rm.runCommand(String("Save"), String(input("where to save? ")))
    rm.close()

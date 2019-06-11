from luciferase import open_image, make_mask, IJ, RoiManager
from tkinter.filedialog import askopenfilename
from tkinter import Tk

def get_fname():
    base = Tk()
    fname = askopenfilename(master=base,title="What image?")
    base.destroy()
    return fname

def wand_all_pixels(mask):
    width = mask.getWidth()
    height = mask.getHeight()
    for x in range(width):
        for y in range(height):
            if mask.getPixel(x,y)[0]:
                IJ.doWand(mask,x,y,0,"Legacy")
                roi = mask.getRoi()
                yield roi


if __name__ == '__main__':
    image_name = get_fname()
    image = open_image(image_name)
    mask = make_mask(image)
    mask.changes = False
    wand_gen = wand_all_pixels(mask)
    rois = []
    for roi in wand_gen:
        if not any(map(lambda r : r.equals(roi), rois)):
            rois.append(roi)

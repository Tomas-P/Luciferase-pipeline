import imagej_interface
import lucbase
from PIL import Image

def to_binary(folder:lucbase.Folder,to_dither=None)->None:
    '''Converts all images in a folder to be binary
    each pixel either black or white. This operation
    happens in place, so be carefull.'''
    for file in folder.files:
        image = Image.open(file)
        im = image.convert("1",dither=None)
        im.save(file)

def to_greyscale(folder:lucbase.Folder)->None:
    "Converts all images in a folder to greyscale."
    for file in folder.files:
        image = Image.open(file)
        im = image.convert("L")
        im.save(file)

def prep_images(infolder:lucbase.Folder,outfolder:lucbase.Folder,imagej:lucbase.Folder)->None:
    '''Takes each image in the infolder,
performs a series of operations designed to reduce noise,
and saves it in the outfolder.'''
    for i,file in enumerate(infolder.files):
        macro = [f"open('{file}');",
                 "run('Subtract Background...', 'rolling=50');",
                 "run('Enhance Contrast...', 'saturated=0.3');",
                 f"saveAs('Tiff', '{outfolder.foldername}\\\\mydata{i}.tif');"]
        mymacro = imagej_interface.ijline(imagej,macro,True)
        imagej_inteface.shell(mymacro)

def find_rois(data:lucbase.Folder,roi:lucbase.Folder,imagej:lucbase.Folder)->None:
    """Find the regions of interest for each image, and save that to the roi folder.
Converts to 8-bit greyscale prior to doing anything else in order to allow the use
of the Statistical Region Merging plugin in Imagej."""
    for i,file in enumerate(data.files):
        macro = [f"open('{file}');",
                 "run('Conversions...', 'scale weighted');",
                 "run('8-bit');",
                 "run('Statistical Region Merging', 'q=25 showaverages');",
                 f"saveAs('Tiff', '{roi.foldername}\\\\roi{i}.tif');"]
        mymacro = imagej_interface.ijline(imagej,macro,True)
        imagej_interface.shell(mymacro)

def create_rois(data:lucbase.Folder, roi:lucbase.Folder, imagej:lucbase.Folder)->None:
    """Finds the regions of interest for each imagej,
saves them as an image, and converts them to binary (black and white)."""
    find_rois(data,roi,imagej)
    to_binary(roi)

def main()->None:
    '''A function to do the following
* Filter noise out from raw images to make data images and save them
* Find the regions of interest of those data images and save them as files
* Convert these regions of interest images to black and white
Which then forms the processing aspect of the pipeline.
'''
    config = lucbase.Config()
    ImageJ = lucbase.Folder(config[lucbase.IMAGEJ])
    data = lucbase.Folder(config[lucbase.DATA])
    roi = lucbase.Folder(config[lucbase.ROI])
    raw = lucbase.Folder(config[lucbase.RAW])
    # first star
    prep_images(raw, data, ImageJ)
    # second and third star
    create_rois(data, roi, ImageJ)

if __name__ == '__main__':
    main()

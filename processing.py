import imagej_interface
import lucbase

def old_process(out:lucbase.Folder,imagej:lucbase.Folder)->None:
    "run the older processing macro"
    old = ["dir = getDirectory('Choose the folder with your raw images');",
           'files = getFileList(dir);',
           'for(i=0; i<files.length; i++){',
           '  open(files[i]);',
           '}',
           "run('Images to Stack', 'name=exStack title=[] use');",
           "run('Rigid Registration', 'initialtransform=[] n=1 tolerance=1.000 level=7 stoplevel=2 materialcenterandbbox=[] template=exStack measure=Euclidean');", "run('Subtract Background...', 'rolling=50 stack');", "setAutoThreshold('Default');", "//run('Threshold...');", "call('ij.plugin.frame.ThresholdAdjuster.setMode', 'B&W');", "call('ij.plugin.frame.ThresholdAdjuster.setMode', 'Red');", "setOption('BlackBackground', false);", "run('Convert to Mask', 'method=Default background=Light calculate');",
           "run('Median...', 'radius=2 stack');",
           "run('Gaussian Blur...', 'sigma=2 stack');",
           r"run('Image Sequence... ', 'format=TIFF save={0}\\data0000.tif');"
           ]
    old[-1] = old[-1].format(out.foldername)
    cmdmacro = imagej_interface.ijline(imagej,old)
    imagej_interface.shell(cmdmacro)

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
        imagej_interface.shell(mymacro)


def main()->None:
    '''A function to filter noise out from raw images to make
data images and save them
in the correct location
'''
    config = lucbase.Config()
    ImageJ = lucbase.Folder(config[lucbase.IMAGEJ])
    data = lucbase.Folder(config[lucbase.DATA])
    roi = lucbase.Folder(config[lucbase.ROI])
    raw = lucbase.Folder(config[lucbase.RAW])
    prep_images(raw, data, ImageJ)

if __name__ == '__main__':
    main()

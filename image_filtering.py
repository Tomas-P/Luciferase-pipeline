from data_storing_objects import Folder, Config
from subprocess import run
import tkinter.filedialog as filedialog
import glob
import re

def finding_macro_dir(ImageJ_Folder):
    names = ImageJ_Folder.files
    for name in names:
        matches = re.findall(ImageJ_Folder.foldername+'/macros$',name)
        if len(matches) != 0:
            break
    return matches[0] # there should only be one match

def Preproccess(macro_dir, output_dir, folder_path):
    # doubled braces are where I don't want to substitute in an object
    macro_text = '''
dir = getDirectory("Choose the folder with your raw images");
files = getFileList(dir);
for(i=0; i<files.length; i++){{
	open(files[i]);
}}
run("Images to Stack", "name=exStack title=[] use");
run("Rigid Registration", "initialtransform=[] n=1 tolerance=1.000 level=7 stoplevel=2 materialcenterandbbox=[] template=exStack measure=Euclidean");
run("Subtract Background...", "rolling=50 stack");
setAutoThreshold("Default");
//run("Threshold...");
call("ij.plugin.frame.ThresholdAdjuster.setMode", "B&W");
call("ij.plugin.frame.ThresholdAdjuster.setMode", "Red");
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light calculate");
run("Median...", "radius=2 stack");
run("Gaussian Blur...", "sigma=2 stack");
run("Image Sequence... ", "format=TIFF save={0}\\\\exStack0000.tif");
'''.format(output_dir.replace('/', '\\\\'))
    # the text for the macro needs the backslashes becuase I am using
    # an ImageJ macro
    # to make ImageJ do what I want

    # helps the user verify the macro text is correct
    print(macro_text) 

    # check to see if the macro already exists, and write the text
    # if and only if it does not exists
    try: 
        t = open(macro_dir + '/preproccess_macro.ijm', 'r')
    except:
        exists = False
    else:
        t.close()
        exists = True
    if not exists:
        with open(macro_dir + '/preproccess_macro.ijm', 'w') as macro:
            macro.write(macro_text)
    else:
        pass

    # run the macro from the shell
    # this directory needs to be changed
    run('cd {0} && ImageJ-win64.exe -macro preproccess_macro.ijm'.format(folder_path.replace('/','\\')), shell=True)

if __name__ == '__main__':
    # data for preproccessing the images
    conf = Config()
    ImageJ = Folder(conf.config_data['ImageJ folder'])
    Data = Folder(conf.config_data['Data images'])
    macro_dir = finding_macro_dir(ImageJ)

    # actually preprocessing the images
    Preproccess(macro_dir, Data.foldername, ImageJ.foldername)

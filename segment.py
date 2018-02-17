from ImageJ_program import ImageJ
import lucbase2 as luc
from os import remove
from sys import argv

def segment():
    # runs a segmentation in ImageJ.
    # makes it very easy to use from Python.
    a_macro = 'actualMacro.ijm'

    with open("TheOneTrueSegmentation.ijm") as the_one_true:
        s = the_one_true.read()
        
    config = luc.config()

    # the path of the folder with data images
    dt = config[luc.DATA]

    # a representation of the folder's contents
    dta = luc.Folder(dt)

    # the file needed to open all images in the file
    dta.sort()

    file = dta.files[0].replace('/',r'\\')

    # the macro we actually want to run
    segment = s.replace('<replace>',file)

    try:
        # we want to delete the file
        remove(a_macro)
    except FileNotFoundError:
        # the file is already gone and can be ignored
        pass

    with open(a_macro,'w') as actual:
        actual.write(segment)

    file = argv[0]
    folder = file[:file.rfind('\\')]
    macro = folder + '/' + a_macro

    ImageJ.run('--headless -macro {}'.format(macro))

if __name__ == '__main__':
    segment()

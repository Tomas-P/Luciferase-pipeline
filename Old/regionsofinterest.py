import lucbase
import imagej_interface

def segment():
    "A function to identify regions of interest using ImageJ"
    config = lucbase.Config()
    ImageJ = lucbase.Folder(config[lucbase.IMAGEJ])
    mymacro = '''input_folder = getDirectory('Choose the folder with the images you want to find the regions of interest of');
output_folder = getDirectory('Choose the folder where you want the rois saved');
run("Image Sequence...", "open="+input_folder+" sort");
run("8-bit");
run("Statistical Region Merging", "q=25 showaverages 3d");
setOption("BlackBackground",false);
run("Make Binary", "method=Huang background=Default calculate black");
print(input_folder);
print(output_folder);
run("Image Sequence... ", "format=TIFF name=roi_images save="+output_folder+"\\roi_images0000.tif");'''.replace("\"",'\'')
    commands = mymacro.split('\n')
    command_line_macro = imagej_interface.ijline(ImageJ,commands)
    return imagej_interface.shell(command_line_macro)

if __name__ == "__main__":
    segment()

# worry about tkinter later
# worry about ImageJ now
from data_storing_objects import Config, Folder
from subprocess import run
from PIL import Image

def write_cmd_commands(commands):
    '''takes list of string arguments and assembles them to
    a one-line series of cmd commands.
    '''
    return ' '.join(commands)

def write_ImageJ_commands(ImageJ_folder, commands):
    macro_com = ' '.join(commands)
    comms = write_cmd_commands(['cd',ImageJ_folder.foldername,
                       '&&','ImageJ-win64.exe','--headless','-eval',
                       '"{0}"'.format(macro_com)])
    return comms


if __name__ == '__main__':
    config = Config()
    ImageJ = Folder(config.config_data['ImageJ folder'])
    data_ims = Folder(config.config_data['Data images'])
    roi_ims = Folder(config.config_data['ROI images'])
    for i, file in enumerate(data_ims.files):
        comms = write_ImageJ_commands(ImageJ,
                ["open('{0}');".format(file.replace(
                '/', '\\\\')),
                 "run('Statistical Region Merging', 'q=25 showaverages');",
                 "saveAs('Tiff', '{0}\\\\roi{1}.tif');".format(roi_ims.foldername.replace(
                '/', '\\\\'), i)
                 ])
        run(comms, shell=True)

    rois = Folder(config.config_data['ROI images'])
    assert len(rois.files) > 0
    

import roi_script_early_version as rse
import data_storing_objects as dso
from image_filtering import finding_macro_dir

def contrast_filter():
    config = dso.Config()
    raws = dso.Folder(config.config_data['raw folder'])
    IJ = dso.Folder(config.config_data['ImageJ folder'])
    macrodir = finding_macro_dir(IJ)
    data = dso.Folder(config.config_data['Data images'])
    for i, raw in enumerate(raws.files):
        comms = rse.write_ImageJ_commands(IJ, ["open('{0}');".format(raw),
                                  "run('Enhance Contrast...', 'saturated=0.3');",
                                  "saveAs('Tiff', '{0}\\\\data{1}');".format(data.foldername,
                                                                             i)
                                       ]
                                  )
        rse.run(comms, shell=True)

if __name__ == '__main__':
    contrast_filter()
    

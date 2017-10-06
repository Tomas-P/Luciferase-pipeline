from PIL import Image
import data_storing_objects as dso
def convert_all_rois(config):
    rois = dso.Folder(config.config_data['ROI images'])
    # strings are smaller than arrays
    for roi in rois.files:
        #create an image object
        im = Image.open(roi)
        # convert it to black and white
        im = im.convert('1')
        # overwrite the origional file
        im.save(roi)

if __name__=='__main__':
    conf = dso.Config()
    convert_all_rois(conf)
    

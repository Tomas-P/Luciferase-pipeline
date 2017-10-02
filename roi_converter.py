from PIL import Image
import data_storing_objects as dso

conf = dso.Config()
rois = dso.Folder(conf.config_data['ROI images'])

# short strings are smaller than large arrays
for roi in rois.files:
    # first we create an image object
    im = Image.open(roi)

    # then convert it to black and white
    im = im.convert('1')

    #and finally overwrite the original file
    im.save(roi)

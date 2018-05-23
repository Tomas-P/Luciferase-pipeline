import imagej
import config
import folder

def register(tag):
    settings = config.configuration()
    my_folder = folder.Folder(settings[tag])
    imagej.run('''-eval "run('Image Sequence...',
'open={} sort');
run('Linear Stack Alignment with SIFT', 'initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size64 maximum_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate');
saveAs('Tiff', '{}/{}.tif');"'''.format(my_folder[0],
                                 my_folder.name[:my_folder.name.rfind('/')],
                                         tag
                                         )
               )
    return my_folder.name[:my_folder.name.rfind('/')] + '/' + tag + '.tif'

if __name__ == '__main__':
    filename = register(config.DATA)
    print(filename)

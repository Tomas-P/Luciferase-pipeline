import data_storing_objects as dso
from tkinter import filedialog

# median functions

def all_image_median(image):
    # finds the median of all pixels in an image
    vals = [pixel['data'] for pixel in image.generate_each_pixel_in_order()]
    vals.sort()
    return vals[int(len(vals)/2)]


def image_data_median(image):
    # finds the median of all pixels marked
    # as data in an image
    vals = [pixel['data'] for pixel in image.generate_each_pixel_in_order() if pixel['is data']==True]
    vals.sort()
    return vals[int(len(vals)/2)]


def image_median(image, data):
    # allows easier finding of medians based on the whole image
    # and medians based only on data pixels
    if data:
        return image_data_median(image)

    elif not data:
        return all_image_median(image)


# mean functions

def all_image_average(image):
    # finds the mean of all pixels in an image
    total = image.data.array.sum()
    avg = total / (len(image.data.array) * len(image.data.array[0]))
    return avg

def only_data_average(image):
    # finds the average of all data pixels in an image
    # incidently is only wrapper for one of the
    # object methods of the ImageDataPoints class
    # in data_storing_objects
    return image.average_data()

def image_average(image, data):
    # makes easy the finding of the image mean
    # and the data mean
    if data:
        return only_data_average(image)

    elif not data:
        return all_image_average(image)


# mode functions

def all_mode(image):
    # finds the mode of all pixels in an image
    counts = {}

    for pixel in image.generate_each_pixel_in_order():
        if pixel['data'] in counts:
            counts[pixel['data']] += 1
        else:
            counts[pixel['data']] = 1

    counts = list(zip(counts.values(), counts.keys()))
    counts.sort()
    return counts[0][1]

def data_mode(image):
    # finds the mode of all data pixels in an image
    counts = {}
    for pixel in image.generate_each_pixel_in_order():
        if not pixel['is data']:
            continue
        elif pixel['data'] in counts.keys():
            counts[pixel['data']] += 1
        else:
            counts[pixel['data']] = 1

    counts = list(zip(counts.values(), counts.keys()))
    counts.sort()
    return counts[0][1]

def mode(image, data):
    # makes finding the mode of an image
    # or the data pixels easier with the
    # image and a boolean parameter
    if data:
        return data_mode(image)
    elif not data:
        return all_mode(image)


# standard deviation functions

def all_deviation(image):
    # finds the sample standard deviation of the entire image
    avg = image_average(image, False)
    total_squares = 0
    for pixel in image.generate_each_pixel_in_order():
        total_squares += (pixel['data'] - avg)**2
    variance = total_squares / ((len(image.data.array)*len(image.data.array[0]))-1)
    return variance**0.5

def data_deviation(image):
    # finds the sample standard deviation of pixels identified as data
    avg = image_average(image, True)
    total_squares = 0
    length = 0
    for pixel in image.generate_each_pixel_in_order():
        if pixel['is data']:
            total_squares += (pixel['data'] - avg)**2
            length += 1
        else:
            pass
    variance = total_squares / (length-1)
    return variance**0.5

def std_deviation(image, data):
    if data:
        return data_deviation(image)
    elif not data:
        return all_deviation(image)

# a function that crudely extracts the numeric characters from a string
# and concatenates them before returning an integer
# this is to make sorting work better.

def extract_int(str_num):
    # finds all of the numeric characters and concatenates them, then returns
    # the integer this forms
    outstring = ''
    for char in str_num:
        if char.isnumeric():
            outstring += char

    return int(outstring)

if __name__ == '__main__':

    # get the user to input a filename to save as
    file_name = filedialog.SaveAs()
    filename = file_name.show()
    
    # finding important information for proccessing data
    conf = dso.Config()
    datas = dso.Folder(conf.config_data['Data images'])
    rois = dso.Folder(conf.config_data['ROI images'])
    image_datas = zip(datas.read_in_next_image(), rois.read_in_next_image())

    datapoints = []

    # the actual data processing
    for data, roi in image_datas:
        im = dso.ImageDataPoints(data, roi)

        outputs = {"median" : {'whole' : image_median(im, False), 'data' : image_median(im, True)},
                   "average" : {'whole': image_average(im, False), 'data' : image_average(im, True)},
                   "mode": {'whole': mode(im, False), 'data': mode(im, True)},
                   "standard deviation" : {'whole' : std_deviation(im, False),
                                           'data' : std_deviation(im, True)}
                   }

        datapoints.append([data.name, outputs])

    # sort the information by the number(s) in the filename
    datapoints.sort(key=lambda x: extract_int(x[0]))
    
    # write the information to the filename previously selected by the user
    with open(filename, 'w') as out:

        # go through each image, and write its information to
        # the filename
        for name, data in datapoints:
            out.write('''{0}
Medians

Whole
{1}

Data
{2}

Averages

Whole
{3}

Data
{4}

Modes

Whole
{5}

Data
{6}

Standard Deviations

Whole
{7}

Data
{8}



'''.format(name, data['median']['whole'], data['median']['data'],
              data['average']['whole'], data['average']['data'],
              data['mode']['whole'], data['mode']['data'],
              data['standard deviation']['whole'],
              data['standard deviation']['data']))

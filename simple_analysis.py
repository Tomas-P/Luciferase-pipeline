import data_storing_objects as dso
import json

# just a simple question later
from tkinter import Tk, ttk, StringVar
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

# method for user input
def get_out():
    # gets the user to set the file the output goes to
    root = Tk()
    lab=ttk.Label(root,text="Enter a name for your output without an extension")
    lab.grid(column=0)
    filename = StringVar()
    entry = ttk.Entry(root, textvariable=filename)
    entry.grid(column=1, row=1)
    leave = ttk.Button(root,text="Done", command=root.destroy)
    leave.grid(column=1, row=2)
    root.mainloop()

    # aquire the name it has been set to
    name = filename.get()
    # send said name wherever it needs to go
    return name

if __name__ == '__main__':
    # getting the user input
    outfile = get_out()
    
    # actual data processing
    conf = dso.Config()
    datas = dso.Folder(conf.config_data['Data images'])
    rois = dso.Folder(conf.config_data['ROI images'])
    image_datas = zip(datas.read_in_next_image(), rois.read_in_next_image())

    datapoints = []
    
    for data, roi in image_datas:
        im = dso.ImageDataPoints(data, roi)
        # the reason float() has to be called
        # is because numpy floats are not json-writable
        outputs = {'image name' : str(data.name),"median" : {'whole' : float(image_median(im, False)), 'data' : float(image_median(im, True))},
                   "average" : {'whole': float(image_average(im, False)), 'data' : float(image_average(im, True))},
                   "mode": {'whole': float(mode(im, False)), 'data': float(mode(im, True))},
                   "standard deviation" : {'whole' : float(std_deviation(im, False)),
                                           'data' : float(std_deviation(im, True))}
                   }
        print(outputs)
        datapoints.append(outputs)

    # actually writing the data to the user-requested file
    with open('{0}.json'.format(outfile), 'w') as file_out:
        json.dump(datapoints, file_out)

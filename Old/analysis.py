import lucbase

def image_number(imagename:str)->int:
    """returns the number created by concatinating
    all numeric characters in the imagename, but
    not the characters in the foldername"""
    # check if the imagename uses backslashes for separation
    if imagename.count("\\"):
        # if so, use that to inform which characters are disgarded
        last = imagename.rfind('\\')
        image = imagename[last:]
        numstring = ''
        for char in image:
            if char.isnumeric():
                numstring += char
        return int(numstring)
    # check if the imagename uses forward slashes for separation
    elif imagename.count('/'):
        #if so, use that to inform which characters are disgarded
        last = imagename.rfind('/')
        image = imagename[last:]
        numstring = ''
        for char in image:
            if char.isnumeric():
                numstring += char
        return int(numstring)
    else: # in the case that neither slash is in the imagename
        # inform the user they have given invalid input
        raise Exception("This is not a valid filename!")
    
def make_table(image_function,images:list)->list:
    """(function, list of lucbase.ImageData)->list of int, float
Returns a list showing the image number in the left column and the
output of the function image_function in the right column. The image number
should be the number in the name of the image.Note that the image_function
should be a method of the lucbase.ImageData class"""
    table = []
    for image in images:
        entry = (image_number(image.data_name),image_function(image))
        table.append(entry)
    return table

def image_list(data_folder:lucbase.Folder, roi_folder:lucbase.Folder):
    """yield the next lucbase.ImageData object based on the image number."""
    images = map(lucbase.ImageData,data_folder.next_image(),roi_folder.next_image())
    for image in images:
        yield image

if __name__ == '__main__':
    # checking to see that the functions work
    config = lucbase.Config()
    data = lucbase.Folder(config[lucbase.DATA])
    roi = lucbase.Folder(config[lucbase.ROI])
    images = image_list(data, roi)
    table = make_table(lucbase.ImageData.mean, images)
    print(len(table),'x',len(table[0]))

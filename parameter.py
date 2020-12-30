import enum

class Param(enum.Enum):
    
    # selection of area known to be background ( no blands)
    BACKGROUND = 0
    
    # folder with data images
    DATA = 1
    
    # image used for segmentation
    MASK = 2
    
    # archive of selections used for group definitions
    GROUPING = 3
    
    # whether to generate ROI-plant definitions
    # if not, use pre-existing archive
    GENERATE = 4
    
    # filename of roi archive whether being read from or writ to
    ROI = 5
    
    # whether to normalize the data
    NORM = 6
    
    # time at which the first image was captured
    INIT = 7
    
    # elapsed time between photographs
    ELAPSED = 8

    # folder where output files will be saved
    OUTPUT = 9

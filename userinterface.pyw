# modules from the application
import analysis
import imagej_inteface
import lucbase
import processing
import regionsofinterest as regions

# modules to make a user interface
import tkinter,
import tkinter.ttk as ttk

# the base window
root = tkinter.Tk()

# the first window
# where the user will deide what operations to perform
window1 = tkinter.Toplevel(root)

# tkinter variables to carry information
roi,analyze,process = tkinter.IntVar(),tkinter.IntVar(),tkinter.IntVar()

#check buttons to communicate with the user
find_roi = ttk.Checkbutton(window1,
                           text = "Find the regions of interest",
                           variable = roi)
to_analyze = ttk.Checkbutton(window1,
                             text = "analyze the image data",
                             variable = analyze)
to_process = ttk.Checkbutton(window1,
                             text = "process the images and filter out noise",
                             variable = process)
# an exit button to stop the entire program
halt = ttk.Button(root,
                  text="Halt the program",
                  command = root.destroy)

# a button to tell the program settings are complete
first_step = ttk.Button(window1,
                        text="I'm ready to continue",
                        command = window1.destroy)

# now have window1's event loop run until it is destroyed
# to get the desired information
window1.mainloop()

# it is important that if multiple operations are done,
# they always follow this order
# process -> find rois -> analyze
# in order to prevent errors

# the tkinter variable have to be accessed with a get method
if process.get():
    # run the commands for processing raw images into data images
    pass
if find_roi.get():
    # run the commands for finding the regions of interest in images
    pass
if to_analyze.get():
    # We're going to need more information from the user here
    # what measures do they want to find?
    # do they want to take into account the roi/segmentation images?
    pass

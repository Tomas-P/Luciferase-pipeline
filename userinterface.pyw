# modules from the application
import analysis
import imagej_inteface
import lucbase
import processing
import regionsofinterest as regions

# modules to make a user interface
import tkinter,
import tkinter.ttk as ttk

#use the process class to make the
#final windows be able to be displayed simultaneously
from multiprocessing import Process

# key important information that will be needed many times
config = lucbase.Config()
IMAGEJ = lucbase.Folder(config[lucbase.IMAGEJ])
DATA = lucbase.Folder(config[lucbase.DATA])
ROI = lucbase.Folder(config[lucbase.ROI])
RAW = lucbase.Folder(config[lucbase.RAW])

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

# make sure everything is displayed
find_roi.pack()
to_analyze.pack()
to_process.pack()
halt.pack()
first_step.pack()
# now have window1's event loop run until it is destroyed
# to get the desired information
window1.mainloop()

# it is important that if multiple operations are done,
# they always follow this order
# process -> find rois -> analyze
# in order to prevent errors

# the tkinter variable have to be accessed with a get method
if process.get():

    # ask the user to use the old or new process
    version = tkinter.IntVar()
    pwindow1 = tkinter.Toplevel(root)

    new = ttk.Radiobutton(pwindow1,
                          text="Use the newer processing mechanism",
                          variable=version,
                          value=0)
    old = ttk.Radiobutton(pwindow1,
                          text = "Use the older processing mechanism",
                          variable = version,
                          value=1)
    nextscreen = ttk.Button(pwindow1,
                            command=pwindow1.destroy,
                            text="Next>")
    # make sure everything is displayed
    new.pack()
    old.pack()
    nextscreen.pack()
    pwindow1.mainloop()
    
    if version.get()==0:
        # use the new process
        processing.prep_images(RAW, DATA, IMAGEJ)
    elif version.get()==1:
        # use the old process
        processing.old_process(DATA, IMAGEJ)

# all processing actions are now complete and we can move to finding
# regions of interest
if find_roi.get():
    # luckily for us, the entire process of finding regions of interest
    # is a single function, but the user needs to be made aware they need
    # to wait for a while and then close out ImageJ to continue
    rwindow = tkinter.Toplevel(root)
    message = ttk.Label(rwindow,text="An ImageJ window will now display.Wait for the operations to finish, then close the main ImageJ window")
    ok = ttk.Button(rwindow, text="Ok",command=rwindow.destroy)
    # ensure everything is displayed
    message.pack()
    ok.pack()
    rwindow.mainloop()

    # now find the regions of interest
    regions.segment()

# now that we know we have
# data and regions of interest
# we can now think about how to analyze
# the images
if to_analyze.get():
    # We will need more information from the user
    # Ask them to choose which measures to use
    optionscreen = tkinter.Toplevel(root)
    # use to represent two different approaches to averages
    mean, dmean = tkinter.IntVar(), tkinter.IntVar()
    median, dmedian = tkinter.IntVar(), tkinter.IntVar()
    # all of the things that need to be displayed,displayed
    ttk.Checkbutton(optionscreen,text="use the naive* mean",variable=mean).pack()
    ttk.Checkbutton(optionscreen,text="use the data* mean",variable=dmean).pack()
    ttk.Checkbutton(optionscreen,text="use the naive* median",variable=median).pack()
    ttk.Checkbutton(optionscreen,text="use the data* median",variable=dmedian).pack()
    ttk.Label(optionscreen,text="*naive means that the measurements of the entire images are used").pack()
    ttk.Label(optionscreen,text="*data means measurements are taken with respect to the ROIs").pack()
    ttk.Button(optionscreen,command=optionscreen.destroy,text="Ok").pack()
    # run the window
    optionscreen.mainloop()

    tables = []

    if mean.get():
        mtable = analysis.make_table(lucbase.ImageData.mean,
                                    analysis.image_list(DATA, ROI)
                                    )
        tables.append('mtable')

    if dmean.get():
        dmtable = analysis.make_table(lucbase.ImageData.data_mean,
                                    analysis.image_list(DATA, ROI)
                                    )
        tables.append('dmtable')

    if median.get():
        mediantable = analysis.make_table(lucbase.ImageData.median,
                                    analysis.image_list(DATA, ROI)
                                    )
        tables.append('mediantable')

    if dmedian.get():
        dmediantable = analysis.make_table(lucbase.ImageData.median,
                                    analysis.image_list(DATA, ROI)
                                           )
        tables.append('dmediantable')

    windows = []
    for table in tables:
        windows.append(tkinter.Toplevel(root))
        tbl = eval(table)
        win = windows[-1]
        t = ''
        for row in tbl:
            t = f'{t}{row}\n'

        if table='mtable':
            tkinter.Label(win, text="naive means").pack(side=tkinter.TOP)
        elif table='dmtable':
            tkinter.Label(win,text="data means").pack(side=tkinter.TOP)
        elif table='mediantable':
            tkinter.Label(win,text="naive medians").pack(side=tkinter.TOP)
        elif table='dmediantable':
            tkinter.Label(win, text="data medians").pack(side=tkinter.TOP)
        
        tkinter.Text(win,text=t).pack(fill=tkinter.X)
        tkinter.Button(win,text="Done",command=win.destroy).pack(side=tkinter.BOTTOM)
        Process(target=win.mainloop).start()

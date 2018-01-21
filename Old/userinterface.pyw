# modules from the application
import analysis
import imagej_interface
import lucbase
import processing
import regionsofinterest as regions

# modules to make a user interface
import tkinter
import tkinter.ttk as ttk

# key important information that will be needed many times
config = lucbase.Config()
IMAGEJ = lucbase.Folder(config[lucbase.IMAGEJ])
DATA = lucbase.Folder(config[lucbase.DATA])
ROI = lucbase.Folder(config[lucbase.ROI])
RAW = lucbase.Folder(config[lucbase.RAW])

# the first window
# where the user will deide what operations to perform
window1 = tkinter.Tk()

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


# a button to tell the program settings are complete
first_step = ttk.Button(window1,
                        text="I'm ready to continue",
                        command = window1.destroy)

# make sure everything is displayed
find_roi.pack(fill=tkinter.X)
to_analyze.pack(fill=tkinter.X)
to_process.pack(fill=tkinter.X)
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
    throwaway = tkinter.Tk()
    version = tkinter.IntVar(throwaway)
    throwaway.destroy()
    pwindow1 = tkinter.Tk()

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
if roi.get():
    # luckily for us, the entire process of finding regions of interest
    # is a single function, but the user needs to be made aware they need
    # to wait for a while and then close out ImageJ to continue
    rwindow = tkinter.Tk()
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
if analyze.get():
    # We will need more information from the user
    # Ask them to choose which measures to use
    optionscreen = tkinter.Tk()
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
        tables.append(['mean table',mtable])

    if dmean.get():
        dmtable = analysis.make_table(lucbase.ImageData.data_mean,
                                    analysis.image_list(DATA, ROI)
                                    )
        tables.append(['data mean table',dmtable])

    if median.get():
        mediantable = analysis.make_table(lucbase.ImageData.median,
                                    analysis.image_list(DATA, ROI)
                                    )
        tables.append(['median table',mediantable])

    if dmedian.get():
        dmediantable = analysis.make_table(lucbase.ImageData.median,
                                    analysis.image_list(DATA, ROI)
                                           )
        tables.append(['data median table',dmediantable])

    results = tkinter.Tk()
    windows = []
    for name,table in tables:
        tbl = ''
        for row in table:
            tbl = f'{tbl}{row}\n'
        wn = tkinter.Toplevel(results)
        windows.append(wn)
        ttk.Label(wn,text=name).pack(side=tkinter.TOP,fill=tkinter.X)
        text = tkinter.Text(wn)
        text.insert(tkinter.END, tbl)
        text.pack(fill=tkinter.X)
    ttk.Button(results,text="close windows",command=results.destroy).pack()
    results.mainloop()

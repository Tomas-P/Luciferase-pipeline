from matplotlib import pyplot
from pathlib import Path
from parameter import Param
import numpy

def labels(arguments :dict):
    "set standard labels for axes"
    xlabel = f"Elapsed time since {arguments[Param.INIT]} in hours"
    pyplot.xlabel(xlabel)
    ylabel = "{}relative intensity".format(
                "normalized " if arguments[Param.NORM] else ""
                )
    pyplot.ylabel(ylabel)

def aggregate_group_into_line(affiliation :dict, group):
    target = affiliation[group]
    return target.mean(axis=1)

def summary(arguments :dict, affiliation :dict, background :list, groups :list):
    "graph a summary of the behavior of every group"
    labels(arguments)
    pyplot.title("Summary")
    for i,g in enumerate(groups):
        line = aggregate_group_into_line(affiliation, g)
        xticks = float(arguments[Param.ELAPSED]) * numpy.arange(line.size)
        pyplot.plot(xticks, line, label=f"Group {i}")
    pyplot.plot(background, label="background")
    pyplot.legend()

def grapheachgroup(arguments:dict, affiliation:dict, background:list, groups:list):
    "graph each group in a separate graph"
    for i,g in enumerate(groups):
        points = len(affiliation[g].mean(axis=1))
        xticks = float(arguments[Param.ELAPSED]) * numpy.arange(points)
        pyplot.plot(xticks, affiliation[g])
        pyplot.title(f"Group {i}")
        labels(arguments)
        yield i

def graphalldata(arguments, affiliation, background, groups):
    "graph all the plants all at once"
    pyplot.plot(background, label="background")
    labels(arguments)
    pyplot.title("All plants shown")
    for g in groups:
        points = len(affiliation[g].mean(axis=1))
        xticks = float(arguments[Param.ELAPSED]) * numpy.arange(points)
        pyplot.plot(xticks, affiliation[g])

def savefig(arguments, filename):
    "save a figure then clear the buffer"
    folder = Path(arguments[Param.OUTPUT])
    absolute = folder / filename
    pyplot.savefig(str(absolute))
    pyplot.clf()

def saveall(arguments, affiliation, background, groups):
    "save all of the graphs than can be created from the data set"
    if arguments[Param.OUTPUT] == "":
        return
    summary(arguments, affiliation, background, groups)
    savefig(arguments, "Overview.png")
    for i in grapheachgroup(arguments,affiliation,background,groups):
        savefig(arguments,f"group-{i}-graph.png")
    graphalldata(arguments,affiliation,background,groups)
    savefig(arguments,"AllStacked.png")

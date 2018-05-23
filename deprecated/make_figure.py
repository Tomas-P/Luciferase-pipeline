import align_temporal
from matplotlib import pyplot

def grids():
    'Get the grids using the align_temporal lib'
    name = align_temporal.get_csv_name()
    csv = align_temporal.read_csv(name)
    two_dim = align_temporal.to_two_d(csv)
    means,medians = align_temporal.to_grids(two_dim)
    return means,medians

def graph_means():
    'Display the means of each plant over time.'
    means,medians = grids()
    # no need to transpose here, we do that in align_temporal.py
    pyplot.plot(means)
    pyplot.ylabel("Average Brightness")
    pyplot.xlabel("Time")
    pyplot.title("Average brighness of plants over time")
    pyplot.show()

def graph_medians():
    'Display the medians of each plant over time.'
    means,medians = grids()
    # no need to transpose here, we do that in align_temporal.py
    pyplot.plot(medians)
    pyplot.ylabel("Median Brightness")
    pyplot.xlabel("Time")
    pyplot.title("Median brighness of plants over time")
    pyplot.show()

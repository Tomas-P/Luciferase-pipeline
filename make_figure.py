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
    # My idea of time and pos is transposed from pyplot's idea of time and pos
    pyplot.plot(means.T)
    pyplot.show()

def graph_averages():
    'Display the medians of each plant over time.'
    means,medians = grids()
    # My idea of time and place is transposed from pyplot's idea of time and place
    pyplot.plot(medians.T)
    pyplot.show()

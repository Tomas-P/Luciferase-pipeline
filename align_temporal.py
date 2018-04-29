# Rearrange the .csv from the ImageJ plugin to have the plants
# lined up with their past and future selfs

from tkinter.filedialog import askopenfilename
from pandas import read_csv
from numpy import ndarray

def get_csv_name():
    return askopenfilename(title="Select the csv file with the plant data")

def count_plants(csv):
    for i in range(len(csv)):
        if csv.Slice[i] > 1:
            return i
def to_two_d(csv):
    grid = {}
    for i in range(len(csv)):
        grid.setdefault(i % count_plants(csv),[]).append(csv.iloc[i])
    return grid

def to_grids(grid):
    mean_grid = ndarray((len(grid),len(grid[0])))
    median_grid = ndarray((len(grid),len(grid[0])))

    for i in grid:
        for j,data_pos in enumerate(grid[i]):
            mean_grid[i,j] = data_pos.Mean
            median_grid[i,j] = data_pos.Median

    return mean_grid, median_grid

if __name__ == '__main__':
    name = get_csv_name()
    csv = read_csv(name)
    d2 = to_two_d(csv)
    means,medians = to_grids(d2)

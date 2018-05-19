import align_temporal
from matplotlib import pyplot

def graph(grid):
    pyplot.plot(grid)
    pyplot.show()

def extract_group(grid,lower_bound,upper_bound):
    return grid[...,lower_bound : upper_bound]

def average_group(group):
    return list(
        map(
            lambda timepoint : sum(timepoint) / len(timepoint),
            group
            )
        )

def plot_groups(*groups):
    arglist = []
    for group in groups:
        arglist.append(range(len(group)))
        arglist.append(group)

    pyplot.plot(*arglist)
    pyplot.show()

if __name__ == '__main__':
    CSVNAME = "C:/Users/Tomas/Documents/Tomas_Pipeline_Measurements.csv"

    means,medians = align_temporal.to_grids(
        align_temporal.to_two_d(
            align_temporal.read_csv(
                CSVNAME
                )
            )
        )

    group_1 = extract_group(means,0,50)
    group_2 = extract_group(means,50,100)
    group_3 = extract_group(means,100,150)
    group_4 = extract_group(means,150,200)
    group_5 = extract_group(means,200,250)
    group_6 = extract_group(means,250,300)
    group_7 = extract_group(means,300,350)

    group_1 = average_group(group_1)
    group_2 = average_group(group_2)
    group_3 = average_group(group_3)
    group_4 = average_group(group_4)
    group_5 = average_group(group_5)
    group_6 = average_group(group_6)
    group_7 = average_group(group_7)

    plot_groups(group_1,group_2,group_3,
                group_4,group_5,group_6,
                group_7
                )
    
    

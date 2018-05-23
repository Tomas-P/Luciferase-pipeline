# The main entry point for the whole program
# is this script.

from os import path
import imagej
import make_figure
import choose_rois

use_existing_file = input("use existing csv? [yes/no] ").lower().startswith("y")
use_means = input("use the means? [yes/no]").lower().startswith('y')
number_groups = int(input("how many groups are there? "))

if not use_existing_file:
    plugin = path.abspath('plugin/Tomas_Pipeline.py')
    imagej.run('--run {}'.format(plugin))

means,medians = make_figure.grids()
grid = means if use_means else medians

groups = []
for i in range(number_groups):
    # lower bound
    lb = int(input("group {} lower bound: ".format(i)))
    # upper bound
    ub = int(input("group {} upper bound: ".format(i)))

    group = choose_rois.extract_group(grid,lb,ub)

    group = choose_rois.average_group(group)
    
    groups.append(group)

choose_rois.plot_groups(*groups)


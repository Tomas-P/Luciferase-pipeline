# The main entry point for the whole program
# is this script.

import os
import imagej
import make_figure

graph = input("medians or averages? type m for medians, or a for averages ")
pluginpath = os.path.abspath('plugin/Tomas_Pipeline.py')
imagej.run('--run {}'.format(pluginpath))
if graph.lower().startswith('m'):
    print("you choose the medians!")
    make_figure.graph_medians()
elif graph.lower().startswith('a'):
    print("you choose the averages!")
    make_figure.graph_means()
else:
    print("I don't understand your input")

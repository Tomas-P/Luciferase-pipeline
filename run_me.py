# The main entry point for the whole program
# is this script.

import os
import imagej
import make_figure

def make_graph(graph):
    if graph.lower().startswith('m'):
        print("you choose the medians!")
        make_figure.graph_medians()
    elif graph.lower().startswith('a'):
        print("you choose the averages!")
        make_figure.graph_means()
    else:
        print("I don't understand your input")

graph = input("medians or averages? type m for medians, or a for averages ")
reuse_csv = bool(input("True or False? you have run this at least once before and you want to use an existing .csv file? [True\False]"))

if reuse_csv:
    make_graph(graph)
else:
    pluginpath = os.path.abspath('plugin/Tomas_Pipeline.py')
    imagej.run('--run {}'.format(pluginpath))
    make_graph(graph)

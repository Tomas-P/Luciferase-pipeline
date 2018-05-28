from xml.etree import ElementTree
import subprocess as sub
from graph_data import main
from os.path import abspath
from matplotlib import pyplot

info = ElementTree.parse('info.xml')
imagejfolder = info.findtext('imagej')
sub.run([imagejfolder+'ImageJ-win64.exe','--run',abspath('T_plugin.py')])
main()
pyplot.show()

import sys
script = sys.argv[0]
here = script[:script.rfind('/')]
sys.path.append(here)
import Segment_Algorithms
from constants import CONSTANTS
import json

def get_options():
	options = here + "/config/options.json"
	optfile = open(options)
	options = json.load(optfile)
	optfile.close()
	return options

def main():
	options = get_options()

	if options["selection algorithm"] == CONSTANTS.ARABADOPSIS:
		return Segment_Algorithms.Arabadopsis.main()
	elif options["selection algorithm"] == CONSTANTS.SETARIA:
		return Segment_Algorithms.Setaria.main()
	elif options["selection algorithm"] == CONSTANTS.OTHER:
		return Segment_Algorithms.Other.main()
	elif options["selection algorithm"] == CONSTANTS.SEEDLING:
		return Segment_Algorithms.At_seeds.main()


if script.endswith("segment.py"):
	main()
	print("Segmentation complete, Archive saved")

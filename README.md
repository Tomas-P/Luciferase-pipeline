# Luciferase-pipeline
A repository to store my work on an automated pipeline for analyzing luciferase imaging data using Python and ImageJ

The pipeline processes, measures, and graphs data from luciferase images with minimal user input,
while maintaining the option to manually edit or define regions of interest and region of interest groups.

It is run by running the main.py script in python3.
It is installed by running install.sh (only works on linux like Debian and related projects)

Pipeline strengths:
* all parameters passed at the beginning of the program, requiring minimal to no user input 
* Uses parallelism to run fast and efficiently
* Accurately, precicely, and reproducably produces graphs

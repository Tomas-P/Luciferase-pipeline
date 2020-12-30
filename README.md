# Luciferase-pipeline
An automated pipeline for analyzing arabidopsis luciferase imaging data.

## How to Install

### On Linux
* Download the `install-luc-linux64.sh` script
* run `install-luc-linux64.sh` in bash, e.g. by running `bash install-luc-linux64.sh`
* answer the prompts (one of the steps requires sudo/admin/root privledges)

### On Windows
* Download the `install-luc-win64.ps1` script
* Change the powershell execution policy to allow running scripts, e.g. by running `Set-ExecutionPolicy Bypass` in powershell
* Run `'install-luc-win64.ps1` in PowerShell, e.g. by 
* Answer the prompts (one of the steps requires administrator privledges)

## How to Run

### On Linux
Run the `run.sh` script in bash, e.g. by running `bash run.sh`

### On Windows
Run the `run.ps1` script in powershell

## About

### Capabilities
* Generate ROI objects to measure plants in the data from an image ( the first image is usually very bright relative to the rest of the sequence )
* measure the plant ROI brightness over the sequence of photographs (and therefore over time)
* process the data to (ideally) improve the signal to noise ratio
* correlate plant ROI objects with experimental group ROI objects by position, and use this to organize data by experimental group
* graph accumulated measurements

### Assumptions
* The data is a timelapse/sequence of 16-bit grayscale images 
* the images depict plates of (transgenic) arabidopsis plants that express luciferase production 
  * the plants have access to luciferin substrate (in the water or the growth media)
  * the plants emit an amount of light that is detectable by the camera
  * the only light sources in the images are either the plants themselves or reflections of their light
* the images cotain a region that is recognizably not data
* the plates in the images form one or more distinct experimental groups
* the time between photographs is fixed for the duration of the timelapse/sequence

### Dependencies
* Fiji (ImageJ variant)
* Python 3 (programming language)
* numpy (n-dimensional array mathematic/manipulation library)
* matplotlib (graphing library)
* pyjnius (java to python interoperation library)
* OpenJDK (open-source java development kit)
* venv (virtual environment tool for Python)

### Input Parameters
* folder with sequence of images
* image (used for segmentation: division of image[s] into subject(data) and non-subject(background) zones)
* background (non-data area of image used for comparison, represented as ImageJ ROI object)
* groups (archive(zip file) containing list of areas (represented as ImageJ ROI objects) defining distinct experimental groups)
* whether to load or generate and save plant/data ROI objects
* filename of or for plant/data ROI objects
* whether to normalize the data (by dividing each subject ROI by its own maximum value)
* the time the first photograph was taken
* elapsed time between each photograph being taken

### Output 
* aggregate graph organized by experimental group over time (average brightness on y-axis, elapsed time on x-axis)
* graph of each experimental group over time (individual brightness on y-axis, elapsed time on x-axis)
* graph of all individuals over time (individual brightness on y-axis, elapsed time on x-axis)


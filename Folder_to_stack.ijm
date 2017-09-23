dir = getDirectory("Choose a Directory");
files = getFileList(dir);
for(i=0; i<files.length; i++){
	open(files[i]);
}
run("Images to Stack", "name=exStack title=[] use");
run("Rigid Registration", "initialtransform=[] n=1 tolerance=1.000 level=7 stoplevel=2 materialcenterandbbox=[] template=exStack measure=Euclidean");
run("Subtract Background...", "rolling=50 stack");
setAutoThreshold("Default");
//run("Threshold...");
call("ij.plugin.frame.ThresholdAdjuster.setMode", "B&W");
call("ij.plugin.frame.ThresholdAdjuster.setMode", "Red");
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light calculate");
run("Median...", "radius=2 stack");
run("Gaussian Blur...", "sigma=2 stack");
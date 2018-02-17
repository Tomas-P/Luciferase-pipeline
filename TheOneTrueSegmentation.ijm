run("Set Measurements...", "centroid bounding stack display redirect=None decimal=3");
run("Image Sequence...", "open=C:\\Users\\Tomas\\Documents\\Arabadopsis_images\\data_comparables\\img_000000000_Default_000_adjust.jpg sort");
run("Linear Stack Alignment with SIFT", "initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate");
side=50;
run("Subtract Background...", "rolling=50 stack");
run("Square");
run("Despeckle");
run("Despeckle");
run("Despeckle");
run("Median...", "radius=2");
run("Minimum...", "radius=2");
for(i=0;i<nSlices();i++){
for(x=0;x<getWidth();x=x+side){
	for(y=0;y<getHeight();y=y+side){
		makeRectangle(x,y,side,side);
		sum = 0;
		for(k=x;k<x+side;k++){
			for(j=y;j<y+side;j++){
				pix = getPixel(k,j);
				sum = sum + pix;
			}
		}
		//only use >90% squares
		if(sum>255*side*side*0.9){
			run("Measure");
		}
	}
}
run("Next Slice [>]");
}
saveAs("Results", "C:\\Users\\Tomas\\Desktop\\Results.csv");
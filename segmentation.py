# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 19:42:56 2018

@author: Tomas
"""

from ImageJ_program import ImageJ
import lucbase2 as luc
import numpy as np

def segment1(file:str)->str:
    # returns a string of the form x y value\n
    # where value is 0 if not data and 255 if data.
    macro = '''open('<replace>');
run('Subtract Background...', 'rolling=50 stack');
run('Square');
run('Despeckle');
run('Median...', 'radius=2');
run('Minimum...', 'radius=2');
setThreshold(123, 255);
setOption('BlackBackground',true);
run('Convert to Mask');
for(x=0;x<getWidth();x++){
	for(y=0;y<getHeight();y++){
		pix = getPixel(x,y);
		print(x,y,pix);
	}
}'''.replace('<replace>',file)
    command = '--headless -eval "{}"'.format(macro)
    return ImageJ.run(command)

def getvalues(segment1_out:str):
    values = []
    segment = segment1_out.strip('\r')
    rows = [item for item in segment.split('\n') if item!='']
    for row in rows:
        items = row.split(' ')
        x, y, val = items
        x = int(x)
        y = int(y)
        val = int(val)
        values.append((x,y,val))
    return values

def to_array(getvalues_out:list)->np.ndarray:
    width = max(map(lambda iterable: iterable[0], getvalues_out)) 
    height = max(map(lambda iterable: iterable[1], getvalues_out))
    array = np.empty((width+1,height+1),dtype=int)
    for x,y,val in getvalues_out:
        array[y][x] = val
        # this looks wrong but it makes sure the image is rotated the right way

    return array
        
if __name__ == '__main__':
    file = "C:\\\\Users\\\\Tomas\\\\Documents\\\\Arabadopsis_images\\\\data_comparables\\\\img_000000001_Default_000_adjust.jpg"
    s = segment1(file)
    out = s.stdout.decode()
    vals = getvalues(out)
    arr = to_array(vals)
    from PIL import Image
    im =Image.fromarray(arr)
    im.show()

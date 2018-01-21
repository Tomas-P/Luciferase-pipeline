# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 18:40:48 2018

@author: Tomas
"""

def simple_segment_macro(filename,side_length,data_percent_threshold):
    macro_lines = [
        "open('{file}');", #run str.format() at some point
        "run('Square');",
        "for(i=0;i<4;i++){run('Despeckle');}",
        "setThreshold(200,255);",
        "run('Make Binary');",
        "height = getHeight();",
        "width = getWidth();",
        "side = {side};",
        "thresh = {thresh};",
        "for(a=0;a<height/side;a++){for(b=0;b<width/side;b++){left=b*side;right=left+side;top=a*side;bottom=top+side;data=0;<>}}".replace(
                '<>',"for(c=left;c<right;c++){for(d=top;d<bottom;d++){if(getPixel(c,d)==255){data++;}}}if(data>thresh*side*side){print('top',top,'bottom',bottom,'left',left,'right',right);}")
        ]
    macro_lines[0] = macro_lines[0].format(file=filename)
    macro_lines[7] = macro_lines[7].format(side=side_length)
    macro_lines[8] = macro_lines[8].format(thresh=data_percent_threshold)
    return ''.join(macro_lines)
#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal

import numpy as np
import time

from os import walk
import sys


keep_running = True

basedirectory = sys.argv[1]

def get_depth(name):
    print '%sdepth/%s'%(basedirectory,name)
    data = np.load('%sdepth/%s'%(basedirectory,name))
    
    return {'pretty':frame_convert.pretty_depth(data),'raw':data}



def get_video(name):
    name = 'C%s'%name[1:]
    print '%scolour/%s'%(basedirectory,name)
    data = np.load('%scolour/%s'%(basedirectory,name))
    
    return data



def do_display(filenames):
    filenames.sort()
    mp.ion()
    mp.gray()
    mp.figure(1)
    depth  = get_depth(f[0])
    image_depth = mp.imshow(depth['pretty'], interpolation='nearest', animated=True)
    mp.figure(2)
    
    image_rgb = mp.imshow(get_video(f[0]), interpolation='nearest', animated=True)
    print('Press Ctrl-C in terminal to stop')

    
    
    for filename in filenames:
        mp.figure(1)
        depth  = get_depth(filename)
        image_depth.set_data(depth['pretty'])
        mp.figure(2)
        colour_image = get_video(filename)
        image_rgb.set_data(colour_image)
        mp.draw()
        mp.waitforbuttonpress(0.01)
        time.sleep(0.1)


f = []
for (dirpath, dirnames, filenames) in walk('%s/depth/'%sys.argv[1]):
    
    f.extend(filenames)
    break

do_display(f)

#!/usr/bin/env python
import freenect
import cv
import frame_convert
import numpy as np

'''
args
directory holding valid depth and colour directories from sync save

will replay files from directory


'''

threshold = 100
current_depth = 130

import numpy as np
import time

from os import walk
import sys


keep_running = True

basedirectory = sys.argv[1]


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_depth(name):
    global threshold
    global current_depth
    
    data = np.load('%sdepth/%s'%(basedirectory,name))
    depth = data
    depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
    depth = depth.astype(np.uint8)
    image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                                 cv.IPL_DEPTH_8U,
                                 1)
    cv.SetData(image, depth.tostring(),
               depth.dtype.itemsize * depth.shape[1])
    cv.ShowImage('Depth', image)
    cv.WaitKey(10) #otherwise windows don't refresh


def show_video(name):
    name = 'C%s'%name[1:] # Change name from D... to C...
    data = np.load('%scolour/%s'%(basedirectory,name))
    cv.ShowImage('Video', frame_convert.video_cv(data))


cv.NamedWindow('Depth')
cv.NamedWindow('Video')
cv.CreateTrackbar('threshold', 'Depth', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Depth', current_depth, 2048, change_depth)

print('Press ESC in window to stop')



depthnames = []
for (dirpath, dirnames, filenames) in walk('%s/depth/'%sys.argv[1]):
    depthnames.extend(filenames)
    break
    
for filename in depthnames:
    print 'Replaying --> %s'%filename
    show_depth(filename)
    show_video(filename)
    time.sleep(0.1)
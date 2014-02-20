#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal

import numpy as np

keep_running = True


def get_depth():
    data = freenect.sync_get_depth()[0]
    print type(data)
    return {'pretty':frame_convert.pretty_depth(data),'raw':data}



def get_video():
    data = freenect.sync_get_video()[0]
    print type(data)
    return data


def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False


mp.ion()
mp.gray()
mp.figure(1)
depth  = get_depth()

image_depth = mp.imshow(depth['pretty'], interpolation='nearest', animated=True)
mp.figure(2)
image_rgb = mp.imshow(get_video(), interpolation='nearest', animated=True)
print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)

import os
import time
now = int(time.time())
directory = '../scans/scan_%d'%now
if not os.path.exists(directory):
    os.makedirs(directory)

depth_directory = '../scans/scan_%d/depth'%now
if not os.path.exists(depth_directory):
    os.makedirs(depth_directory)
    
colour_directory = '../scans/scan_%d/colour'%now
if not os.path.exists(colour_directory):
    os.makedirs(colour_directory)
    
    
print 'Making %s'%directory

while keep_running:
    mp.figure(1)
    depth  = get_depth()
    image_depth.set_data(depth['pretty'])
    mp.figure(2)
    colour_image = get_video()
    image_rgb.set_data(colour_image)
    mp.draw()
    t = time.time()
    fname = '%s/D%s.nparray'%(depth_directory,t)
    np.save(fname, depth['raw'])
    fname = '%s/C%s.nparray'%(colour_directory,t)
    np.save(fname, colour_image)
    print "Writing %s"%fname
    mp.waitforbuttonpress(0.01)

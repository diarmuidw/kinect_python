#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import signal
import frame_convert
import math
import numpy as np
mp.ion()
image_rgb = None
image_depth = None
keep_running = True

filenum = 0
minDistance = -10
scaleFactor = 0.0021

def savedepth(depth):
    global filenum
    fname = '/tmp/N%s.ply'%filenum
    #filenum = filenum +1
    print 'Generating cloud file %s...\n'%fname
    step = 1
    fc = open(fname, 'wt')
    fc.write('ply\n')
    fc.write('format ascii 1.0\n')
    fc.write('comment : created from Kinect depth image\n')
    numelements = 0
    fc.write('element vertex %s\n' %numelements )
    fc.write('property float x\n')
    fc.write('property float y\n')
    fc.write('property float z\n')
    fc.write('end_header\n')
    #depth.resize(480,640)

    # Convert from pixel ref (i, j, z) to 3D space (x,y,z)
    for i in range(0,480,step):
        for j in range(0,640,step):
            z = depth[i][j]
            if z > 0:
                x = (i - 480 / 2) * (z + minDistance) * scaleFactor
                y = (640 / 2 - j) * (z + minDistance) * scaleFactor
                fc.write("%f  %f  %f\n" % (x, y, z))
                numelements = numelements +1
    fc.write('element vertex %s\n' %numelements )
    fc.close
    print 'Done'


def display_depth(data):
    global image_depth
    global filenum
    filenum = filenum+1
    #print data.shape
    '''
    print type(data)
    print 100.0/(-0.00307 * data[240,320] + 3.33)
    print 0.1236 * math.tan(data[240,320] / 2842.5 + 1.1863)
    print data[240,320]
    print '-------'
    '''
    depth = 100/(-0.00307*data + 3.33)
    savedepth(depth)
    data = frame_convert.pretty_depth(data)
    
    mp.gray()
    mp.figure(1)
    if image_depth:
        image_depth.set_data(data)
    else:
        image_depth = mp.imshow(data, interpolation='nearest', animated=True)
    mp.draw()

data = np.load('/tmp/E2.nparray.npy')
display_depth(data)

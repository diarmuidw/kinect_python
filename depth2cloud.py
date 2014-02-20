# depth2cloud.py  - convert Kinect depth image into 3D point cloud, in PLY format
# Ben Bongalon (ben@borglabs.com)
#  @ TODO: 
#    - change to GPL
#    - save in binary PLY format   


import sys
from pylab import *

minDistance = -10
scaleFactor = 0.0021


def usage():
  print '\ndepth2cloud  <img_file> <cloud_file>\n'
  exit(0)

  
if len(sys.argv) != 3:
  usage()
imgfile = sys.argv[1]
cloudfile = sys.argv[2]
print 'Reading binary image...\n'
raw = fromfile(imgfile, 'H')

print 'Generating cloud file...\n'
fc = open(cloudfile, 'wt')
fc.write('ply\n')
fc.write('format ascii 1.0\n')
fc.write('comment : created from Kinect depth image\n')
fc.write('element vertex %d\n' % len(raw))
fc.write('property float x\n')
fc.write('property float y\n')
fc.write('property float z\n')
fc.write('end_header\n')

# Compute depth (unit in cm) from raw 11-bit disparity value
# According to ROS site
depth = 100/(-0.00307*raw + 3.33)
depth.resize(480,640)

# Convert from pixel ref (i, j, z) to 3D space (x,y,z)
for i in range(480):
    for j in range(640):
        z = depth[i][j]
        x = (i - 480 / 2) * (z + minDistance) * scaleFactor
        y = (640 / 2 - j) * (z + minDistance) * scaleFactor
        fc.write("%f  %f  %f\n" % (x, y, z))
        
fc.close
print 'Done!'


import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy
import os
import platform
import glob

# Display defaults
matplotlib.style.use('ggplot')  # Use ggplot style for plots
plt.rc('image', cmap='gray', interpolation='nearest')  # Display all images the same way
plt.rcParams['figure.figsize'] = (16 * 0.8, 9 * 0.8)  # Display images in this size
plt.rc('lines', linewidth=2)  # Make lines a bit wider
plt.rc('lines', marker='o')  # Always with line markers
# Colors from http://tools.medialab.sciences-po.fr/iwanthue/
colors = ["#CC5B9B", "#6FAB4C", "#7889C6", "#CC6D39"]

# Functions
def read_gray(filename, width=1280, height=4*1024):
    '''Read a .gray image from the detector to a numpy array, ready to display'''
    image = numpy.fromfile(filename, dtype=numpy.int16).reshape(height, width)
    return image

def reslice_image(inputimagename, ImageWidth=1280, ImageHeight=4*1024, read=True):
    '''Display 4sensor image in "human-readable" format'''
    if read:
        # Read the image from disk
        img = read_gray(inputimagename, width=ImageWidth, height=ImageHeight)
    else:
        # We already have an image, just reslice it
        img = inputimagename
    # Split into top and bottom, which we concatenate afterwards
    bottom = numpy.concatenate((img[0 * ImageHeight / 4:(0 + 1) * ImageHeight / 4, :],
                                img[1 * ImageHeight / 4:(1 + 1) * ImageHeight / 4, :]),
                               axis=1)
    top = numpy.concatenate((img[2 * ImageHeight / 4:(2 + 1) * ImageHeight / 4, :],
                             img[3 * ImageHeight / 4:(3 + 1) * ImageHeight / 4, :]),
                            axis=1)
    concatenate = numpy.concatenate((top, bottom), axis=0)
    return concatenate

StartPath = '/afs/psi.ch/project/EssentialMed/Images/detector2/leadglass'
Folders = glob.glob(os.path.join(StartPath, '*gkt_gkt_*_*'))

plt.ion()
for c,i in enumerate(Folders[:3]):
    print 80* '-'
    print Folders[c]
    plt.figure(c)
    ImageNames = glob.glob(os.path.join(i, '*.gray'))
    Proj = reslice_image(ImageNames[0])
    Dark = reslice_image(ImageNames[1])
    Corrected = numpy.subtract(Proj, Dark)
    print 'Projection image min: %0.2f, mean: %0.2f, max: %0.2f' % (numpy.min(Proj), numpy.mean(Proj), numpy.max(Proj))
    print 'Dark image min: %0.2f, mean: %0.2f, max: %0.2f' % (numpy.min(Dark), numpy.mean(Dark), numpy.max(Dark))
    print 'Corrected image min: %0.2f, mean: %0.2f, max: %0.2f' % (numpy.min(Corrected), numpy.mean(Corrected), numpy.max(Corrected))
    plt.subplot(231)
    plt.imshow(Proj)
    plt.subplot(232)
    plt.imshow(Dark)
    plt.subplot(233)
    plt.imshow(Corrected,clim=(0, 500))

    plt.subplot(235)
    plt.hist(Proj.ravel(), bins=32)
    plt.xlim([0,1024])
    plt.subplot(234)
    plt.hist(Dark.ravel(), bins=32)
    plt.xlim([0,1024])
    plt.subplot(236)
    plt.hist(Corrected.ravel(), bins=32)
    plt.xlim([0,1024])

    plt.suptitle(Folders[c])
    plt.draw()
    plt.pause(0.001)
plt.ioff()
plt.show()


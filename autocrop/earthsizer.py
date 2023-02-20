import glob
import os.path
import json
import datetime
import requests
import io
from urllib.request import urlopen
import time
import math  
import numpy  
from matplotlib import pyplot as plt

from PIL import Image, ImageFilter

def determine_earth_pixelsize(image):
    with Image.open(image) as im:
        im = im.convert("1")
        im = im.filter(ImageFilter.SMOOTH_MORE)
        data = numpy.asarray(im)
        graph = []
        for i in range(len(data)):
            count = numpy.count_nonzero(data[i] == True)
            graph.append(count)
        #im.show()
        size = numpy.array(graph).max()
        print('{};{}'.format(os.path.basename(image),size))

scanpath = r'year/*.jpg'
files = sorted(glob.glob(scanpath))
for f in files:
    determine_earth_pixelsize(f)

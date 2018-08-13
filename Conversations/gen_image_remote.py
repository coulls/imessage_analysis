#!/usr/bin/python

import sys
import numpy as np
import os
from PIL import Image
from config import CONVO_CODE

image_string = "%s/temp.png" % (CONVO_CODE)

size = int(sys.argv[1])
pix_array = []
for k in range(size):
    for l in range(size):
        pix_array.append(tuple(np.random.random_integers(0,255,4)))
im = Image.new("RGBA", (size,size))
im.putdata(pix_array)
im.save(image_string, "PNG")

size = str(size).zfill(4)

print os.stat("%s/temp.png" % (CONVO_CODE)).st_size

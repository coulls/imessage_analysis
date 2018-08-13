#!/usr/bin/python

import sys
import subprocess
import shlex
import time
import signal
import numpy as np
import os
from PIL import Image
from config import OSX_OUT_DATA, OSX_OUT_CODE

image_string = "./temp.png"

wait_times = [7, 8, 9, 10]
sizes = [64, 128, 256, 512]

trials = range(250)

for i in trials:
    for j in range(len(sizes)):
        size = sizes[j]
        pix_array = []
        for k in range(size):
            for l in range(size):
                pix_array.append(tuple(np.random.random_integers(0,255,4)))
        im = Image.new("RGBA", (size,size))
        im.putdata(pix_array)
        im.save(image_string, "PNG")

        size = str(size).zfill(4)
    
        pic_capture_string = "%s/image/data_%s/%d.pcap" % (OSX_OUT_DATA,size,i)

        try:
            os.remove(len_capture_string)
        except:
            pass

        f_idx = open("%s/image/data_%s/index.txt" % (OSX_OUT_DATA,size), "a")
        f_idx.write("%d,%d\n" % (i, os.stat("temp.png").st_size))
        f_idx.close()

        filter_string = "(tcp port 443 or tcp port 5223) and (net 17.0.0.0/8 or net 137.0.0.0/8)"
            
        #Run applescript and finish
        applescript_cmd = "osascript paste_image.scpt %s" % (image_string)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(10)

        #Open tcpdump and sleep
        tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (pic_capture_string, filter_string)
        tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
        time.sleep(1)

        applescript_cmd = "osascript enter_letter.scpt"
        subprocess.call(shlex.split(applescript_cmd))
        
        time.sleep(wait_times[j])
    
        #tcpdump_proc.terminate()
        tcpdump_proc.send_signal(signal.SIGINT)
        time.sleep(1)
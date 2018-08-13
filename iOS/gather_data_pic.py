#!/usr/bin/python

import sys
import subprocess
import shlex
import time
import signal
import numpy as np
import os
from PIL import Image
from config import iOS_SEND_DATA, iOS_RECV_DATA

image_string = "./temp.png"

sizes = [64, 128, 256]
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
    
        pic_capture_string_out = "%s/image/data_%s/%d.pcap" % (iOS_SEND_DATA,size,i)
        try:
            os.remove(len_capture_string_out)
        except:
            pass

        pic_capture_string_in = "%s/image/data_%s/%d.pcap" % (iOS_RECV_DATA,size,i)
        try:
            os.remove(len_capture_string_in)
        except:
            pass

        f_idx_out = open("%s/image/data_%s/index.txt" % (iOS_SEND_DATA,size), "a")
        f_idx_out.write("%d,%d\n" % (i, os.stat("temp.png").st_size))
        f_idx_out.close()

        f_idx_in = open("%s/image/data_%s/index.txt" % (iOS_RECV_DATA,size), "a")
        f_idx_in.write("%d,%d\n" % (i, os.stat("temp.png").st_size))
        f_idx_in.close()

        filter_string = "(tcp port 443 or tcp port 5223 or tcp port 80) and (net 17.0.0.0/8 or net 137.0.0.0/8)"
            
        #Run applescript and finish
        applescript_cmd = "osascript click_image_paste.scpt %s" % (image_string)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(5)

        #Open tcpdump and sleep
        tcpdump_cmd_out = "tcpdump -i rvi0 -w %s %s" % (pic_capture_string_out, filter_string)
        tcpdump_proc_out = subprocess.Popen(shlex.split(tcpdump_cmd_out))
        time.sleep(1)

        #Open tcpdump and sleep
        tcpdump_cmd_in = "tcpdump -i en1 -w %s %s" % (pic_capture_string_in, filter_string)
        tcpdump_proc_in = subprocess.Popen(shlex.split(tcpdump_cmd_in))
        time.sleep(1)

        applescript_cmd = "osascript click_image_send.scpt"
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(20)

        #tcpdump_proc.terminate()
        tcpdump_proc_out.send_signal(signal.SIGINT)
        time.sleep(1)
    
        tcpdump_proc_in.send_signal(signal.SIGINT)
        time.sleep(1)
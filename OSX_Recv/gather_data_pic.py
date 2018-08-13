#!/usr/bin/python

import sys
import subprocess
import shlex
import time
import signal
import os
from config import OSX_RECV_DATA, OSX_RECV_CODE

wait_times = [8, 9, 10]
sizes = [64, 128, 256]

image_string = "%s/temp.png" % (OSX_RECV_CODE)

trials = range(250)

for i in trials:
    for j in range(len(sizes)):
        size = sizes[j]
        
        gen_pic_cmd = "ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \"/opt/local/bin/python %s/generate_pic.py %d\"" % (OSX_RECV_CODE,size)
        file_size = subprocess.check_output(shlex.split(gen_pic_cmd))
        
        size = str(size).zfill(4)
    
        pic_capture_string = "%s/image/data_%s/%d.pcap" % (OSX_RECV_DATA,size,i)

        try:
            os.remove(len_capture_string)
        except:
            pass

        f_idx = open("%s/image/data_%s/index.txt" % (OSX_RECV_DATA,size), "a")
        f_idx.write("%d,%s\n" % (i, file_size))
        f_idx.close()

        filter_string = "(tcp port 443 or tcp port 5223 or tcp port 80) and (net 17.0.0.0/8 or net 137.0.0.0/8)"

        #Run applescript and finish
        applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \"osascript %s/paste_image.scpt %s\"" % (OSX_RECV_CODE,image_string)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(4)

        #Open tcpdump and sleep
        tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (pic_capture_string, filter_string)
        tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
        time.sleep(1)

        applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \"osascript %s/enter_letter.scpt\"" % (OSX_RECV_CODE)
        subprocess.call(shlex.split(applescript_cmd))
        
        time.sleep(wait_times[j])
    
        tcpdump_proc.send_signal(signal.SIGINT)
        time.sleep(1)


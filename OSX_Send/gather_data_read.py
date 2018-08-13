#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
from config import OSX_RECV_DATA, OSX_RECV_CODE

random.seed()

test_chars = list(string.digits)
test_chars.extend(string.letters)

lengths = [8]
trials = range(250)

for i in trials:
    for j in lengths:
        char = "".join(random.choice(test_chars) for k in range(j))
        j = str(j).zfill(3)

        len_capture_string = "%s/other/data_read/%d.pcap" % (OSX_RECV_DATA,i)
        try:
            os.remove(len_capture_string)
        except:
            pass

        filter_string = "tcp port 5223 and net 17.0.0.0/8"


        #Run applescript and finish
        applescript_cmd = "osascript type_letter.scpt %s" % (char)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(1)
    
        applescript_cmd = "osascript enter_letter.scpt"
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(4)
    
        #Open tcpdump and sleep
        tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (len_capture_string, filter_string)
        tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
        time.sleep(2)

        applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \"osascript %s/change_focus.scpt\"" % (OSX_RECV_CODE)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(5)

        #tcpdump_proc.terminate()
        tcpdump_proc.send_signal(signal.SIGINT)
        time.sleep(1)
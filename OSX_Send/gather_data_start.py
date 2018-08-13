#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
from config import OSX_OUT_DATA, OSX_OUT_CODE

random.seed()

test_chars = list(string.digits)
test_chars.extend(string.letters)


for i in range(250):
    char = "".join(random.choice(test_chars) for j in range(100))

    start_capture_string = "%s/other/data_start/%d.pcap" % (OSX_OUT_DATA,i)
    try:
        os.remove(start_capture_string)
    except:
        pass

    stop_capture_string = "%s/other/data_stop/%d.pcap" % (OSX_OUT_DATA,i)
    try:
        os.remove(stop_capture_string)
    except:
        pass

    filter_string = "tcp port 5223 and net 17.0.0.0/8"

    #Open tcpdump and sleep
    tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (start_capture_string, filter_string)
    tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
    time.sleep(1)

    #Run applescript and finish
    applescript_cmd = "osascript type_letter.scpt %s" % (char)
    subprocess.call(shlex.split(applescript_cmd))

    time.sleep(3)
    #tcpdump_proc.terminate()
    tcpdump_proc.send_signal(signal.SIGINT)

    time.sleep(1)

    #Open tcpdump and sleep
    tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (stop_capture_string, filter_string)
    tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
    time.sleep(2)

    #Run applescript and finish
    applescript_cmd = "osascript del_letter.scpt 100"
    subprocess.call(shlex.split(applescript_cmd))

    time.sleep(4)
    #tcpdump_proc.terminate()
    tcpdump_proc.send_signal(signal.SIGINT)

    #Wait then close tcmpdump
    time.sleep(1)

#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
import os
from config import iOS_SEND_DATA, iOS_RECV_DATA

random.seed()

test_chars = list(string.digits)
test_chars.extend(string.letters)

lengths = [8,16,32,64,128]
trials = range(0,250)

for i in trials:
    for j in lengths:
        char = "".join(random.choice(test_chars) for k in range(j))
        j = str(j).zfill(3)

        len_capture_string_send = "%s/text/data_%s/%d.pcap" % (iOS_SEND_DATA,j,i)
        try:
            os.remove(len_capture_string_send)
        except:
            pass

        len_capture_string_recv = "%s/text/data_%s/%d.pcap" % (iOS_RECV_DATA,j,i)
        try:
            os.remove(len_capture_string_in)
        except:
            pass

        filter_string = "tcp port 5223 and net 17.0.0.0/8"

        #Open tcpdump and sleep
        tcpdump_cmd_send = "tcpdump -i rvi0 -w %s %s" % (len_capture_string_send, filter_string)
        tcpdump_proc_send = subprocess.Popen(shlex.split(tcpdump_cmd_send))
        time.sleep(1)

        #Open tcpdump and sleep
        tcpdump_cmd_recv = "tcpdump -i en1 -w %s %s" % (len_capture_string_recv, filter_string)
        tcpdump_proc_recv = subprocess.Popen(shlex.split(tcpdump_cmd_recv))
        time.sleep(1)

        #Run applescript and finish
        applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa mobile@192.168.1.5 \" \
            /Applications/biteSMS.app/biteSMS -send -iMessage scott.coull@gmail.com '%s'\"" % (char)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(10)

        #tcpdump_proc.terminate()
        tcpdump_proc_send.send_signal(signal.SIGINT)
        time.sleep(1)
        tcpdump_proc_recv.send_signal(signal.SIGINT)
        time.sleep(1)
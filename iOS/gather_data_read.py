#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
import os
from config import iOS_RECV_DATA, iOS_SEND_DATA

random.seed()

test_chars = list(string.digits)
test_chars.extend(string.letters)

lengths = [8]

trials = range(0,250)

for i in trials:
    for j in lengths:
        char = "".join(random.choice(test_chars) for k in range(j))
        j = str(j).zfill(8)

        len_capture_string_recv = "%s/other/data_read/%d.pcap" % (iOS_RECV_DATA,i)
        try:
            os.remove(len_capture_string_out)
        except:
            pass

        len_capture_string_send = "%s/other/data_read/%d.pcap" % (iOS_SEND_DATA,i)
        try:
            os.remove(len_capture_string_in)
        except:
            pass

        filter_string = "tcp port 5223 and net 17.0.0.0/8"


        #Run applescript and finish
        applescript_cmd = "osascript type_letter_messages.scpt %s" % (char)
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(1)

        applescript_cmd = "osascript enter_letter.scpt"
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(5)

        #Open tcpdump and sleep
        tcpdump_cmd_recv = "tcpdump -i rvi0 -w %s %s" % (len_capture_string_recv, filter_string)
        tcpdump_proc_recv = subprocess.Popen(shlex.split(tcpdump_cmd_recv))
        time.sleep(1)

        #Open tcpdump and sleep
        tcpdump_cmd_send = "tcpdump -i en1 -w %s %s" % (len_capture_string_send, filter_string)
        tcpdump_proc_send = subprocess.Popen(shlex.split(tcpdump_cmd_send))
        time.sleep(1)

        applescript_cmd = "osascript click_screen_start.scpt"
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(5)

        #tcpdump_proc.terminate()
        tcpdump_proc_recv.send_signal(signal.SIGINT)
        time.sleep(1)
        tcpdump_proc_send.send_signal(signal.SIGINT)
        time.sleep(1)

        applescript_cmd = "osascript click_screen_stop.scpt"
        subprocess.call(shlex.split(applescript_cmd))
        time.sleep(1)
        
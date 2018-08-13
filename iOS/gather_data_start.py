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


for i in range(241,250):
    char = "".join(random.choice(test_chars) for j in range(10))

    start_capture_string_out = "%s/other/data_start/%d.pcap" % (iOS_SEND_DATA,i)
    try:
        os.remove(start_capture_string_out)
    except:
        pass

    stop_capture_string_out = "%s/other/data_stop/%d.pcap" % (iOS_SEND_DATA,i)
    try:
        os.remove(stop_capture_string_out)
    except:
        pass

    start_capture_string_in = "%s/other/data_start/%d.pcap" % (iOS_RECV_DATA,i)
    try:
        os.remove(start_capture_string_in)
    except:
        pass

    stop_capture_string_in = "%s/other/data_stop/%d.pcap" % (iOS_RECV_DATA,i)
    try:
        os.remove(stop_capture_string_in)
    except:
        pass

    filter_string = "tcp port 5223 and net 17.0.0.0/8"

    #Open tcpdump and sleep
    tcpdump_cmd_out = "tcpdump -i rvi0 -w %s %s" % (start_capture_string_out, filter_string)
    tcpdump_proc_out = subprocess.Popen(shlex.split(tcpdump_cmd_out))
    time.sleep(1)

    #Open tcpdump and sleep
    tcpdump_cmd_in = "tcpdump -i en1 -w %s %s" % (start_capture_string_in, filter_string)
    tcpdump_proc_in = subprocess.Popen(shlex.split(tcpdump_cmd_in))
    time.sleep(1)

    #Run applescript and finish
    applescript_cmd = "osascript type_letter_screen.scpt %s" % (char)
    subprocess.call(shlex.split(applescript_cmd))
    time.sleep(3)

    #tcpdump_proc.terminate()
    tcpdump_proc_out.send_signal(signal.SIGINT)
    time.sleep(1)
    tcpdump_proc_in.send_signal(signal.SIGINT)
    time.sleep(1)


    #Open tcpdump and sleep
    tcpdump_cmd_out = "tcpdump -i rvi0 -w %s %s" % (stop_capture_string_out, filter_string)
    tcpdump_proc_out = subprocess.Popen(shlex.split(tcpdump_cmd_out))
    time.sleep(1)

    #Open tcpdump and sleep
    tcpdump_cmd_in = "tcpdump -i en1 -w %s %s" % (stop_capture_string_in, filter_string)
    tcpdump_proc_in = subprocess.Popen(shlex.split(tcpdump_cmd_in))
    time.sleep(1)

    #Run applescript and finish
    applescript_cmd = "osascript del_letter.scpt 10"
    subprocess.call(shlex.split(applescript_cmd))
    time.sleep(3)

    #tcpdump_proc.terminate()
    tcpdump_proc_out.send_signal(signal.SIGINT)
    time.sleep(1)
    tcpdump_proc_in.send_signal(signal.SIGINT)
    time.sleep(1)

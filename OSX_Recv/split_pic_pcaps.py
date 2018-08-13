#!/usr/bin/python

import sys
import glob
import os
import subprocess
import shlex
from config import OSX_RECV_DATA

for file_name in glob.glob("%s/%s/data_*/*.pcap" % (OSX_RECV_DATA, sys.argv[1])):
    toks = os.path.split(file_name)
    idx = toks[0].split("_")[-1]
    
    #tcpdump for apple/ms tls and aps
    new_file = "%s/%s-apple-tls/data_%s/%s" % (OSX_RECV_DATA, sys.argv[1], idx, toks[1])
    try:
        os.remove(new_file)
    except:
        pass
    subprocess.call(shlex.split("tcpdump -r %s -w %s port 443 and net 17.0.0.0/8" % (file_name, new_file)))

    new_file = "%s/%s-ms-http/data_%s/%s" % (OSX_RECV_DATA, sys.argv[1], idx, toks[1])
    try:
        os.remove(new_file)
    except:
        pass
    subprocess.call(shlex.split("tcpdump -r %s -w %s port 80 and net 137.0.0.0/8" % (file_name, new_file)))

    new_file = "%s/%s-aps/data_%s/%s" % (OSX_RECV_DATA,sys.argv[1], idx, toks[1])
    try:
        os.remove(new_file)
    except:
        pass
    subprocess.call(shlex.split("tcpdump -r %s -w %s port 5223 and net 17.0.0.0/8" % (file_name, new_file)))
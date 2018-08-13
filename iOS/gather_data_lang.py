#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
import re
import os
from config import iOS_RECV_DATA, iOS_SEND_DATA

random.seed()

digits_test = re.compile('\d | \" | \'')

langs = ['chinese','english','spanish','french','german','russian']
grams = ['n']

trials = range(0,250)

for lang in langs:
    for gram in grams:
        f = open("%s/%s/%sgram.txt" % (iOS_SEND_DATA,lang, str(gram)))
        lines = f.readlines()
        f.close()
        
        #Captures both directions simultaneously using the built in iPhone/iPad interfaces and wireless.
        f_idx_out = open("%s/%s/data_%sgram/index.txt" % (iOS_SEND_DATA,lang,str(gram)), "a")
        f_idx_in = open("%s/%s/data_%sgram/index.txt" % (iOS_RECV_DATA,lang,str(gram)), "a")
        
        for i in trials:
            char = random.choice(lines)
            char = char.strip().split(",")[0]
            while digits_test.search(char) != None:
                char = random.choice(lines)
                char = char.strip().split(",")[0]
            char = char.replace('"', '')
            char = char.replace("'","")        
        

            f_idx_out.write("%d,%s\n" % (i, char))
            f_idx_in.write("%d,%s\n" % (i, char))
            f_idx_out.flush()
            f_idx_in.flush()
        
            lang_capture_string_out = "%s/%s/data_%sgram/%d.pcap" % (iOS_SEND_DATA,lang, str(gram), i)
            try:
                os.remove(lang_capture_string_out)
            except:
                pass

            lang_capture_string_in = "%s/%s/data_%sgram/%d.pcap" % (iOS_RECV_DATA,lang, str(gram), i)
            try:
                os.remove(lang_capture_string_in)
            except:
                pass
    
            filter_string = "tcp port 5223 and net 17.0.0.0/8"


            #Open tcpdump and sleep
            tcpdump_cmd_out = "tcpdump -i rvi0 -w %s %s" % (lang_capture_string_out, filter_string)
            tcpdump_proc_out = subprocess.Popen(shlex.split(tcpdump_cmd_out))
            time.sleep(1)
    
            #Open tcpdump and sleep
            tcpdump_cmd_in = "tcpdump -i en1 -w %s %s" % (lang_capture_string_in, filter_string)
            tcpdump_proc_in = subprocess.Popen(shlex.split(tcpdump_cmd_in))
            time.sleep(1)
    
            #Run applescript and finish
            applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa mobile@192.168.1.5 \" \
                /Applications/biteSMS.app/biteSMS -send -iMessage scott.coull@gmail.com '%s'\"" % (char)
            subprocess.call(shlex.split(applescript_cmd))
            time.sleep(10)

            #tcpdump_proc.terminate()
            tcpdump_proc_out.send_signal(signal.SIGINT)
            time.sleep(1)
            tcpdump_proc_in.send_signal(signal.SIGINT)
            time.sleep(1)
            
        f_idx_out.close()
        f_idx_in.close()
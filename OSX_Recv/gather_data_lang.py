#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
import re
from config import OSX_RECV_DATA, OSX_RECV_CODE

random.seed()

digits_test = re.compile('\d | \" | \'')

langs = ['chinese','french','german','russian','english','spanish']
grams = ['n']

trials = range(250)

for lang in langs:
    for gram in grams:
        f = open("%s/%s/%sgram.txt" % (OSX_RECV_DATA,lang, str(gram)))
        lines = f.readlines()
        f.close()
        
        f_idx = open("%s/%s/data_%sgram/index.txt" % (OSX_RECV_DATA,lang,str(gram)), "a")
        
        for i in trials:
            char = random.choice(lines)
            char = char.strip().split(",")[0]
            while digits_test.search(char) != None:
                char = random.choice(lines)
                char = char.strip().split(",")[0]
            char = char.replace('"', '')
            char = char.replace("'","")
            f_idx.write("%d,%s\n" % (i, char))
            f_idx.flush()
            lang_capture_string = "%s/%s/data_%sgram/%d.pcap" % (OSX_RECV_DATA,lang, str(gram), i)
            try:
                os.remove(lang_capture_string)
            except:
                pass

            filter_string = "tcp port 5223 and net 17.0.0.0/8"


            #Run applescript and finish
            applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \"osascript %s/type_letter.scpt '%s'\"" % (OSX_RECV_CODE,char)
            subprocess.call(shlex.split(applescript_cmd))
            time.sleep(4)

            #Open tcpdump and sleep
            tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (lang_capture_string, filter_string)
            tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
            time.sleep(1)

            applescript_cmd = "ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \"osascript %s/enter_letter.scpt\"" % (OSX_RECV_CODE)
            subprocess.call(shlex.split(applescript_cmd))
            time.sleep(4)

            #tcpdump_proc.terminate()
            tcpdump_proc.send_signal(signal.SIGINT)
            time.sleep(1)

        f_idx.close()
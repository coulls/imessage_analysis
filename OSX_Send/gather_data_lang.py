#!/usr/bin/python

import subprocess
import string
import shlex
import time
import signal
import random
import re
from config import OSX_OUT_DATA, OSX_OUT_CODE

random.seed()

digits_test = re.compile('\d | \" | \'')

langs = ['english', 'spanish','french','german','chinese','russian']
grams = [1,3,5,'n']

trials = range(250)

for lang in langs:
    for gram in grams:
        f = open("%s/%s/%sgram.txt" % (OSX_OUT_DATA,lang, str(gram)))
        lines = f.readlines()
        f.close()
        
        f_idx = open("%s/%s/data_%sgram/index.txt" % (OSX_OUT_DATA,lang,str(gram)), "a")
        
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
            lang_capture_string = "%s/%s/data_%sgram/%d.pcap" % (OSX_OUT_DATA,lang, str(gram), i)
            try:
                os.remove(lang_capture_string)
            except:
                pass

            filter_string = "tcp port 5223 and net 17.0.0.0/8"

            #Run applescript and finish
            applescript_cmd = 'osascript type_letter.scpt \"%s\"' % (char)
            subprocess.call(shlex.split(applescript_cmd))
            time.sleep(5)

            #Open tcpdump and sleep
            tcpdump_cmd = "tcpdump -i en1 -w %s %s" % (lang_capture_string, filter_string)
            tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
            time.sleep(1)

            applescript_cmd = "osascript enter_letter.scpt"
            subprocess.call(shlex.split(applescript_cmd))
            time.sleep(5)

            #tcpdump_proc.terminate()
            tcpdump_proc.send_signal(signal.SIGINT)
            time.sleep(1)

        f_idx.close()
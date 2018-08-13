from config import CONVO_DATA, CONVO_CODE
import signal
import sys
import subprocess
import shlex
import random
import os
import time
import numpy as np
import progressbar
from PIL import Image

random.seed()

#devices = ['OSX', 'iOS']
devices = ['iOS']
languages = ['chinese','russian','english','german','french','spanish']
actions = ['text'] * 9 + ['image'] # 90% text messages, 10% attachment
stops = [False] * 9 + [True] # 90% complete, 10% stop
sessions = range(25)
FNULL = open(os.devnull, 'w')

def send_image(send_location, device, img_size, stop):
    pix_array = []
    for k in range(img_size):
        for l in range(img_size):
            pix_array.append(tuple(np.random.random_integers(0,255,4)))
    im = Image.new('RGBA', (img_size,img_size))
    im.putdata(pix_array)
    im.save('%s/temp.png' % (CONVO_CODE), 'PNG')
    file_size = os.stat('%s/temp.png' % (CONVO_CODE)).st_size

    if (send_location == 'remote'):
        if (device == 'iOS'):
            #create image, copy to clipboard, send with VNC
            applescript_cmd = 'osascript image_ios.scpt %s/temp.png' % (CONVO_CODE)
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            time.sleep(3)
            
            if (stop):
                #use vnc to delete
                applescript_cmd = 'osascript delete_ios.scpt 2'
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            
            else:
                applescript_cmd = 'osascript send_ios.scpt'
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
                
        else:
            #tell remote host to create image, copy, paste, send with SSH
            applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                \"/opt/local/bin/python %s/gen_image_remote.py %d\"' % (CONVO_CODE, img_size)
            file_size = subprocess.check_output(shlex.split(applescript_cmd))
            file_size = int(file_size)
            
            applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                \"osascript %s/image_local.scpt %s/temp.png\"' % (CONVO_CODE, CONVO_CODE)
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            time.sleep(2)
            
            if (stop):
                applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                    \"osascript %s/delete_local.scpt 2\"' % (CONVO_CODE)
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            
            else:
                applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                    \"osascript %s/send_local.scpt\"' % (CONVO_CODE)
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
               
    else:
        applescript_cmd = 'osascript image_local.scpt %s/temp.png' % (CONVO_CODE)
        subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
        time.sleep(2)
        
        if (stop):
            applescript_cmd = 'osascript delete_local.scpt 2'
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)

        else:
            applescript_cmd = 'osascript send_local.scpt'
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)

    time.sleep(20)
    return file_size

def send_text(send_location, device, language, stop):
    #get text to send here.  possible only because all use command line.
    f = open('./language_data/%s_ngram.txt' % (language))
    lines = f.readlines()
    f.close()
    
    text = random.choice(lines)
    text = text.strip().split(",")[0]
    text = text.replace('"', '')
    text = text.replace("'","")
    if (send_location == 'remote'):
        if (device == 'iOS'):
            applescript_cmd = 'osascript type_ios.scpt \"%s\"' % (text)
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            time.sleep(3)
            
            if (stop):
                applescript_cmd = 'osascript delete_ios.scpt %d' % (len(text))
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
                
            else:
                applescript_cmd = 'osascript send_ios.scpt'
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
                
        else:
            applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                \"osascript %s/type_local.scpt \'%s\'\"' % (CONVO_CODE, text)
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            time.sleep(2)
            
            if (stop):
                applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                    \"osascript %s/delete_local.scpt %d\"' % (CONVO_CODE, len(text))
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
                
            else:
                applescript_cmd = 'ssh -i /Users/coulls/.ssh/id_rsa coulls@scoull.rj \
                    \"osascript %s/send_local.scpt\"' % (CONVO_CODE)
                subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
                
    else:
        applescript_cmd = 'osascript type_local.scpt \"%s\"' % (text)
        subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
        time.sleep(2)
        
        if (stop):
            applescript_cmd = 'osascript delete_local.scpt %d' % (len(text))
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)
            
        else:
            applescript_cmd = 'osascript send_local.scpt'
            subprocess.call(shlex.split(applescript_cmd), stdout = FNULL)

    time.sleep(5)
    return len(text)
    
for i in sessions:
    remote_dev = random.choice(devices)
    remote_lang = random.choice(languages)
    local_lang = random.choice(languages)
    session_length = 200
    #Local means at laptop, remote means other side of connection (iOS, OSX)
    monitor_location = random.choice(['local','remote'])
    #monitor_location = 'local'
    
    capture_location = "%s/%s/%d.pcap" % (CONVO_DATA,remote_dev,i)
    try:
        os.remove(capture_location)
    except:
        pass

    filter_string = "((tcp port 5223 or tcp port 443) and net 17.0.0.0/8) or \
        ((tcp port 80 or tcp port 443) and net 137.0.0.0/8)"

    if (remote_dev == 'iOS' and monitor_location == 'remote'):
        tcpdump_cmd = "tcpdump -i rvi0 -w %s %s" \
            % (capture_location, filter_string)
    else:
        tcpdump_cmd = "tcpdump -i en1 -w %s %s" \
            % (capture_location, filter_string)
        
    tcpdump_proc = subprocess.Popen(shlex.split(tcpdump_cmd))
    time.sleep(1)

    f = open(os.path.join(CONVO_DATA,"%s/%d.sess" % (remote_dev,i)),'w')
    f.write("#local_dev; local_lang; remote_dev; remote_lang; monitor_location, length\n")
    f.write("#OSX; %s; %s; %s; %s; %d\n" % (local_lang, remote_dev, remote_lang,
        monitor_location, session_length))

    progress = progressbar.ProgressBar()
    for j in progress(range(session_length)):
        action = random.choice(actions)

        #Send is going into Apple relative to monitor location, Recv out
        direction = random.choice(['send', 'recv'])
        
        stop = random.choice(stops)

        img_size = random.choice(range(16, 128))
        
        if ((monitor_location == 'remote' and direction == 'send')
            or (monitor_location == 'local' and direction == 'recv')):

            if (action == 'image'):
                out_length = send_image('remote', remote_dev, img_size, stop)
            else:
                out_length = send_text('remote', remote_dev, remote_lang, stop)
        else:
            if (action == 'image'):
                out_length = send_image('local', 'OSX', img_size, stop)
            else:
                out_length = send_text('local', 'OSX', local_lang, stop)

        f.write("start_%s;" % (direction))
        if (stop):
            f.write("stop_%s;" % (direction))
        else:
            f.write("%s_%s_%d;" % (action, direction, out_length))

    time.sleep(2)
    f.close()
    tcpdump_proc.send_signal(signal.SIGINT)
FNULL.close()
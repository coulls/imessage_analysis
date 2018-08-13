# Traffic Analysis of Encrypted Messaging Services: Apple iMessage and Beyond.

This repository contains scripts and utilities used in collecting data for 
the paper, "Traffic Analysis of Encrypted Messaging Services:  Apple iMessage 
and Beyond."  Included are utilities for automatically generating iMessage 
network traffic for various user behaviors both from an OSX (now, MacOS) 
computer and iPhone.

Note that these utilities were written and used circa 2014, and it is 
unlikely that they can be directly applied to the latest versions of iOS or 
MacOS without heavy modifications.  Also, note that generation of user behaviors 
on the iPhone requires a Jailbroken phone with VNC and SSH access.  There are 
also several dependencies, which are explained below.

No support will be provided for these utilities, but hopefully they will 
provide a starting point for anyone who wants to generate user behavior 
data on iOS or MacOS devices.

If you use any of these utilities, please consider citing the original paper:

* S. Coull and K. Dyer. Traffic Analysis of Encrypted Messaging Services: Apple iMessage and Beyond. ACM SIGCOMM Computer Communications Review, 44(4), October, 2014. 


-------------------------------------
Instructions for iOS Data Collection
------------------------------------
The following README includes information on how each of the iOS data 
collection scripts operates.  Packet capture data is simultaneously 
collected from the local wireless interface and all iPhone interfaces 
using the rvi0 interface created by the rvictl utility.

Dependencies:
1.) Cliclick -- mouse click utility for Mac OSX
2.) VNC client -- remote access to iPhone GUI from Mac OSX
3.) Jailbroken iPhone -- install of unauthorized apps
4.) VNC server on iPhone -- remote access to Messages GUI on phone
5.) SSH access to iPhone -- remote access to BiteSMS
6.) BiteSMS on iPhone -- command line driven iMessages
7.) Pastebote on iPhone & Mac OSX -- shares Mac clipboard with phone
8.) Python 2.6+ -- drives data collection and calls other scripts
9.) tcpdump -- collects packets for each iMessage event
10.) rvictl -- creates virtual interface to collect to iPhone packets

Start/Stop Collection
---------------------
Start/stop data collection records the messages sent by iMessage when 
a user starts or stops typing in the Messages app.  This collection is 
driven through remote VNC access to the Messages GUI.

Workflow:
1.) Determine x,y coordinates of Messages text box using Cliclick
2.) Set focus to VNC client and click in Messages text box with Cliclick
3.) Begin collecting "start" message data using tcpdump
4.) Use AppleScript to type random message into text box using VNC
5.) Stop "start" message collection
6.) Start "stop" message collection
7.) Use AppleScript to type backspaces and erase all text using VNC
8.) Stop "stop" message collection

Read Reciept Collection
-----------------------
This collects packet trace data associated with the event that a user, 
with read recipients enabled, has looked at a message.

Workflow:
0.) Ensure read recipients are enabled on recipient device
1.) Determine x,y coordinates of button to return to main Messages index
2.) Determine x,y coordinates of Messages index used for collection
3.) Send random text to recipient using SSH and BiteSMS
4.) Start tcpdump collection
5.) Use Cliclick to view Messages index from sender
6.) Stop tcpdump collection

Random Text & Language Collection
---------------------------------
Collects data on the sending and receiving of standard text messages 
containing random text strings of exponentially increasing length 
(8, 16, 32, 64, 128).  Languages proceed in a similar way except 
instead of creating random strings, the strings are taken from the 
corpus index in the respective data folders.

Workflow:
1.) Start tcpdump collection
2.) Send random text of specified size using SSH and BiteSMS
3.) Stop tcpdump collection

Image Collection
----------------
Capture all data streams surrounding the event where a user sends an 
attachment through iMessage.  These include APNS, TLS (to Apple/MS) on 
the sender side and APNS, HTTP (to MS), TLS (to Apple) on the receiver.
Images are sent a canonical attachments of exponentially increasing 
dimensions (16 x 16, 32 x 32, 64 x 64).

Workflow:
1.) Determine x,y coordinates of Messages text box, paste bubble, and send
2.) Generate random PNG image of specified dimensions save to "temp.png"
3.) Use AppleScript to copy "temp.png" to clipboard
4.) Pastebot should automatically transfer the image to iPhone's clipboard
5.) Use VNC and Cliclick to paste image.  Wait until after "start" message
6.) Start tcpdump collection
7.) Use VNC and Cliclick to press send button
8.) Stop tcpdump collection after image has fully transferred


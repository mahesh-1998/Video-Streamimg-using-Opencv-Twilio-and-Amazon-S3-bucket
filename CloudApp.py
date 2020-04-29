# USAGE
# python detect.py --conf config/config.json

# import the necessary packages
from __future__ import print_function
from cloud_project.notifications import TwilioNotifier
from cloud_project.utils import Conf
from imutils.video import VideoStream
from imutils.io import TempFile
from datetime import datetime
from datetime import date
import numpy as np
import argparse
import imutils
import signal
import time
import cv2
import sys

# function to handle keyboard interrupt
def signal_handler(sig, frame):
	print("[INFO] You pressed `ctrl + c`! Closing mail detector" \
		" application...")
	sys.exit(0)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="Path to the input configuration file")
args = vars(ap.parse_args())

# load the configuration file and initialize the Twilio notifier
conf = Conf(args["conf"])
tn = TwilioNotifier(conf)


# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")

def menu():
	print("Select from the options:")
	print("\n1. Use webcam")
	print("\n2. Manually add path of video")
	choice = input("\n")
	choice = int(choice)
	if choice == 1:
		WebcamStream(choice)
	elif choice == 2:
		WebcamStream(choice)
	else:
		print("Please select valid option")

def WebcamStream(choice):

	if choice == 2:
		tempVideopath = input("\nEnter the path of video:")
		tempVideo = tempVideopath[tempVideopath.rfind("/")+1:len(tempVideopath)]
		print("\nPath:"+tempVideopath +"\nFilename:"+tempVideo)
		msg = "Cloud Computing mini project"+"\n"+"Video from local directory"
		tn.send_path(msg,tempVideo,tempVideopath)
	else:
		cap = cv2.VideoCapture(0)

		# Define the codec and create VideoWriter object
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		#tempVideo = 'output.xvi'
		tempVideo = filename = 'output_{0}.avi'.format(datetime.now().strftime("%Y-%m-%d"))
		out = cv2.VideoWriter(tempVideo,fourcc, 20.0, (640,480))
		startTime = datetime.now()
		print("\nFilename:"+tempVideo)
		while(cap.isOpened()):
		    ret, frame = cap.read()
		    timeDiff = (datetime.now() - startTime).seconds
		    if ret==True:
			#frame = cv2.flip(frame,0)

			# write the flipped frame
                        out.write(frame)
                        cv2.imshow('frame',frame)
                        if cv2.waitKey(1) & 0xFF == ord('q') or (timeDiff > 10):
                            msg = "Cloud Computing mini project"+"\n"+"Video from Webcam"
                            tn.send(msg,tempVideo)
                            break
		    else:
                            break
                # Release everything if job is finished
		cap.release()
		out.release()
		cv2.destroyAllWindows()


menu()





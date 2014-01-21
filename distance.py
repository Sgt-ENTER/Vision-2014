# Import Libraries
import cv2 as cv
import numpy as np
import math

#Get feed from WebCam
vc = cv.VideoCapture(-1)

#Set Video Capture properties
vc.set(cv.cv.CV_CAP_PROP_BRIGHTNESS, 0.2)
vc.set(cv.cv.CV_CAP_PROP_SATURATION, 0.5)  #0.125
vc.set(cv.cv.CV_CAP_PROP_CONTRAST, 0.5)   #0.01

#Resolution (pixels)
width = 640
height = 480

#Target squareness ratio
target_ratio = 0.6 # Needs to have height/width be between this and the reciprocal

#max. distance the camera can detect is 13 feet
#ClivePamer is the distance threshold (it is the maximum distance that the camera will detect)
ClivePalmer = 13 #ft

#Ball Dimensions 6
ballw = 0
ballh = 0

#Image counter
counter = 0

if vc: # try to get the first frame
	#setting frame width
	vc.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, width)
	#setting frame height
	vc.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
	
	#Reading the webcam feed
	retval, frame = vc.read()

	#Kernel Dimensions
	kernel = cv.getStructuringElement (cv.MORPH_ELLIPSE,(4, 4))
	
	#Constant Video feed
	while retval:
		retval, frame = vc.read()
		
		#Converting to HSV
		hsv_image = cv.cvtColor(frame, cv.cv.CV_BGR2HSV)
		
		#Colour Space Threshold
		mask_neg = cv.inRange(hsv_image, np.array([0, 50, 50]), np.array ([10,255,255]))
		mask_pos = cv.inRange(hsv_image, np.array([170,50,50]), np.array ([180,255,255]))
	
		#Combine masks
		mask = mask_pos | mask_neg
		
		final_image = frame 
		
		#Eroding and Dilating mask
		opened = cv.erode(mask, kernel, iterations = 7)
		opened = cv.dilate(opened, kernel, iterations = 7)
		
		#Find and Display contour
		contours, hierarchy = cv.findContours(opened, cv.cv.CV_RETR_EXTERNAL, cv.cv.CV_CHAIN_APPROX_NONE)
		
		largest_size = 0
		largest_index = 0
		for index, contour in enumerate(contours):
			if cv.contourArea(contour) > largest_size: 
				
				#Get co-ordinates and dimensions of ball
				x,y,w,h = cv.boundingRect(contours[largest_index])
				
				ballratio = 1.0 * w/h
				
				#Track ball when size > threshold
				#print "%.2f" % ballratio
				if ballratio > target_ratio and ballratio < 1.0/target_ratio:
					largest_size = cv.contourArea(contour)
					largest_index = index
					
		if contours and largest_size > 0: #if no red detected, it will stall until it finds red
			x,y,w,h = cv.boundingRect(contours[largest_index])
			#distance formula from width of ball
			distance = 1661.5*w**-1.075
			if distance < ClivePalmer: 
				cv.rectangle(final_image, (x,y), (x+w, y+h), (0,255,0), 7)
				cv.drawContours(frame, contours, largest_index, (0,255,0)) 
				moments = cv.moments(contours[largest_index])
			
				#Get centroid
				if moments['m00'] != 0: 
					xbar = int(moments['m10']/moments['m00'])
					ybar = int(moments['m01']/moments['m00'])
				
				#draw circle at centroid of ball
				#cv.circle(final_image, (xbar,ybar),10, (0,255,0), 7)
				
				
		#Show feed
		cv.imshow("preview", final_image)
		
		# save image
		key = cv.waitKey(20)

		if key == ord('p'):
			cv.imwrite('picture%d %dw x %dh.png' % (counter,w,h),final_image)
			counter += 1
			
		#break Loop	
		if key == ord('a'): # exiton pressing 'a'
			break
			#Loop forever...

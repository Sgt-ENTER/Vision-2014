import cv2 as cv
import numpy as np
import math

cv.namedWindow("preview")
vc = cv.VideoCapture(-1)

if vc: # try to get the first frame
	vc.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
	vc.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
	retval, frame = vc.read()

	
	while retval:
		retval, frame = vc.read()
		hsv_image = cv.cvtColor(frame, cv.cv.CV_BGR2HSV)
		mask_neg = cv.inRange(hsv_image, np.array([0, 50, 50]), np.array ([10, 255, 255]))
		mask_pos = cv.inRange(hsv_image, np.array([170, 50, 50]), np.array ([180, 255, 255]))
		#final_image = cv.cvtColor(mask, cv.cv.CV_GRAY2RGB)
		#	|cv.cvtColor(mask_neg, cv.cv.CV_GRAY2RGB))
		mask = mask_pos |mask_neg
		
		kernel = cv.getStructuringElement (cv.MORPH_RECT,(7, 7))
		opened = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
	
		contours, hierarchy = cv.findContours(opened, cv.cv.CV_RETR_EXTERNAL, cv.cv.CV_CHAIN_APPROX_NONE)
		largest_size = 0
		largest_index = 0
		for index, contour in enumerate(contours):
			if cv.contourArea(contour) > largest_size: 
				largest_size = cv.contourArea(contour)
				largest_index = index
		cv.drawContours(frame, contours, largest_index, (0,255,0)) 
		moments = cv.moments(contours[largest_index])
		final_image = frame #& cv.cvtColor(opened, cv.cv.CV_GRAY2RGB)
		#circles = cv.HoughCircles(opened, cv.cv.CV_HOUGH_GRADIENT, 2, 120, 200, 100)
		#if circles != None:
			#for circle in circles:
				#cv.circle(final_image, (circle[0], circle[1] ),circle [2], (0,255,0))
		if moments['m00'] != 0: 
			xbar = int(moments['m10']/moments['m00'])
			ybar = int(moments['m01']/moments['m00'])
			cv.circle(final_image, (xbar,ybar),10, (0,255,0), 7)
		
		
		cv.imshow("preview", final_image)	
		key = cv.waitKey (20)
		if key != -1: # exiton any key
			break
			#Loop forever...
			
 

import cv2 as cv
import numpy as np
import math
import socket
import threading
import SocketServer

width = 640.0
height = 480.0

xbar = 99.0
ybar = 99.0
w = 99.0

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        global xbar, ybar, w
        data = self.request.recv(1024)
        response = '{} {} {}'.format(xbar,ybar,w)
        #print "Request from cRIO."
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
    
if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "10.47.74.42", 4774
	
	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address
	
	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread.daemon = True
	server_thread.start()
	
	vc = cv.VideoCapture(-1)
	
	if vc: # try to get the first frame
		vc.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, width)
		vc.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
		retval, frame = vc.read()
	
		while retval:
			retval, frame = vc.read()
			hsv_image = cv.cvtColor(frame, cv.cv.CV_BGR2HSV)
			mask_neg = cv.inRange(hsv_image, np.array([0, 50, 50]), np.array ([10, 255, 255]))
			mask_pos = cv.inRange(hsv_image, np.array([170, 50, 50]), np.array ([180, 255, 255]))
			mask = mask_pos | mask_neg
			
			kernel = cv.getStructuringElement (cv.MORPH_RECT,(7, 7))
			opened = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
		
			contours, hierarchy = cv.findContours(opened, cv.cv.CV_RETR_EXTERNAL, cv.cv.CV_CHAIN_APPROX_NONE)
			largest_size = 0
			largest_index = 0
			
			ball_found = False
			if contours: 
				for index, contour in enumerate(contours):
					if cv.contourArea(contour) > largest_size: 
						largest_size = cv.contourArea(contour)
						largest_index = index
				moments = cv.moments(contours[largest_index])
				
				if moments['m00'] != 0: 
					xbar = 2.0*moments['m10']/moments['m00']/width - 1.0
					ybar = 2.0*moments['m01']/moments['m00']/height - 1.0
					x,y,w,h = cv.boundingRect(contours[largest_index])
					w = 2.0 * w / width
					ball_found = True	
				
					#print "Ball found! {} {} {}".format(xbar, ybar, w)
			if not ball_found:
				xbar = 99
				ybar = 99
				w = 99
				#print "Ball lost :-("
		
					
			
			
				
	 
	

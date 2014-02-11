import cv2
import cv2.cv as cv
import numpy as np
import math as m



class GoalFinder:
    def __init__(self, width = 640, height = 480): # Constructor to get the video capture set up
		#video Capture settings
        self.videoPort = -1
        self._vc = cv2.VideoCapture(self.videoPort)
        self._width = 1.0 * width # Force a float
        self._height = 1.0 * height

		#video resolution
        self._vc.set(cv.CV_CAP_PROP_FRAME_WIDTH, self._width)
        self._vc.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self._height)

        #Set Video Capture properties
        self._vc.set(cv.CV_CAP_PROP_BRIGHTNESS, 0.2)
        self._vc.set(cv.CV_CAP_PROP_SATURATION, 0.5)
        self._vc.set(cv.CV_CAP_PROP_CONTRAST, 0.5)

        self.rect_index = []
        # Public member variables to store the last calculated values
        # Invalid values indicate ball not found
##        self.xbar = 99.0 # xbar, ybar should be in the range [-1.0, 1.0]
##        self.ybar = 99.0
##        self.width = 99.0 # diam should be in the range (0.0, 2.0]
##        self.height = 99.0
        self.rectangles = []
        
        self.VHlow = 0.94
        self.VHhigh = 1.74
        self.HHlow = 1.73
        self.HHhigh = 1.93
        
        
        self.height = []
        self.Hpos = 3
        self.Hlength = 0
        self.Glength = 0
        self.sort = []
        self.avg = 0
       
        self.bestpos = 5 #find by testin on cat
        self.angle = 0
        

        
        self.threshold = 250
        self.maxval = 255

    def find(self):
        if not self._vc:
            # Try to reinitialise, but still return None
            self.__init__()
            return None
        # We have a video capture object so we can proceed
        retval, frame = self._vc.read()
        if not retval:
            return None

        # Do Goal Tracking Bit
        greyimage = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(greyimage)
        ret, thresh = cv2.threshold(equ, self.threshold, self.maxval, cv2.THRESH_BINARY)
        thresh2 = cv2.adaptiveThreshold(thresh, self.maxval,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,19,2)
        kernel = cv2.getStructuringElement (cv2.MORPH_RECT,(5, 5))
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        blur = cv2.GaussianBlur(opened, (1,1), 0)
        #dilopened = cv2.dilate(thresh, kernel, iterations = 2)
        edge = cv2.Canny(blur,0, self.maxval)
        dilopened = cv2.dilate(thresh, kernel, iterations = 2)
        #dilopened = cv2.erode(thresh, kernel, iterations = 2)
        #bgmask = self.bgsub.apply(frame)

        contours, hierarchy = cv2.findContours(dilopened, cv2.cv.CV_RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_NONE)
        found_rectangles = []
        for index, contour in enumerate(contours):
            #self.rect_index[index] = index
            area = cv2.contourArea(contour)
            if area > 1800:
				x,y,w,h = cv2.boundingRect(contours[index])
				found_rectangles.append([x,y,w,h])
				if self.Glength != 0:
					for i in range(self.Glength):
						if self.Hlength < self.Glength:
							self.height.append(self.rectangles[i][self.Hpos])
					
					self.sort = sorted(self.height)
					Slength = len(self.sort)
					if Slength !=0:
						if Slength < 3:
							highsort = ([self.sort[Slength -1]])
							
						else:
							highsort = ([self.sort[Slength -2], self.sort[Slength -1]])
							self.avg = np.average(highsort)
					else:
						self.avg = 99.0
                    
        self.rectangles = found_rectangles
        self.Glength = len(self.rectangles)
        self.Hlength = len(self.height)
        
        equation = (8*10**(-9)*(self.avg**4))-(8*10**(-6)*(self.avg**2))+(0.0032*(self.avg**2))-(0.6061*self.avg)+53.116
        angle = m.acos(self.bestpos/equation) #in radians
        self.angle = (angle*m.pi/2)
        print self.sort
			
        #if contours:
			#for index, contour in enumerate(contours):
				#largest_size = cv2.contourArea(contour)
				#largest_index = index

			#if largest_index > 0:

#cv2.drawContours(frame, contours, index, (0,255,0),4)
				#cv2.drawContours(frame, contours, index, (0,255,0))
				#goal_found = True

        #if not goal_found:
            # No ball found so set the member variables to invalid values
##            self.xbar = 99.0
##            self.ybar = 99.0
##            self.height = 99.0
##            self.width = 99.0

        # Return the frame, the contours and largest image in case we
        # want to show them on the screen
         #return 	frame #self.rectangles#, contours, index#, contours, largest_index

    def absolute(self):
        # Convert xbar, ybar and diam to absolute values for showing on screen
        return (int((self.xbar+1.0)*self._width/2.0),
            int((self.ybar+1.0)*self._height/2.0),
            int(self.height*self._width/2.0))

if __name__ == "__main__":
    gf = GoalFinder( 640, 480)
    cv2.namedWindow("preview")
    while True:
        result = gf.find()
        frame = result
        for rect in gf.rectangles:
            x,y,w,h = rect
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 7)
        
        #frame, contours, largest_index = result\
        #cv2.drawContours(frame, contours, index, (0,255,0), 
        if frame:
            cv2.imshow("preview", frame)
        key = cv2.waitKey (10)
        if key != -1:
			break# Exit on any keybreak
        # Get the next frame, and loop forever

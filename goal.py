#Import libraries
import cv2
import cv2.cv as cv
import math as m

#Camera number
CAMERA = 0

class GoalFinder:
    def __init__(self, width = 640, height = 480): # Constructor to get the video capture set up
        self._vc = cv2.VideoCapture(CAMERA)
        self._width = 1.0 * width # Force a float
        self._height = 1.0 * height
        self._center = 0.5* self._width

		#initialise video feed and make sure its good
        #try: 
            #self._vc = cv2.VideoCapture(self.videoPort)
        #except:
			#self._vc = None			
		
		#video resolution
        self._vc.set(cv.CV_CAP_PROP_FRAME_WIDTH, self._width)
        self._vc.set(cv.CV_CAP_PROP_FRAME_HEIGHT, self._height)

        #Set Video Capture properties
        self._vc.set(cv.CV_CAP_PROP_BRIGHTNESS, 0.2)
        self._vc.set(cv.CV_CAP_PROP_SATURATION, 0.5)
        self._vc.set(cv.CV_CAP_PROP_CONTRAST, 0.5)

        #Default values
        self.defaultHvalue = 99.0
        self.rectHeight = self.defaultHvalue

        # Best position to fire from
        self.rect_index = []
        self.gRange = self.defaultHvalue
        self.angle = self.defaultHvalue
        self.Hot = self.defaultHvalue
        self.currentPos = self.defaultHvalue
        self.currentWidth = self.defaultHvalue

        # Threshold to detect rectanlges
        self._threshold = 250
        self._maxval = 255
        self._minarea = 2.8125*self._width #value from spreadsheets

        # Kernel for eroding/dilating
        self._kernel = cv2.getStructuringElement (cv2.MORPH_RECT,(5, 5))


    def find(self,frame):
        if frame == None:
            self.gRange = self.defaultHvalue
            self.angle = self.defaultHvalue
            self.Hot = self.defaultHvalue
            return None

        # Do Goal Tracking Bit
        #Convert to grey scale
        greyimage = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        #Equalise to remove brightness
        equ = cv2.equalizeHist(greyimage)

        # Convert to binary
        ret, thresh = cv2.threshold(equ, self._threshold, self._maxval, cv2.THRESH_BINARY)
        thresh2 = cv2.adaptiveThreshold(thresh, self._maxval,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,19,2)
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, self._kernel)
        blur = cv2.GaussianBlur(opened, (1,1), 0)
        edge = cv2.Canny(blur,0, self._maxval)
        dilopened = cv2.dilate(thresh, self._kernel, iterations = 2)

        contours, hierarchy = cv2.findContours(dilopened, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_NONE)
        found_rectangles = []
        filter_height = []
        filter_x = []
        xvalue = []
        northernstar = self.defaultHvalue
        goal_found = False
        for index, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > self._minarea:
                x,y,w,h = cv2.boundingRect(contours[index])
                found_rectangles.append([x,y,w,h])
                filter_height.append([h])
                filter_x.append([x])
        #sorts the filtered height into acending order        
        filter_height = sorted(filter_height)
        if len(filter_height) != 0:
            #stores the index of max value in filter height
            #if it can compare w to max filter height
            #xvalue is index -1 (this make it into index form)
            for index, w in enumerate(filter_height):
                if w == max(filter_height):
                    xvalue = index - 1     #x
            
            northernstar = filter_height[len(filter_height)-1]
            
            angletoS = filter_x[xvalue]
           
            self.rectangles = found_rectangles
            
         
            self.rectHeight = northernstar[len(northernstar)-1]
            self.rectWidth = angletoS[len(angletoS)-1]
            self.rect_index = len(found_rectangles)
            
                #if self.bestPosition/self.currentPos < 1.00:
            self.angle = (self.rectWidth/(self._width/2))-1#rescaled width value from -1 to +1
            self.gRange = 461.25*self.rectHeight**(-0.916) # finds range of goal in meteres 
            self.Hot = self.rect_index 
        return frame #self.rectangles#, contours, index#, contours, largest_index
        
    def capture(self):
        if not self._vc:
            # Try to reinitialise, but still return None
            self.__init__()
            return None
        # We have a video capture object so we can proceed
        retval, frame = self._vc.read()
        if retval:
            return frame
        else:
            return None

    def absolute(self):
        # Convert xbar, ybar and diam to absolute values for showing on screen
        return (float(self.gRange),
            float(self.angle),
            int(self.Hot))

if __name__ == "__main__":
    gf = GoalFinder(640, 480)
    cv2.namedWindow("preview")
    result = gf.find(gf.capture())
    while result != None:
        
        ## After here is for visual feedback only
       frame = result
       for rect in gf.rectangles:
           x,y,w,h = rect
           cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 7)
	       #frame, contours, largest_index = result\
		   #cv2.drawContours(frame, contours, index, (0,255,0),
       cv2.imshow("preview", frame)
       print gf.absolute()
       key = cv2.waitKey (20)
       if key != -1:
           break# Exit on any keybreak
			# Get the next frame, and loop forever
       result = gf.find(gf.capture())
		  

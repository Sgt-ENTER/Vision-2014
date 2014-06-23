#image 1.5m is actually 1.2 but was changed to allow for easy reading by the program
import csv
import cv2
from nose.tools import assert_almost_equal
from goal import GoalFinder #gets our goal.py code

def test_find():
    gf = GoalFinder()   
    
    with open('img/goal.csv','rb') as csvfile:
	#opens image file
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            frame = cv2.imread('img/'+row[0])
            gf.find(frame)
           
            delta = 0.05
            # Create a separate test for each image
            yield find_goal, gf, row[0], row[1], row[2], row[3], delta
                
def find_goal(gf,filename, gRange, angle, Hot, delta):
    #will compare what we got from the image with what we expected to get
    message = filename + " - %s\nExpected: %s +/- "+str(delta)+"\nReceived: %s"
    assert_almost_equal(gf.gRange, float(gRange), delta=delta, msg=message % ("gRange", gRange, str(gf.gRange)))
    assert_almost_equal(gf.angle, float(angle), delta=delta, msg=message % ("angle", angle, str(gf.angle)))
    assert_almost_equal(gf.Hot, float(Hot), delta=delta, msg=message % ("Hot", Hot, str(gf.Hot)))
	
    
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    import nose
    nose.main()

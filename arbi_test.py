import numpy

# Constructor Initialise
#Initialise Variables
height = [] #For storing height values only
Hpos = 3    #position of height in array we get from ball.py
Hlength = 0 #Length of Height only array
Glength = 0 #Length of Goal array (values we get from ball.py)
sort = [] #Array in ascending order of Height values
avg = 0 # average values of H

#same while loop as in ball.py
while True:
    rect = [[1,2,3,4],[5,6,7,8],[1,5,6,7],[45,7,8,34]] # sample Goal values

    Glength = len(rect) #Get length of Goal detection array
    Hlength = len(height)

    #check for detection of goals
    if Glength != 0: #if length of array is not zero, you have detected something
        for i in range(Glength): #loop through array
            if Hlength < Glength: #condition to make sure we only add the rectangles we find
                #add values to height array
                # --- add code to add values to height array
                # --- check for tutorials on adding values
                # --- to access multidimensional arrays use this code
                # --- array[first array pos][sub array pos]
		
		sort = sorted(height)
        Slength = len(sort)
        if Slength != 0: #Condition to make sure we have something
            if Slength < 3: #if we detect only the left hand side goals [2 rectangles]
                #select the last value because that will be the largest one
                highsort = ([sort[Slength-1]]) # length count starts from 1, array count starts from 0
            else:
                  #select the last two values
                # --- Insert code to detect last two values in array
                # --- Look at the above code for help
               
            #average the H values we filtered
            # --- insert code for averaging values of vairable - highsort
        # --- research about numpy average
			print avg
			else:
				avg = 99 # default value




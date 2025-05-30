'''
*********************************************************************************
*
*        		===============================================
*           		        CYBORG OPENCV TASK 2
*        		===============================================
*
*
*********************************************************************************
'''

# Author Name:		[Samarpan Sahu]
# Roll No:			[124EC0035]
# Filename:			task_2A_{Samarpan Sahu}.py
# Functions:		detect_faulty_squares


####################### IMPORT MODULES #######################
import cv2 as cv
import numpy as np
##############################################################

def detect_faulty_squares(img):
    
    sorted_squares = {}
    
	################################################################
    ##                     Add your code here                     ##

    prev_color=0
    x=105
    y=105
    pos_y=65
    pos_x=1
    count=1
    while(x<526 and y<526):
        pixel_values=img[y,x]
        if(pixel_values[0]==0 and pixel_values[1]==0 and pixel_values[2]==255):
            color="Red"
        elif(pixel_values[0]==255 and pixel_values[1]==255 and pixel_values[2]==0):
            color="Blue"
        elif(pixel_values[0]==0 and pixel_values[1]==255 and pixel_values[2]==0):
            color="Green"
        elif(pixel_values[0]==0 and pixel_values[1]==165 and pixel_values[2]==255):
            color="Orange"
        elif(pixel_values[0]==255 and pixel_values[1]==255 and pixel_values[2]==255):
            color="Black"
        else:
            color="White"
        if(color!="Black" and color !="White"):
            pos=chr(pos_y)+str(pos_x)
            tup=(color,pos)
            if(prev_color==1):
                color="Black"
            else:
                color="White"
            sorted_squares[tup]=color
        pos_x+=1
        x+=60
        count+=1
        prev_color=1-prev_color
        if(pos_x>8):
            prev_color=1-prev_color
            pos_y+=1
            pos_x=1
            y+=60
            x=105


	################################################################

    return sorted_squares

# img=cv.imread("/home/samarpan/Desktop/Task_2A/Test_images/faulty_chessboard_5.png")
# print(detect_faulty_squares(img))
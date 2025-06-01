'''
*********************************************************************************
*
*        		===============================================
*           		        CYBORG OPENCV BONUS TASK
*        		===============================================
*
*
*********************************************************************************
'''

# Author Name:		[Samarpan Sahu]
# Roll No:			[124EC0035]
# Filename:			bonus_task_[Samarpan Sahu].py
# Functions:		process_distorted_chessboard

####################### IMPORT MODULES #######################
import cv2 as cv
import numpy as np
import cv2.aruco as aruco
##############################################################

img=cv.imread("/home/samarpan/Desktop/Task_2B_BONUS_124EC0035/distorted_chessboard.png")
#Converting to top-down view
init_pts=np.array([[409,431],[557,414],[468,637],[332,659]],dtype=np.float32)  #I got these points manually

final_pts=np.array([[100,100],[400,100],[400,400],[100,400]],dtype=np.float32)

trans=cv.getPerspectiveTransform(init_pts,final_pts)    
img_trans=cv.warpPerspective(img,trans,(500,500))

#Reducing distortion
h,w=img_trans.shape[:2]
camera_matrix = np.array([[float(w), 0, float(w/2)],[0, float(h), float(h/2)],[0,  0,  1]],dtype=np.float32)
dist_coeffs = np.array([-0.855, 0.25, 0,0, 0.025], dtype=np.float32)   #Got the values by trial and error
undistort=cv.undistort(img_trans,camera_matrix,dist_coeffs)            #The rectified image is attached 

#Detecting and Reading Aruco Markers
gray=cv.cvtColor(undistort,cv.COLOR_BGR2GRAY)
dict=aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
parameter=aruco.DetectorParameters()
detector=aruco.ArucoDetector(dict,parameter)
corners,ids,reject_img=detector.detectMarkers(gray)
id_img=aruco.drawDetectedMarkers(undistort,corners,ids,(255,0,14))   #Image having the ArUco markers id labelling is attached

row,coloumn=ids.shape
print("The ids of ArUco Markers are:",end=" ")
for i in range (0,row):
    print(ids[i,coloumn-1],end=" ")
#cv.imwrite("/home/samarpan/Desktop/Cyborg_Robotics_Tasks_2025/IP_TASK/Task_2B_BONUS/id_pic.png",id_img)
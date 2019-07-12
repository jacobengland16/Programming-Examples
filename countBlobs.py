"""
Created on Thu Jul 11 13:46:09 2019

@author: jengland
"""

'''
Instead of manually counting out seeds to be weighed, we can use OpenCV to detect
blobs present in an image. This is advantagous because it saves a significant amount of
time when counting a large number of seeds. 

To count the seeds, spread a few seeds out on a piece of paper, 
making sure that they aren't touching (they can be close but need some white space).

Plug image name into the script and a seed count will be found. 
If exact accuracy is needed, I recommend viewing the image (saved to your desktop currently)
to verify that the seeds were properly counted. 

'''
import cv2
import numpy as np

#declare object with the blob detection filter properties
params = cv2.SimpleBlobDetector_Params()

seedType = input("Enter the seed type: ")
seedType = seedType.lower()

#declare filter properties specific to canola
params.filterByColor = True
params.blobColor = 0

params.filterByConvexity = True
params.minConvexity = .9

params.filterByArea = True
params.minArea = 200

#open the image in greyscale format
im = cv2.imread("C:/Users/jengland/Desktop/seedsWeighed.jpg", cv2.IMREAD_GRAYSCALE)
kernal = np.ones((3,3),np.uint8)
im = cv2.erode(im,kernal,iterations = 1)

#create a blob detector, pass in filters
detector = cv2.SimpleBlobDetector_create(params)

#detect objects, location of objects stored in an array
keypoints = detector.detect(im)

#draws circles around detected blobs
keypointsImage = cv2.drawKeypoints(im,keypoints,np.array([]),(0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#creates/saves a new image with circles around the detected blobs. 
cv2.imwrite("C:/Users/jengland/Desktop/seedsCounted.jpg",keypointsImage)

#print out the total number of blobs
numBlobs = len(keypoints)
print("Total number of Objects:",numBlobs)

import numpy as np
import cv2

# cv2.namedWindow('image', cv2.WINDOW_NORMAL)

#Load the Image
# imgo = cv2.imread('0008-0407-2011-1313_littering_pop_can_on_grass_pics_pictures_photos.jpg')
# imgo = cv2.imread('2008-07-12_arizona_green_tea_can_littering_the_lawn2.jpg')
imgo = cv2.imread('coca-cola 007.JPG')
height, width = imgo.shape[:2]

#Create a mask holder
mask = np.zeros(imgo.shape[:2],np.uint8)

#Grab Cut the object
bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

#Hard Coding the Rect The object must lie within this rect.
rect = (10,10,width-30,height-30)
cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')

####MY STUFF I'M ADDING
# print mask.depth()
# mask_split = np.array(cv2.split(mask))
# print mask_split
# mask_split = cv2.filter2D(mask_split, -1, np.ones((25,25)))
# mask = cv2.merge(mask_split)
# print mask
# np.invert(mask)
# mask = cv2.filter2D(mask, -1, np.ones((25,25)))
# np.invert(mask)
# mask = cv2.medianBlur(mask,25)
##########

img1 = imgo*mask[:,:,np.newaxis]

#Get the background
background = imgo - img1

####MY STUFF I'M ADDING
background = cv2.medianBlur(background,25)
##########

#Change all pixels in the background that are not black to white
background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]

#Add the background and the image
final = background + img1

####MY STUFF I'M ADDING
# final = cv2.fastNlMeansDenoisingColored(final,None,10,10,7,21)
# print mask
# final = cv2.filter2D(final, -1, np.ones((1000,1000)))
# final_grey = cv2.cvtColor(final, cv2.COLOR_BGR2GRAY)
# print final_grey
# final_grey = cv2.threshold(final_grey, 254, 255, cv2.THRESH_BINARY_INV)
# print final_grey[1]
# np.invert(final_grey[1])
# # final_grey = cv2.filter2D(final_grey[1], -1, np.ones((15,15)))
# final_grey = cv2.medianBlur(final_grey[1],15)
# np.invert(final_grey)
# cv2.imshow('image2', final_grey )
# final = cv2.medianBlur(final,15)
# cv2.findContours(final,contours,hierarchy,Imgproc.RETR_TREE,Imgproc.CHAIN_APPROX_SIMPLE);
##########

#To be done - Smoothening the edges.

cv2.imshow('image', final )
cv2.imwrite('output.jpg',final)

k = cv2.waitKey(0)

if k==27:
	cv2.destroyAllWindows()


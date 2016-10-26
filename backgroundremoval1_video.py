import numpy as np
import cv2

def nothing(*arg):
    pass

def make_odd(val):
    if val % 2 == 0:
        val += 1

    return val

def findSignificantContours (img, edge_image):
    # image, 

    contours, heirarchy = cv2.findContours(edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if heirarchy is None:
        return None

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    # tooSmall = edge_image.size * 0.00005 # If contour isn't covering 5% of total area of image then it probably is too small
    # tooSmall = edge_image.size * 1 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    tooSmall = 0.0
    for tupl in level1:
        contour = contours[tupl[0]];
        area = cv2.contourArea(contour)
        if area > tooSmall:
            significant.append([contour, area])

            # Draw the contour on the original image
            cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.cv.CV_AA, maxLevel=1)

    significant.sort(key=lambda x: x[1])
    #print ([x[1] for x in significant]);
    return [x[0] for x in significant];

window_nm = 'img_cntrls'
cv2.namedWindow(window_nm)
cv2.createTrackbar('blur_size', window_nm, 13 , 21, nothing)

# img = cv2.imread('0008-0407-2011-1313_littering_pop_can_on_grass_pics_pictures_photos.jpg')
video_capture = cv2.VideoCapture('WIN_20161025_16_54_51_Pro.mp4')

while True:
    ret, img = video_capture.read()
    if ret == True:

        blur_size = cv2.getTrackbarPos('blur_size',window_nm)
        blur_size = make_odd(blur_size)

        blurred = cv2.GaussianBlur(img, (blur_size, blur_size), 0) # Remove noise

        img_grey = imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edgeImg = cv2.Canny(blurred,100,200)

        findSignificantContours(img, edgeImg)

        cv2.imshow('Orig',img)
        # cv2.imshow('Blurred',blurred)
        # cv2.imshow('edgeImg',edgeImg)
    else:
        video_capture.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO,0)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
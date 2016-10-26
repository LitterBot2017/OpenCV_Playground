import numpy as np
import cv2

# def edgedetect (channel):
#     sobelX = cv2.Sobel(channel, cv2.CV_16S, 1, 0)
#     sobelY = cv2.Sobel(channel, cv2.CV_16S, 0, 1)
#     sobel = np.hypot(sobelX, sobelY)

#     sobel[sobel > 255] = 255; # Some values seem to go above 255. However RGB channels has to be within 0-255

def nothing(*arg):
    pass

def make_odd(val):
    if val % 2 == 0:
        val += 1

    return val

window_nm = 'img_cntrls'
cv2.namedWindow(window_nm)
cv2.createTrackbar('blur_size', window_nm, 7 , 21, nothing)

img = cv2.imread('0008-0407-2011-1313_littering_pop_can_on_grass_pics_pictures_photos.jpg')

blurred = cv2.GaussianBlur(img, (5, 5), 0) # Remove noise

# edgeImg = np.max( np.array([ edgedetect(blurred[:,:, 0]), edgedetect(blurred[:,:, 1]), edgedetect(blurred[:,:, 2]) ]), axis=0 )

img_grey = imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edgeImg = cv2.Canny(img,100,200)

# scharrX = cv2.Scharr(channel, cv2.CV_16S, 1, 0)
# scharrY = cv2.Scharr(channel, cv2.CV_16S, 0, 1)
# scharr = np.hypot(scharrX, scharrY)

while True:
    blur_size = cv2.getTrackbarPos('blur_size',window_nm)
    blur_size = make_odd(blur_size)

    blurred = cv2.GaussianBlur(img, (blur_size, blur_size), 0) # Remove noise

    img_grey = imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edgeImg = cv2.Canny(blurred,100,200)

    cv2.imshow('Orig',img)
    cv2.imshow('Blurred',blurred)
    cv2.imshow('edgeImg',edgeImg)
    # cv2.imshow('Orig',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
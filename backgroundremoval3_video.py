import numpy as np
import cv2
import math

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
    tooSmall = 0.005 * edge_image.size
    # tooSmall = 0.0
    for tupl in level1:
        contour = contours[tupl[0]];
        (x,y),radius = cv2.minEnclosingCircle(contour)
        area = math.pi*radius*radius
        # area = cv2.contourArea(contour)
        if area > tooSmall:
            significant.append([contour, area])

            # Draw the contour on the original image
            cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.cv.CV_AA, maxLevel=1)
            cv2.circle(img,(int(x),int(y)),int(radius),(0,255,0),2)

    significant.sort(key=lambda x: x[1])
    #print ([x[1] for x in significant]);
    return [x[0] for x in significant];

window_nm = 'img_cntrls'
cv2.namedWindow(window_nm)
cv2.createTrackbar('blur_size', window_nm, 13 , 21, nothing)
# cv2.createTrackbar('blur_size', window_nm, 13 , 101, nothing)
cv2.createTrackbar('canny_high', window_nm, 200 , 250, nothing)
cv2.createTrackbar('canny_low', window_nm, 50 , 250, nothing)

# file_name = 'WIN_20161025_16_46_54_Pro'
file_name = 'WIN_20161025_16_54_51_Pro'
# file_name = 'WIN_20161025_16_56_51_Pro'
# file_name = 'WIN_20161025_17_01_08_Pro'
# file_name = 'WIN_20161025_17_02_21_Pro'
# file_name = 'WIN_20161025_17_05_50_Pro'
# file_name = 'WIN_20161025_17_06_56_Pro'
# img = cv2.imread('0008-0407-2011-1313_littering_pop_can_on_grass_pics_pictures_photos.jpg')
video_capture = cv2.VideoCapture(file_name+'.mp4')
# video_writer = cv2.VideoWriter('WIN_20161025_16_54_51_Pro_processed.mp4', cv2.cv.CV_FOURCC('H','2','6','4'), 29, (1280,720), 1)
# video_writer = cv2.VideoWriter('WIN_20161025_16_54_51_Pro_processed.mp4', -1, 29, (1280,720), 1)
# video_writer = cv2.VideoWriter(file_name+'_processed.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 29, (1280,720), 1)

fgbg = cv2.BackgroundSubtractorMOG2()

frame_skip_factor = 10
frame_count = 0
while True:
    frame_count += 1
    ret, img = video_capture.read()
    if (ret == True):
        if frame_count%frame_skip_factor == 0:

            canny_high = cv2.getTrackbarPos('canny_high',window_nm)
            canny_low = cv2.getTrackbarPos('canny_low',window_nm)

            blur_size = cv2.getTrackbarPos('blur_size',window_nm)
            blur_size = make_odd(blur_size)

            # blurred = cv2.GaussianBlur(img, (blur_size, blur_size), 0) # Remove noise
            # blurred = cv2.GaussianBlur(img, (blur_size, blur_size), 0) # Remove noise
            # blurred = cv2.medianBlur(np.uint8(img), (blur_size, blur_size)) # Remove noise
            blurred = cv2.medianBlur(np.uint8(img), blur_size) # Remove noise
            # blurred = cv2.blur(img, (blur_size, blur_size))

            # img_grey = imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # edgeImg = cv2.Canny(blurred,canny_low,canny_high)

            fgmask = fgbg.apply(blurred)
            # fgmask = fgbg.apply(img)

            findSignificantContours(img, fgmask)

            cv2.imshow('Orig',img)
            # cv2.imshow('Blurred',blurred)
            # cv2.imshow('edgeImg',edgeImg)
            # cv2.imshow('frame',fgmask)
            # video_writer.write(img)

    else:
        # video_capture.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO,0)
        # video_writer.release()
        video_capture.release()
        cv2.destroyAllWindows()
        exit()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
# video_writer.release()
video_capture.release()
cv2.destroyAllWindows()
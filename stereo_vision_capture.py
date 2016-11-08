import numpy as np
import cv2
import math
import datetime

file_name = repr(datetime.datetime.now())

# video_writer_right = cv2.VideoWriter(file_name+'_right.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 29, (1280,960), 1)
# video_writer_left = cv2.VideoWriter(file_name+'_left.avi', cv2.cv.CV_FOURCC('M','J','P','G'), 29, (1280,720), 1)

video_writer_right = cv2.VideoWriter(file_name+'_right.avi', -1, 29, (1280,720), 1)
video_writer_left = cv2.VideoWriter(file_name+'_left.avi', -1, 29, (1280,720), 1)


video_capture_right = cv2.VideoCapture(2)
video_capture_right.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
video_capture_right.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
video_capture_left = cv2.VideoCapture(1)
video_capture_left.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)
video_capture_left.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, img_right = video_capture_right.read()
    ret, img_left = video_capture_left.read()
    if (ret == True):

        cv2.imshow('right',img_right)
        cv2.imshow('left',img_left)
        video_writer_right.write(img_right)
        video_writer_left.write(img_left)

    else:
        # video_capture.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO,0)
        # video_writer.release()
        # video_capture.release()
        # cv2.destroyAllWindows()
        exit()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_writer_right.release()
video_writer_left.release()
video_capture_right.release()
video_capture_left.release()
cv2.destroyAllWindows()
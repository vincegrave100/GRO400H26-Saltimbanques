from __future__ import print_function
import cv2 as cv
import numpy as np

max_value = 255
max_value_H =360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)

def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)

def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)

def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)

def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)

def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

cap = cv.VideoCapture(0,cv.CAP_V4L2)
cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)

while True:
    ret, frame = cap.read()
    #print (ret, frame)
    if not ret:
        print("Errreur camera")
        break
    #blur channel
    blur = cv.GaussianBlur(frame, (3, 3), 0)

    vid_gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    frame_HSV = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    #frame_threshold = cv.inRange(blur, (low_H, low_S, low_V), (high_H, high_S, high_V))
    ret, thresh = cv.threshold(vid_gray, 150, 255, cv.THRESH_BINARY)

    #detect the contours on the binary image using cv.CHAINE_APPROX_NONE
    contours, hierrarchy = cv.findContours( image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_SIMPLE)
    contours1, hierrarchy1 = cv.findContours(image=thresh, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

    #draw contours on the original vid
    vid_copy_none = frame.copy()
    vid_copy_simple = frame.copy()

    cv.drawContours(image=vid_copy_none, contours=contours, contourIdx=-1,color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)
    cv.drawContours(image=vid_copy_simple, contours=contours, contourIdx=-1,color=(0, 255, 0), thickness=2, lineType=cv.LINE_AA)

    #creation de masques locaux

    #cv.imshow("filtreHSV", frame_HSV)
    cv.imshow(window_capture_name, frame)
    cv.imshow(window_detection_name, thresh)
    cv.imshow("detection contour none", vid_copy_none)
    cv.imshow("detection contour simple", vid_copy_simple )

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break
    #Ferme le programme lorsque la fenetre est fermee
    if cv.getWindowProperty("Camera", 0) >= 1:
        break

cap.release()
cv.destroyAllWindows()
cv.createTrackbar(low_H_name, window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name, high_H, max_value, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)


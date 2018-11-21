import cv2
import numpy as np
import math

video_capture = cv2.VideoCapture(0)
video_capture.set(3,160)
video_capture.set(4,120)

while(True):
  ret,frame=video_capture.read()
  crop_image=frame[60:120,0:160]
  gray=cv2.cvtColor(crop_image,cv2.COLOR_BGR2GRAY)
  blur=cv2.GaussianBlur(gray,(5,5),0)
  ret,thresh=cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
  contours,hierarchy=cv2.findContours(thresh.copy(),1,cv2.CHAIN_APPROX_NONE)
  
  if len(contours) > 0:
    c = max(contours, key=cv2.contourArea)
    M=cv2.moments(c)
    y = c[0:34]
    cx=int(M['m10']/M['m00'])
    cy=int(M['m01']/M['m00'])
    cv2.line(crop_image,(cx,0),(cx,720),(255,0,0),1)
    cv2.line(crop_image,(0,cy),(1280,cy),(255,0,0),1)
    cv2.drawContours(crop_image, contours,-1, (255,0,0), 1)
    p = y[1][0]

    x1=y[0][0][0]
    x2=y[1][0][0]

    y1=y[0][0][1]
    y2=y[1][0][1]

    u = abs((y2 - y1)/(x2 - x1))

    l = math.atan(u)

    l = l*(180/3.141)

    l = 90 - l

    print(l)
  else:   
    print("No line!!")
  cv2.imshow("frame",crop_image)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
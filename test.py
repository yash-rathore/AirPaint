'''
detect object color using hsv => make mask => make a contour around it => detect center => store coordinates => display things on screen and divide screen in such a way
that getting coordinates is evenly distributed => Put text => check whether you can identify when specific coordinate is in that section of screen => enter those points is
deque => using for loops display k-1th and kth points as straight lines.
'''

import cv2
import numpy
from collections import deque


def nothing(x):
    print("")


bars = cv2.namedWindow("bars")

col=[(0, 255, 255),(255, 0, 0),(0, 0, 0),(0, 255, 0),(150, 0, 255),(0, 0, 255),(255, 255, 0)]
#       yellow         blue      black    green          pink          red        cyan

# trackbars to set own color of blanket
cv2.createTrackbar("upper_hue", "bars", 30, 180, nothing)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, nothing)
cv2.createTrackbar("upper_value", "bars", 255, 255, nothing)
cv2.createTrackbar("lower_hue", "bars", 20, 180, nothing)
cv2.createTrackbar("lower_saturation", "bars", 100, 255, nothing)
cv2.createTrackbar("lower_value", "bars", 100, 255, nothing)

# paintwindow canvas
paintWindow = numpy.zeros((480, 640, 3)) + 255
# describing areas of color changing on paint window
cv2.rectangle(paintWindow, (20, 10), (155, 60), col[2], 2)
cv2.rectangle(paintWindow, (175, 10), (310, 60), col[1], -1)
cv2.rectangle(paintWindow, (330, 10), (465, 60), col[3], -1)
cv2.rectangle(paintWindow, (485, 10), (620, 60), col[5], -1)

cv2.rectangle(paintWindow, (20, 70), (155, 120), col[0], -1)
cv2.rectangle(paintWindow, (175, 70), (310, 120), col[2], -1)
cv2.rectangle(paintWindow, (330, 70), (465, 120), col[4], -1)
cv2.rectangle(paintWindow, (485, 70), (620, 120), col[6], -1)

bpoints = [deque(maxlen=1024)]#maxlen is used because when an element is added to left , element is removed from right side and vice versa
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
cpoints = [deque(maxlen=1024)]
ppoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
blpoints = [deque(maxlen=1024)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
cyan_index = 0
pink_index = 0
black_index = 0

color_index = 0


# kernel used for dilation and smoothening  of mask

kernel = numpy.ones((5, 5), numpy.uint8)

cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.rectangle(frame, (20, 10), (155, 60), col[2], 2)
    cv2.rectangle(frame, (175, 10), (310, 60), col[1], -1)
    cv2.rectangle(frame, (330, 10), (465, 60), col[3], -1)
    cv2.rectangle(frame, (485, 10), (620, 60), col[5], -1)

    cv2.rectangle(frame, (20, 70), (155, 120), col[0], -1)
    cv2.rectangle(frame, (175, 70), (310, 120), col[2], -1)
    cv2.rectangle(frame, (330, 70), (465, 120), col[4], -1)
    cv2.rectangle(frame, (485, 70), (620, 120), col[6], -1)

    upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
    upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
    upper_value = cv2.getTrackbarPos("upper_value", "bars")
    lower_value = cv2.getTrackbarPos("lower_value", "bars")
    lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
    lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")

    upper_hsv = numpy.array([upper_hue, upper_saturation, upper_value])
    lower_hsv = numpy.array([lower_hue, lower_saturation, lower_value])

    cv2.putText(paintWindow, 'Clear', (49, 43), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, 'Clear', (49, 43), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # creating mask
    # Identifying the pointer by making its mask
    Mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    # how to create contour around the mask , a circle
    contours, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None

    if len(contours) > 0:  # if contour size is actually large enough to draw
        cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]

        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
        cv2.circle(frame, (int(x), int(y)), 1, (0, 0, 255), 2)

        # finding center of circle, and getting coordinates of center
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        center = (cx, cy)
        cv2.circle(frame, center, int(radius), (0, 0, 255), 2)
        if cy < 120:  # if not in drawing area , only in color selection area
            if 20 < cx < 155 and 10 < cy < 60:  # clear
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                cpoints = [deque(maxlen=512)]
                ppoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                blpoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                cyan_index = 0
                pink_index = 0
                black_index = 0
                paintWindow[67:, :, :] = 255
            #       yellow0         blue1      black2    green3          pink4          red5        cyan6
            if 20 < cx < 155 and 70 < cy < 120:  # yellow
                color_index = 0

            if 175 < cx < 310 and 10 < cy < 60:  # blue
                color_index = 1

            if 175 < cx < 310 and 70 < cy < 120:  # black
                color_index = 2

            if 330 < cx < 465 and 10 < cy < 60:  # green
                color_index = 3

            if 330 < cx < 465 and 70 < cy < 120:  # pink
                color_index = 4

            if 485 < cx < 620 and 10 < cy < 60:  # red
                color_index = 5

            if 485 < cx < 620 and 70 < cy < 120:  # cyan
                color_index = 6
        else:  # when in drawing area
            #       yellow0         blue1      black2    green3          pink4          red5        cyan6

            if color_index == 0:
                ypoints[yellow_index].appendleft(center)
            elif color_index == 1:
                bpoints[blue_index].appendleft(center)
            elif color_index == 2:
                blpoints[black_index].appendleft(center)
            elif color_index == 3:
                gpoints[green_index].appendleft(center)
            elif color_index == 4:
                ppoints[pink_index].appendleft(center)
            elif color_index == 5:
                rpoints[red_index].appendleft(center)
            elif color_index == 6:
                cpoints[cyan_index].appendleft(center)

    else:  # when contours are not big enough to draw , we simply append the next deques to avoid messing up
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1
        blpoints.append(deque(maxlen=512))
        black_index += 1
        ppoints.append(deque(maxlen=512))
        pink_index += 1
        cpoints.append(deque(maxlen=512))
        cyan_index += 1

    # now actually drawing the points => draw k-1 and k th point together, if either of those are none (when contours not detected) => dont draw anything
    #       yellow0         blue1      black2    green3          pink4          red5        cyan6
    points = [ypoints,bpoints,blpoints,gpoints,ppoints,rpoints,cpoints]
    for i in range(len(points)):  # i gives the index of deque color eg)1,2,3
        for j in range(len(points[i])):  # j gives color and also deque for it eg)bpoints,gpoints,rpoints
            for k in range(1,len(points[i][j])):# k gives the coordinates in form of tuples eg(122,256)
                if points[i][j][k-1] == None or points[i][j][k] == None: #if either of points in deques are None , it does not draw anything
                    continue
                #code to draw lines out of k-1 and k th point over and over again
                cv2.line(paintWindow, points[i][j][k-1], points[i][j][k], col[i], 2)
                cv2.line(frame, points[i][j][k-1], points[i][j][k], col[i], 2)

    cv2.imshow("live", frame)
    cv2.imshow("mask detect", Mask)
    cv2.imshow("PaintWindow", paintWindow)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

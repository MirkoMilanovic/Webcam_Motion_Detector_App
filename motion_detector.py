"""
The Webcam_Motion_Detector_App can catch any motion with the Webcam which gets triggered as soon as the program starts.
The exact "start" and "end" that the object appeared in are saved in an external file. 

MOTION DETECTION:
1. trigger the web-cam (the first frame should be the static background - base img - movement is different than that)
        - with "first_frame = None", "if first_frame is None:", we catch the first frame
        - we use continue to start the new iteration
2. grayout the image and the base image
3. comparing -  two images, you get the result picture (showing the motion in white)
        - we use gaussian filter to smooth the images, to reduce the noise, and then the difference:
            cv2.GaussianBlur(gray, (21, 21), 0) - img, gaussian kernel 21x21, standard deviation-commonly used 0
        - we make a delta_frame as a absolute difference of two frames:
            cv2.absdiff(first_frame, gray)
4. make a treshold to make a only black and white inside the loop:
            cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        - of the delta frame, with a threshold=30, maxvalue=255, binary threshold method
        (you get a tuple of 2 values, the first one is used for other methods, and the second is frame)
5. to kick out small black areas inside the white areas, to smooth out the thresh_frame
            thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        - thrash frame we smooth with no kernel, 2 iteratations used (more->smoother)
6. find the contours of the white parts of the img
            (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            (cnts,_) - it depends on the cv2/cv3, p2/p3
        - to find a contours of the image we use copy of the frame, not to modify it, retrieve ext. is
        the method to get external lines, and a method for  approximation
7. make a for loop for the contours, if the area is too small, not to consider it
        - we need to iterate through the extracted contours, to exclude the small ones (small areas):
        "if cv2.contourArea(contour) < 1000: .... continue"; continue-break the iteration and continue the loop,
8. draw the rectangles over the big white areas, that are shown over the current video (frame)
        "(x, y, w, h) = cv2.boundingRect(contour)" - we extract the rectangle values of the bounding rectangle
9. the time when the object enters/exits the screen

"""
import cv2, time

first_frame = None
video = cv2.VideoCapture(0)


while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = gray
        cv2.imshow("First frame", gray)
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:      
        if cv2.contourArea(contour) < 1000:
            continue      
        (x, y, w, h) = cv2.boundingRect(contour)  
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("Video", gray)
    cv2.imshow("Threshold frame", thresh_frame)
    cv2.imshow("Difference", delta_frame)
    cv2.imshow("Color frame", frame)

    key = cv2.waitKey(20)
    if key == ord('q'):
        break


video.release()
cv2.destroyAllWindows()
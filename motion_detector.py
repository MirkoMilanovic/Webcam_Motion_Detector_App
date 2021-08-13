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
4. make a treshold to make a only black and white inside the loop
5. find the contours of the white parts of the img
6. make a for loop for the contours, if the area is too small, not to consider it
7. draw the rectangles over the big white areas, that are shown over the current video (frame)
8. the time when the object enters/exits the screen

"""
import cv2, time

first_frame = None
video2 = cv2.VideoCapture(0)
time.sleep(3)
video = cv2.VideoCapture(0)


while True:
    check, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = gray
        cv2.imshow("First frame", gray)
        continue

    cv2.imshow("Video", gray)

    delta_frame = cv2.absdiff(first_frame, gray)
    cv2.imshow("Difference", delta_frame)

    key = cv2.waitKey(20)
    if key == ord('q'):
        break


video.release()
cv2.destroyAllWindows()
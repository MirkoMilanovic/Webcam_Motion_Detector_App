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
9. the time when the object enters/exits the screen:
        We want to make a excel file with times, for every entrance in front of the camera to write start/exit time
        - we need to see in the code where are the moments of the start and stop of the motion, so we make a
        variable status=0, but when motion occures, then change it to 1
        - when status changes "0 -> 1 = record START time" and "1 -> 0 = record END time"
        - we make a list of all statuses [0000011110001111111111], we look a sample of the last two items, if they
        are the same, don't do anything, if they change from 0-1 or 1-0, record time (if statement, datetime.now()),
        we put those recorded times in a new list of times.
        - we get an error, that we can't get values from the list, so we make first two elements like [None, None]
        - we want to make sure that the end of the recording, records the exit time, if status is 1
        - throw the list of times in a pandas dataframe, and then to CSV file. We need that to put the data in EXCEL,
        first we need empty pandas dataframe with columns Start, End, and when we create the times list,
        outside the loop, we append those times in the pandas dataframe, we need a loop for appending
        - the list of statuses (list full of 0 and 1) is getting too long over time of the recording. So we change
        the list overwritting it with a list containing only two last elements, before the list is used:

            status_list = status_list[-2:]      - this is memory efficient

MAKING A PLOT:
First we need to think of the structure of our script. We need to think about:
- which plot to use? ...We will use quadrant
- what are the input parameters? ...We have them in a dataframe with datetimes (which we save to csv)

"""
import cv2, time, pandas
from datetime import datetime

first_frame = None
video = cv2.VideoCapture(0)
waiting = True
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])

while True:
    check, frame = video.read()
    status = 0

    if waiting is True:
        time.sleep(5)
        check, frame = video.read()
        waiting = False
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if first_frame is None:
        first_frame = gray
        cv2.imshow("First frame", gray)
        continue

    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 70, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    cv2.imshow("Video", gray)
    cv2.imshow("Threshold frame", thresh_frame)
    cv2.imshow("Difference", delta_frame)
    cv2.imshow("Color frame", frame)

    key = cv2.waitKey(20)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

    print(status)

print(status_list)
print(times)

for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()
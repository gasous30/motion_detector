import cv2, time
from datetime import datetime
import pandas as pd

camera_port = 1 # 0 for integrated, 1 for external
video = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)

times = []
status_list = [None,None,0]
first_frame = None
df = pd.DataFrame(columns=['Start','End'])
while True:

    if first_frame is None:
        t = 0
        while t < 4:
            check, frame = video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, ksize=(21,21), sigmaX=0)
            t = t + 1
            time.sleep(3)
            print(f'Calibrating... ', 4-t)
            first_frame=gray

        continue

    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, ksize=(21,21), sigmaX=0)
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame,thresh=50, maxval=255, type=cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, kernel=None, iterations=5)

    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)

    status_list.append(status)
    status_list = status_list[-2:]
    if not status_list[-1] == status_list[-2]:
        times.append(datetime.now())

    # cv2.imshow('First Frame', first_frame)
    # cv2.imshow('Gray Frame', gray)
    cv2.imshow('Color Frame', frame)
    # cv2.imshow('Delta Frame', delta_frame)
    # cv2.imshow('Threshold Frame', thresh_frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({'Start':times[i], 'End': times[i+1]}, ignore_index=True)

df.to_csv('Times.csv')

video.release()
cv2.destroyAllWindows()
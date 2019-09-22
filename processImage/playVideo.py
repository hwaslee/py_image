import sys
import cv2
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil


cap = cv2.VideoCapture('BotInsight_M7_L3.mp4')
if not cap.isOpened():
    print("already open..")
    print("so, exit..")
    exit(0)

timer = timeutil.TimeElapsed()
count = 0

frametimer = timeutil.TimeElapsed()
framepos = 0.0
while True:
    # 읽을 frame 위치를 지정
    cap.set(cv2.CAP_PROP_POS_FRAMES, framepos)
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    # 파일 속성 FPS 당 1 frame만 점검
    framepos = framepos + cv2.CAP_PROP_FPS

    count = count + 1
    print(count, cap.get(cv2.CAP_PROP_POS_FRAMES), "frame elapsed..[", frametimer.getelapsed(), "]")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

'''
frametimer = timeutil.TimeElapsed()
for cnt in range(1000):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    numOfFrame = numOfFrame + 1
    print("frame elapsed..[", frametimer.getelapsed(), "]")
'''

print("done..")
print("Total elapsed time: ", timer.getelapsed(), ", Count:", count)
print("파일 현재 위치(초), CAP_PROP_POS_MSEC(sec):", cap.get(cv2.CAP_PROP_POS_MSEC)/1000)
print("전체 frame 갯수, CAP_PROP_FRAME_COUNT:", cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("현재 frame 위치, CAP_PROP_POS_FRAMES:", cap.get(cv2.CAP_PROP_POS_FRAMES))
print("frame rate,    CAP_PROP_FPS:", cap.get(cv2.CAP_PROP_FPS))

cap.release()
cv2.destroyAllWindows()
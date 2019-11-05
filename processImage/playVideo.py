import sys
import cv2
sys.path.insert(1, '/Users/andrew/Documents/py_basic/util')
import timeutil


# def video_info(infilename):
#     cap = cv2.VideoCapture(infilename)
#
#     if not cap.isOpened():
#         print("could not open :", infilename)
#         exit(0)
#
#     length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#
#     print('length : ', length)
#     print('width : ', width)
#     print('height : ', height)
#     print('fps : ', fps)


# cap = cv2.VideoCapture('BotInsight_M7_L3.mp4')
# cap = cv2.VideoCapture('/Volumes/NO NAME/20191021 영상기술검수 에러반려 예시/video black/N2018010300026_기술검수반려 [M]제왕수산 갈치  뷰티_갈치조림 (수정).MXF')
cap = cv2.VideoCapture('/Volumes/NO NAME/20191021 영상기술검수 에러반려 예시/video black/N2018010800080_기술검수반려 [M]AHC 아이크림 시즌6_인포.MXF')
if not cap.isOpened():
    print("already open..")
    print("so, exit..")
    exit(0)


timer = timeutil.TimeElapsed()
count = 0

frametimer = timeutil.TimeElapsed()
framepos = 0.0
stop_flag = False
while True:
    if stop_flag:
        break

    # 읽을 frame 위치를 지정
    cap.set(cv2.CAP_PROP_POS_FRAMES, framepos)
    ret, frame = cap.read()ㅜ
    if not ret:
        break

    # cur_pos = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    # if cur_pos < 17.8 or cur_pos > 18.9:
    #     framepos = framepos + 1
    #     continue

    # N2018010300026_기술검수반려.. 554 frame에서 약간 이상한 것 보임
    if framepos > 30 or framepos < -1:
        framepos = framepos + 1
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    # 파일 속성 FPS 당 1 frame만 점검
    # framepos = framepos + cv2.CAP_PROP_FPS
    framepos = framepos + 1

    count = count + 1
    print('{:4d} {:4d}th frame, {} sec elapsed'.format(count, int(cap.get(cv2.CAP_PROP_POS_FRAMES)), frametimer.getelapsed()))

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_flag = True
            break
        if cv2.waitKey(1) & 0xFF == ord('n'):
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
print()

print("전체 frame width, CAP_PROP_FRAME_WIDTH:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("전체 frame width, CAP_PROP_FRAME_WIDTH:", int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("전체 frame height, CAP_PROP_FRAME_HEIGHT:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("전체 frame height, CAP_PROP_FRAME_HEIGHT:", int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

print("전체 frame 갯수, CAP_PROP_FRAME_COUNT:", cap.get(cv2.CAP_PROP_FRAME_COUNT))
print("전체 frame 갯수, CAP_PROP_FRAME_COUNT:", int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
print("현재 frame 위치, CAP_PROP_POS_FRAMES:", cap.get(cv2.CAP_PROP_POS_FRAMES))
print("frame rate,    CAP_PROP_FPS:{:.2f}".format(cap.get(cv2.CAP_PROP_FPS)))
print("파일 현재 위치(초), CAP_PROP_POS_MSEC(sec):", cap.get(cv2.CAP_PROP_POS_MSEC)/1000)


cap.release()
cv2.destroyAllWindows()
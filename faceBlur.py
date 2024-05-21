import cv2
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector


def blur(img,k):
    h,w = img.shape[:2]
    kh,kw = h//k,w//k
    if kh%2==0:
        kh-=1
    if kw%2==0:
        kw-=1
    img = cv2.GaussianBlur(img,ksize=(kh,kw),sigmaX=0)
    return img


def pixelate_face(image, blocks=10):
    # divide the input image into NxN blocks
    (h, w) = image.shape[:2]
    xSteps = np.linspace(0, w, blocks + 1, dtype="int")
    ySteps = np.linspace(0, h, blocks + 1, dtype="int")
    # loop over the blocks in both the x and y direction
    for i in range(1, len(ySteps)):
        for j in range(1, len(xSteps)):
            # compute the starting and ending (x, y)-coordinates
            # for the current block
            startX = xSteps[j - 1]
            startY = ySteps[i - 1]
            endX = xSteps[j]
            endY = ySteps[i]
            # extract the ROI using NumPy array slicing, compute the
            # mean of the ROI, and then draw a rectangle with the
            # mean RGB values over the ROI in the original image
            roi = image[startY:endY, startX:endX]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(image, (startX, startY), (endX, endY),
                (B, G, R), -1)
    # return the pixelated blurred image
    return image


factor = 3
cap = cv2.VideoCapture(0)
width = 1000
height = 720
cap.set(3,width)
cap.set(4,height)
detector = FaceMeshDetector(maxFaces=2)

while 1:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame, faces = detector.findFaceMesh(frame, draw=False)
    # 103, 332, 172, 197
    try:
        for face in faces:
            # print(face)
            x,y = face[103][0] - 75, face[103][1] - 75
            w = face[332][0] + 50
            h = face[172][1] + 50
            # print(x,y,w,h)
            # cv2.line(frame, (30, 0), (30,470), (255,0,255), 2)
            # print(face)
            if x <= 0 or x >= width or y <= 0 or y >= height:
                cv2.rectangle(frame, (x,y), (w,h), (255,0,255), -1)
            frame[y:h,x:w] = pixelate_face(blur(frame[y:h,x:w],factor))
    except:
        pass

    cv2.imshow('Live',frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()
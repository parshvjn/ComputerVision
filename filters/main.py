import cv2
cap = cv2.VideoCapture(0)
def cartoonize (image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  blurImage = cv2.medianBlur(image, 1)

  edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

  color = cv2.bilateralFilter(image, 9, 200, 200)

  cartoon = cv2.bitwise_and(color, color, mask = edges)

  return cartoon

while True:
  success, img = cap.read()
  img = cartoonize(img)
  cv2.imshow('camera', img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
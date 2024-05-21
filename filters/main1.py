import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def dodge(front: np.ndarray, back: np.ndarray) -> np.ndarray:
  result = back * 255.0 / (255.0 - front)
  result[result > 255] = 255
  result[back == 255] = 255
  return result.astype('uint8')

while True:
  success, img = cap.read()
  grayscale = np.array(np.dot(img[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)
  grayscale = np.stack((grayscale,) * 3, axis=-1)
  inverted_img = 255 - grayscale
  blur_img = cv2.GaussianBlur(inverted_img, ksize=(0, 0), sigmaX=5)
  final_img = dodge(front=blur_img, back=grayscale)
  cv2.imshow('camera', final_img)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()
cv2.destroyAllWindows()
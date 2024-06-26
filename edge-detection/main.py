import cv2
import numpy as np

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture(0)

# Read the video
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Converting the image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Using the Canny filter to get contours
        edges = cv2.Canny(gray, 100, 200, 3, L2gradient=True)
        # Using the Canny filter with different parameters
        edges_high_thresh = cv2.Canny(gray, 60, 120)
        # Stacking the images to print them together
        # For comparison
        # images = np.hstack((gray, edges, edges_high_thresh))

        # Display the resulting frame
        cv2.imshow('Frame', edges_high_thresh)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
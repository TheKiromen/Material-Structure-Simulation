import cv2 as cv
import numpy as np

# Colors associated with microstructure grains
# First one is black, it signifies no grain at all
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
          (255, 0, 255), (125, 125, 255), (125, 255, 125), (255, 125, 125)]

# Load the image
image = cv.imread(r'output/Output.png')

# Create color mask
mask = cv.inRange(image, colors[1], colors[1])
# Apply the mask
masked_img = cv.bitwise_and(image, image, mask=mask)

# Convert image to gray
grayscale = cv.cvtColor(masked_img, cv.COLOR_BGR2GRAY)
# Bin the image
flag, binned = cv.threshold(grayscale, 10, 255, cv.THRESH_BINARY)
# Find contours
contours, hierarchy = cv.findContours(binned, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# Draw the contours
result = np.zeros(image.shape)
cv.drawContours(result, contours, -1, (255, 255, 255), 1)

# Display the result
cv.imshow("Image", result)
cv.waitKey(0)

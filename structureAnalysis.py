import cv2 as cv
import numpy as np

# Colors associated with microstructure grains
# First one is black, it signifies no grain at all
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
          (255, 0, 255), (125, 125, 255), (125, 255, 125), (255, 125, 125)]
global_contours = []
global_hierarchy = []

# Load the image
image = cv.imread(r'output/Output.png')

for i in range(1, 10):
    # Create color mask
    mask = cv.inRange(image, colors[i], colors[i])
    # Apply the mask
    masked_img = cv.bitwise_and(image, image, mask=mask)

    # Convert image to gray
    grayscale = cv.cvtColor(masked_img, cv.COLOR_BGR2GRAY)
    # Bin the image
    flag, binned = cv.threshold(grayscale, 10, 255, cv.THRESH_BINARY)
    # Find contours from single channel
    color_contours, hierarchy = cv.findContours(binned, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Save found contours
    global_contours.append(color_contours)
    global_hierarchy.append(hierarchy)

    # Display single colored grains
    cv.imshow("Image", masked_img)
    cv.waitKey(0)

# # Create empty image
# result = np.zeros(image.shape)
# # Draw all contours onto the image
# for contour in global_contours:
#     cv.drawContours(result, contour, -1, (255, 255, 255), 1)
# # Display the result
# cv.imshow("All contours", result)

cv.waitKey(0)
cv.destroyAllWindows()

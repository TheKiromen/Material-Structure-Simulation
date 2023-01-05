import csv

import cv2 as cv
import numpy as np

# Colors associated with microstructure grains
# First one is black, it signifies no grain at all
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
          (255, 0, 255), (125, 125, 255), (125, 255, 125), (255, 125, 125)]
# Data from all grains in the image
global_contours = []
global_hierarchy = []

# Load the image
image = cv.imread(r'output/mesh_src.png')
image = cv.resize(image, (700, 700), interpolation=cv.INTER_NEAREST_EXACT)

# Create csv file for data storage
f = open(r'output/data.csv', 'w', encoding="UTF-8", newline='')
writer = csv.writer(f)
writer.writerow(["ID", "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10"])

labeled_image = image.copy()

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
    # cv.imshow("Window", masked_img)
    # cv.waitKey(0)

# Create empty image
result = np.zeros(image.shape)
i = 0
# Draw all contours onto the image
for contour in global_contours:
    for c in contour:
        # Label the image
        rect = cv.minAreaRect(c)[0]
        cx = int(rect[0])
        cy = int(rect[1])
        cv.putText(labeled_image, text=str(i), org=(cx - 7, cy + 5), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.3,
                   color=(0, 0, 0), thickness=1, lineType=cv.LINE_AA)
        i += 1

        params = [i, i*2, i*4]

        # Calculate grain parameters
        # W1 
        # W2
        # W3
        # W4
        # W5
        # W6
        # W7
        # W8
        # W9
        # W10

        # Save all params as CSV
        writer.writerow(params)

    # Draw contours for preview
    # cv.drawContours(result, contour, -1, (255, 255, 255), 1)

# Save the labeled image
cv.imwrite(r'output/labeled_image.png', labeled_image)

# Close and save csv data file
f.close()

# Display the result
# cv.imshow("Window", result)
cv.imshow("Window", labeled_image)

# Close the preview
cv.waitKey(0)
cv.destroyAllWindows()

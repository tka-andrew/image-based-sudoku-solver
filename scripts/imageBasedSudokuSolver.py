import cv2
import numpy as np

IMAGE_PATH = "/src/ImageBasedSudokuSolver/images/sudoku/sudoku04.jpg"

img = cv2.imread(IMAGE_PATH)

# rescale image
height = img.shape[0]
width = img.shape[1]
new_height = 960
scale_factor = new_height/height # adjust scale according to new height
new_width = int(width * scale_factor)
dimensions = (new_width, new_height)
img = cv2.resize(img, dimensions, interpolation=cv2.INTER_LINEAR)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)

# perform dilation to make the lines more visible
kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8)
thresh = cv2.dilate(thresh, kernel)

# cv2.RETR_EXTERNAL = only find the most external contours, excluding enclosed ones
# cv2.CHAIN_APPROX_SIMPLE = only store few points of the contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

approxContours = [] # approximate contours

# each contour stores a list of coordinates
# supposeqdly a perfect contour with 4 sides should have only 4 points
# but I put up to 20 for some tolerance, then afterwards the approxPolyDP will do 2nd time filtering
for contour in contours:
    if (len(contour) < 20): # first layer of filtering
        perimeter = cv2.arcLength(contour,True)
        epsilon = 0.02*perimeter # maximum distance from contour to approximated contour
        approx = cv2.approxPolyDP(contour,epsilon,True)
        approxContours.append(approx)

filteredContours = []
for contour in approxContours:
    if (len(contour) ==4): # if the contour is a polygon with 4 sides
        filteredContours.append(contour)

# find the biggest
filteredContours = sorted(filteredContours, key=cv2.contourArea, reverse=True) # sort according to contourArea in descending order
biggestContour = filteredContours[0]

# find topLeft(x,y) and bottomRight(x,y) of the biggestContour
topLeftX = new_width
topLeftY = new_height
bottomRightX = 0
bottomRightY = 0
for points in biggestContour:
    point = points[0] # due to points is something like [[ 13 211]]
    if point[0] < topLeftX:
        topLeftX = point[0]
    if point[0] > bottomRightX:
        bottomRightX = point[0]
    if point[1] < topLeftY:
        topLeftY = point[1]
    if point[1] > bottomRightY:
        bottomRightY = point[1]

## the [] around biggestContour is necessary as now there is only one contour
#cv2.drawContours(img, [biggestContour], -1, (0, 255, 0), 3)

# crop the image based on the topLeft(x,y) and bottomRight(x,y) of the biggestContour
sudoku_thresh = thresh[topLeftY:bottomRightY, topLeftX:bottomRightX]

# further dilate to make the lines more visible, so that later we can get exactly 81 squares
kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]],np.uint8)
dilated_sudoku = cv2.dilate(sudoku_thresh, kernel)
dilated_sudoku = cv2.dilate(dilated_sudoku, kernel)

# inverse the binary image, to switch our area of interest (white contours) into the inner squares
dilated_sudoku = cv2.bitwise_not(dilated_sudoku)
fakeRGB_sudoku = cv2.cvtColor(sudoku_thresh, cv2.COLOR_GRAY2RGB)
cells_contours, hierarchy = cv2.findContours(dilated_sudoku, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# supposedly 81
print(len(cells_contours))

for cell in cells_contours:
    x,y,w,h = cv2.boundingRect(cell)
    cell_img = fakeRGB_sudoku[y:y+h, x:x+w]
    cv2.imshow("sudoku cell", cell_img)
    cv2.imwrite("/src/ImageBasedSudokuSolver/test.png", cell_img)
    cv2.waitKey(0) # Display the image infinitely until any keypress
    break

# c2 = thresh[topLeftY:topLeftY+50, topLeftX:topLeftX+50]

cv2.imshow("ROI", fakeRGB_sudoku)
cv2.waitKey(0) # Display the image infinitely until any keypress
cv2.destroyAllWindows()
import cv2
import numpy as np

from ImageProcessingHelper import *

IMAGE_PATH = "/src/ImageBasedSudokuSolver/images/sudoku/sudoku25.jpg"
TEMPLATE_PATH = "/src/ImageBasedSudokuSolver/templates/"

img = cv2.imread(IMAGE_PATH)

# rescale image
img, new_height, new_width = resizeImgToHeight(960, img)

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

template_list = ["template_1.png","template_2.png","template_3.png","template_4.png","template_5.png","template_6.png","template_7.png","template_8.png","template_9.png"]

sudoku_w, sudoku_h = sudoku_thresh.shape

grid = np.zeros([9,9])

for count, templateImgName in enumerate(template_list):
    template = cv2.imread(TEMPLATE_PATH + templateImgName)
    template =  cv2.cvtColor(template, cv2.COLOR_BGR2GRAY) # image read will be bgr, need to convert
    res = cv2.matchTemplate(sudoku_thresh,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9 # digit 3 and 8 very similar, we need high threshold
    w1 = template.shape[0]
    h1 = template.shape[1]
    loc = np.where( res >= threshold)
    # there will be multiple points here, some might overlap each other
    # but it's ok, the operation is idempotent as long as the digit recognition is correct
    for pt in zip(*loc[::-1]):
        # "//" means floor division
        grid_y = pt[0]*9//sudoku_w # (x,y) in grid and (x,y) in sudoku are different
        grid_x = pt[1]*9//sudoku_h # (x,y) in grid and (x,y) in sudoku are different
        grid[grid_x][grid_y] = count + 1

print(grid) # validate whether all the digit recognition are correct

cv2.imshow("ROI", fakeRGB_sudoku)
cv2.waitKey(0) # Display the image infinitely until any keypress
cv2.destroyAllWindows()
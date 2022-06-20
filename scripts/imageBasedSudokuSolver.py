import cv2
import numpy as np
import signal

from ImageProcessingHelper import *
from sudoku_solver import SudokuSolver

def timeout_handler(num, stack):
    raise TimeoutError

TEMPLATE_PATH = "/src/ImageBasedSudokuSolver/templates/"

def imageBasedSudokuSolver(imagePath, showImage):
    img = cv2.imread(imagePath)

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

    unsolvedGrid = grid.copy()

    print("\noriginal sudoku")
    print(unsolvedGrid) # validate whether all the digit recognition are correct
    solver = SudokuSolver()
    solver.solveSudoku(grid)
    print("\nsolved sudoku")
    print(grid) # validate whether the solved sudoku is correct

    # font
    font = cv2.FONT_HERSHEY_SIMPLEX  
    # fontScale
    fontScale = 1   
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2

    w_percell = sudoku_w//9
    h_percell = sudoku_h//9

    for i in range(0,9):
        for j in range(0,9):
            if (unsolvedGrid[i,j] == 0):
                # the origin is coordinates from bottom-left corner of the text
                # the w_percell*1//4 and h_perccell*3//4 are used to adjust the coordinate a little bit
                o_x = j*w_percell + w_percell*1//4
                o_y = i*h_percell + h_percell*3//4
                org = (o_x, o_y)
                fakeRGB_sudoku = cv2.putText(fakeRGB_sudoku, str(int(grid[i,j])), org, font, fontScale, color, thickness, cv2.LINE_AA)

    # REFERENCE: https://medium.com/@mh_yip/opencv-detect-whether-a-window-is-closed-or-close-by-press-x-button-ee51616f7088
    if (showImage):
        wait_time = 500
        cv2.namedWindow("solved sudoku", cv2.WINDOW_KEEPRATIO)
        cv2.imshow("solved sudoku", fakeRGB_sudoku)
        while cv2.getWindowProperty('solved sudoku', cv2.WND_PROP_VISIBLE) >= 1:
            keyCode = cv2.waitKey(wait_time)
            if (keyCode & 0xFF) == ord("q"):
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':

    # REFERENCE: https://medium.com/@chamilad/timing-out-of-long-running-methods-in-python-818b3582eed6
    signal.signal(signal.SIGALRM, timeout_handler)
    wait_timeout = 3
    signal.alarm(wait_timeout)

    try:
        imagePath = "/src/ImageBasedSudokuSolver/images/sudoku/sudoku05.jpg"
        target=imageBasedSudokuSolver(imagePath, True)
    except TimeoutError:
            print("\nTimeout! Probably this is due to poor digit recognition.\n")
    except:
        print("Unknown exception!")
    finally:
        signal.alarm(0)
    


    
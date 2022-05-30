# Image-based Sudoku Solver
This is an image-based sudoku solver project that takes an image as input, and then uses OpenCV to find out the Sudoku and transform it into a 2D vector, and then solve it and display a solved sudoku. 
The input images are screenshots of the games from the Sudoku game on Play Store. 
This project is developed on Docker container for better portability and application isolation.

This project is just a simple project with some contraints/assumptions such as:
    1) Input images are screenshots from the 'Sudoku' game available on PlayStore
    2) The font style of the digits are the same
    3) The sudoku is the biggest contour on the image

Based on the constraints/assumptions above, using OpenCV template matching is enough to perform digit recognition.

## Current status : Under development
1. Able to find ROI (sudoku)
2. Able to disect the sudoku into 81 contours
3. Saved Digit Templates
4. Validated that OpenCV template matching can be used for this application
5. Transformed the detected sudoku to 2D grid
6. Solve the sudoku and return a solved 2D grid

## TODO
1. Display the correct answer on the sudoku image
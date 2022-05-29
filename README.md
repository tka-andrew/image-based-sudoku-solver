# Image-based Sudoku Solver
This is an image-based sudoku solver project that takes an image as input, and then uses OpenCV to find out the Sudoku and transform it into a 2D vector, and then solve it and display a solved sudoku. 
The input images are screenshots of the games from the Sudoku game on Play Store. 
This project is developed on Docker container for better portability and application isolation.

## Current status : Under development
1. Able to find ROI (sudoku)
2. Able to disect the sudoku into 81 contours
3. Saved Digit Templates

## TODO
1. Try using OpenCV template matching to perform digit recognition
2. Transform the detected sudoku into a 2D vector
3. Solve the sudoku and return a solved 2D vector
4. Display the correct answer on the sudoku image
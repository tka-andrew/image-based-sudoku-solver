import cv2
import random
import string

def resizeImgToHeight(new_height:int, img):
    height = img.shape[0]
    width = img.shape[1]
    scale_factor = new_height/height # adjust scale according to new height
    new_width = int(width * scale_factor)
    dimensions = (new_width, new_height)
    return cv2.resize(img, dimensions, interpolation=cv2.INTER_LINEAR), new_height, new_width

def generateRandomImageName(prefix: string = None, postfix: string = None) -> string:
    # generate random 16 characters
    randomName = ''.join((random.choice(string.ascii_lowercase) for x in range(16))) #
    if prefix is not None:
        randomName = prefix + '_' + randomName
    if postfix is not None:
        randomName = randomName + '_' + postfix
    return randomName
        

def saveImage(img, absoluteDirectory: string, imgName, format: string) -> None:
    if not absoluteDirectory[-1] == "/":
        absoluteDirectory += "/"
    imgName = absoluteDirectory + imgName + format
    cv2.imwrite(imgName, img)

def saveContoursAsImages(contours, originalImg, absoluteDirectory: string, format: string) -> None:
    for cell in contours:
        x,y,w,h = cv2.boundingRect(cell)
        cell_img = originalImg[y:y+h, x:x+w]
        saveImage(cell_img, absoluteDirectory, generateRandomImageName(), format)
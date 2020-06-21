import cv2
import numpy as np 
import glob

def main():
    files = glob.glob("./1/tshirt3.jpg")
    for f in files:
        img = cv2.imread(f, 1)
        img = cv2.resize(img, (128, 128))
        img_sobel = cv2.Sobel(img, cv2.CV_8U, 0, 1)
        img_sobely = cv2.Sobel(img, cv2.CV_8U, 1, 0)
        abs_sobel = cv2.absdiff(img_sobel, img_sobely)
        # for i in range(1, 16):
        #     cv2.line(img, (i * 8, 0), (i * 8, 128), (0,255,0), 1)
        #     cv2.line(img, (0, i * 8), (128, i * 8), (0,255,0), 1)
        cv2.imwrite("test.jpg", img)
        cv2.imwrite("Sobel.png", img_sobel)
        cv2.imwrite("Sobely.png", img_sobely)
        cv2.imwrite("abs.png", abs_sobel)

if __name__ == "__main__":
    main()
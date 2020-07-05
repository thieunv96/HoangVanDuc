import cv2
import numpy as np 
import glob

def main():
    files = glob.glob("./vay/*.jpg")
    for f in files:
        img = cv2.imread(f, 1)
        img = cv2.resize(img , (128, 128))
        cv2.imwrite(f, img)

if __name__ == "__main__":
    main()
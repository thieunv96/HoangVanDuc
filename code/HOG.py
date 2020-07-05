import numpy as np
import cv2


def calculate_gradients(img):
    h, w = img.shape[0], img.shape[1]
    magnitude = np.zeros((h, w))
    direction = np.zeros((h, w))
    img = img.astype("float32")
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            pCu = img[y, x]
            # compute x direction
            pBx = img[y, x - 1]
            pFx = img[y, x + 1]
            Gx = pFx - pBx
            # compute y direction
            pBy = img[y - 1, x]
            pFy = img[y + 1, x]
            Gy = pFy - pBy
            # Magnitude
            G = np.sqrt(Gx * Gx + Gy * Gy)
            magnitude[y, x] = G
            D = 0 if Gy == 0 else np.arctan(Gx / Gy)
            D = D * 180.0 / np.pi
            D = D if D >= 0 else D + 180
            direction[y, x] = D
    return magnitude, direction


def calculate_hispercell(magnitude, direction, bin_num):
    
    if bin_num == 9:
        bins = (0, 20, 40, 60, 80, 100, 120, 140, 160)
        vote = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        bin_range = 20
    elif bin_num == 18:
        bins = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
                100, 110, 120, 130, 140, 150, 160, 170)
        vote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        bin_range = 10
    for x in range(magnitude.shape[1]):
        for y in range(magnitude.shape[0]):
            g = magnitude[x, y]
            d = direction[x, y]
            il = d // bin_range
            ih = 0 if il == (bin_num - 1) else il + 1
            divia = d - bins[int(il)]
            vote[int(il)] += (divia / bin_range) * g
            vote[int(ih)] += ((bin_range - divia) / bin_range) * g
    vote = np.asarray(vote) / 9
    vote = vote.astype("uint8")
    return vote

def HOG(magnitude_arr, direction_arr, cells=(8, 8), blocks=(8, 8),  bin_num=9):
    max_w = magnitude_arr.shape[1] // cells[0]
    max_h = magnitude_arr.shape[0] // cells[1]
    print(max_h)
    print(max_w)
    cells_array = []
    for y in range(max_h):
        for x in range(max_w):
            mag = magnitude_arr[y*cells[1]:(y + 1) * cells[1], x * cells[0]:(x + 1) * cells[0]]
            direct = direction_arr[y*cells[1]:(y + 1) * cells[1], x * cells[0]:(x + 1) * cells[0]]
            val = calculate_hispercell(mag, direct, bin_num)
            print(val.shape)
            cells_array.append(val)
    
    cells_array = np.asarray(cells_array)
    
    print(cells_array.shape)
    return cells_array

def main():
    img = cv2.imread("1.png", 0)
    magnitude, direction = calculate_gradients(img)
    hist = HOG(magnitude, direction)


if __name__ == "__main__":
    main()

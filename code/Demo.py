import numpy as np
import cv2
import glob


class HOG:
    @staticmethod
    def calculate_gradients(img):
        # tinh kich thuoc hinh anh va khai bao mang chua cuong do va huong
        h, w = img.shape[0], img.shape[1]
        magnitude = np.zeros((h, w))
        direction = np.zeros((h, w))
        img = img.astype("float32")
        # lap tinh toan cuong do va huong cua tung pixel
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
                # Magnitude (Gradient) - cuong do
                G = np.sqrt(Gx * Gx + Gy * Gy)
                magnitude[y, x] = G
                # Direction - huong
                D = 0 if Gy == 0 else np.arctan(Gx / Gy)
                D = D * 180.0 / np.pi
                D = D if D >= 0 else D + 180
                direction[y, x] = D
        return magnitude, direction

    @staticmethod
    def calculate_hispercell(magnitude, direction, bin_num):
        # chia chia bin cua cells
        if bin_num == 9:
            bins = (0, 20, 40, 60, 80, 100, 120, 140, 160)
            vote = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            bin_range = 20
        elif bin_num == 18:
            bins = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
                    100, 110, 120, 130, 140, 150, 160, 170)
            vote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            bin_range = 10

        # lap va vote vao tung cells
        for x in range(magnitude.shape[1]):
            for y in range(magnitude.shape[0]):
                g = magnitude[x, y]
                d = direction[x, y]
                il = d // bin_range
                ih = 0 if il == (bin_num - 1) else il + 1
                divia = d - bins[int(il)]
                vote[int(il)] += (divia / bin_range) * g
                vote[int(ih)] += ((bin_range - divia) / bin_range) * g

        # gian hoa tung cells roi tra ve vector cua hinh anh voi cac cells        
        vote = np.asarray(vote) / 9
        vote = vote.astype("uint8")
        return vote

    @staticmethod
    def hog_feature(img, cells=(8, 8), blocks=(8, 8),  bin_num=9):
        magnitude_arr, direction_arr = HOG.calculate_gradients(img)
        max_w = magnitude_arr.shape[1] // cells[0]
        max_h = magnitude_arr.shape[0] // cells[1]
        cells_array = []
        # tinh toan feature theo tung cells
        for y in range(max_h):
            for x in range(max_w):
                mag = magnitude_arr[y*cells[1]:(y + 1) * cells[1], x * cells[0]:(x + 1) * cells[0]]
                direct = direction_arr[y*cells[1]:(y + 1) * cells[1], x * cells[0]:(x + 1) * cells[0]]
                val = HOG.calculate_hispercell(mag, direct, bin_num)
                cells_array.append(val)
        cells_array = np.asarray(cells_array)
        # tinh toan feature theo norm trung binh
        cells_array = np.reshape(cells_array, blocks[0], blocks[1], cells_array.shape[1])
        return cells_array


class KNN:
    @staticmethod
    def caculate_distance(p1, p2):
        p1 = p1.astype("float32")
        p2 = p2.astype("float32")
        sum_dis = 0
        for i in range(len(p1)):
            sum_dis += (p1[i] - p2[i]) * (p1[i] - p2[i])
        return np.sqrt(sum_dis)

    @staticmethod
    def predict(x, y, k, f_predict):
        # x la feature anh, y label tuong ung cua feature anh, k la so hang xom gan nhat,
        # f_predict la freature cua anh can du doan
        array_distance = []
        # tinh toan khoang cach den cac diem
        for i in range(len(x)):
            d = KNN.caculate_distance(x[i], f_predict)
            array_distance.append[d]

        array_distance_sorted = sorted()



def main():
    img = cv2.imread("1.jpg", 0)
    img2 = cv2.imread("tesst.png", 0)
    feature = HOG.hog_feature(img)
    # feature2 = HOG.hog_feature(img2)
    # KNN.predict([feature], [0], 1, feature2)
    # print(feature.shape)


def Tshirt_class():
    # load toan bo anh o thu muc so sanh cho ao
    files = glob.glob()


if __name__ == "__main__":
    main()

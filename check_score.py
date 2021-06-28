import cv2

import vision


class CheckScore:
    def __init__(self, digits_img):
        self.digits_img = digits_img
        self.digits_array = []
        self.add_digits_to_array()

    def add_digits_to_array(self):
        for i in range(0, 10):
            x = int(i * 20)
            end_x = int(i * 20 + 20)
            y = 0
            end_y = 20
            self.digits_array.append(self.digits_img[y:end_y, x:end_x].copy())

    def check_score(self, img):
        gray_score_tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray_score_tmp, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        score = ""

        while True:

            for index, item in enumerate(self.digits_array):
                finder = vision.Vision(item)
                points = finder.find(thresh[0:int(thresh.shape[0]), 0:22], threshold=0.8)

                if points:

                    score += str(index)

                    break

                else:
                    continue

            thresh = thresh[0:int(thresh.shape[0]), 22:thresh.shape[1]]

            if thresh.shape[1] < 22:
                break

        if len(score) > 0:
            return int(score)
        else:
            return 0

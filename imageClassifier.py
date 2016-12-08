from sys import argv, maxint
import time
import numpy as np


class ImageFiles:
    def __init__(self):
        pass
    test_files = {}
    train_files = {}


def read_files(file_name):
    files = {}
    input_file = open(file_name, 'r')
    for line in input_file:
        data = line.split()
        img = np.empty((8, 8, 3), dtype=np.int)
        index = 2
        i = 0
        while i < 8:
            j = 0
            while j < 8:
                k = 0
                while k < 3:
                    img[i][j][k] = int(data[index])
                    index += 1
                    k += 1
                j += 1
            i += 1
        files[data[0] + data[1]] = {"orient": int(data[1]), "img": img}

    input_file.close()
    return files


def test_nearest():
    confusion_matrix = np.zeros((4, 4), dtype=np.int)
    i = 0
    result = 0
    for test_f_id in imf.test_files:
        i += 1
        test_f_img = imf.test_files[test_f_id]["img"]

        min_dist = maxint
        img_with_min_dist = ""

        for train_f_id in imf.train_files:
            train_f_img = imf.train_files[train_f_id]["img"]
            new_img = np.subtract(train_f_img, test_f_img)
            new_img = np.square(new_img)
            dist = np.sum(new_img)
            if dist < min_dist:
                min_dist = dist
                img_with_min_dist = train_f_id

        if imf.test_files[test_f_id]["orient"] == imf.train_files[img_with_min_dist]["orient"]:
            result += 1
        confusion_matrix[imf.test_files[test_f_id]["orient"]/90, imf.train_files[img_with_min_dist]["orient"]/90] += 1

    print "Confusion Matrix: \n" + str(confusion_matrix)
    print "Accuracy:" + str(result*1.0/(i*1.0))

start_time = time.time()
train_file = argv[1]
test_file = argv[2]
mode = argv[3]

imf = ImageFiles()
imf.train_files = read_files(train_file)
imf.test_files = read_files(test_file)

if mode == "nearest":
    test_nearest()

end_time = time.time()
print end_time - start_time

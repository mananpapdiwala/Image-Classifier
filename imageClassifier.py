from sys import argv, maxint
import time
import numpy as np


class ImageFiles:
    def __init__(self):
        pass
    test_files = {}
    train_files = {}


def read_files(file_name, train_mode):
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
    print len(files)
    return files


def test_nearest():
    confusion_matrix = np.zeros((4, 4), dtype=np.int)
    i = 0
    result = 0
    for test_f_id in imf.test_files:
        print i
        i += 1
        test_f_img = imf.test_files[test_f_id]["img"]

        # when k = 20
        # min_dist = [maxint]*20
        # img_with_min_dist = [""]*20

        min_dist = maxint
        img_with_min_dist = ""

        for train_f_id in imf.train_files:
            train_f_img = imf.train_files[train_f_id]["img"]
            new_img = np.subtract(train_f_img, test_f_img)
            new_img = np.square(new_img)
            dist = np.sum(new_img)
            """ if dist < min_dist[19]:
                min_dist[19] = dist
                img_with_min_dist[19] = train_f_id
                img_with_min_dist = [x for (y, x) in sorted(zip(min_dist, img_with_min_dist))]
                min_dist.sort()
                # http://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list


            orientation = [0, 0, 0, 0]
            for file_id in img_with_min_dist:
                orientation[imf.train_files[file_id]["orient"]/90] += 1
            """

            if dist < min_dist:
                min_dist = dist
                img_with_min_dist = train_f_id

        # if imf.test_files[test_f_id]["orient"]/90 == orientation.index(min(orientation)):
        if imf.test_files[test_f_id]["orient"] == imf.train_files[img_with_min_dist]["orient"]:
            result += 1
        confusion_matrix[imf.test_files[test_f_id]["orient"]/90, imf.train_files[img_with_min_dist]["orient"]/90] += 1
    print "Accuracy:" + str(result/i*1.0)
    print "Confusion Matrix: " + str(confusion_matrix)


start_time = time.time()
train_file = argv[1]
test_file = argv[2]
mode = argv[3]

imf = ImageFiles()
imf.train_files = read_files(train_file, True)
imf.test_files = read_files(test_file, False)

if mode == "nearest":
    test_nearest()

end_time = time.time()
print time.asctime(time.localtime(time.time()))
print end_time - start_time

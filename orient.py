from sys import argv, maxint
from time import time
from cStringIO import StringIO

if __name__ == '__main__':
    train_file = argv[1]
    test_file = argv[2]
    mode = argv[3]

    with open(train_file) as f:
        content = f.readlines()
    train = {}
    for line in content:
        words = line.split()
        train[words[0] + "+|+" + words[1]] = map(int, words[2:])
    p_len = len(train[words[0] + "+|+" + words[1]])
    with open(test_file) as f:
        content = f.readlines()
    test = {}
    for line in content:
        words = line.split()
        test[words[0] + "+|+" + words[1]] = map(int, words[2:])

    start_time = time()
    count = 0
    file_str = StringIO()
    for test_img in test:
        min_dist = maxint
        for train_img in train:
            dist = 0
            # for i in xrange(0, p_len, 3):
            for i in range(0, p_len):
                dist += (train[train_img][i] - test[test_img][i]) ** 2
                '''+ \
                        (train[train_img][i + 1] - test[test_img][i + 1]) ** 2 + \
                        (train[train_img][i + 2] - test[test_img][i + 2]) ** 2'''
            if dist < min_dist:
                min_dist = dist
                test_orient = train_img.split('+|+')[1]
        file_str.write(test_img.split('+|+')[0] + " " + test_orient + '\n')
        if test_img.split('+|+')[1] == test_orient:
            count += 1
    with open('nearest output.txt', 'w') as f:
        f.write(file_str.getvalue())
    print count * 100.0 / len(test)
    print (time() - start_time) * 1.0 / 60
    # A = 67.2322375398
    # Time = 47.859950002

    # Adaboost
    # if

    # NN


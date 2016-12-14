from random import random, randint
from sys import argv, maxint
import numpy as np
import math
import copy
from cStringIO import StringIO
# http://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/

# To maintain all the train and test data files
class ImageFiles:
    def __init__(self):
        pass

    test_files = {}
    train_files = {}
    adaboost = {}
    orientation = [0, 90, 180, 270]

# This function reads the data from the file given as parameter and returns a numpy array of that data
def read_files2(file_name):
    files = {}
    input_file = open(file_name, 'r')
    for line in input_file:
        data = line.split()
        img = np.empty(192, dtype=np.int)
        index = 2
        i = 0
        while i < 192:
            img[i] = int(data[index])
            index += 1
            i += 1
        files[data[0] + data[1]] = {"orient": int(data[1]), "img": img}

    input_file.close()
    return files

# The k nearest neighbors algorithm is used to estimate the orientation of the test file
# For any one test data point euclidean distance is calculated with respect to every train example and the train example that gives min distance
# The orientation of that train example is labelled to the test data point
# This function prints accuracy, confusion matrix and writes the output in the file nearest_output.txt
# For the given train and test data this method takes around 9-10 minutes
def test_nearest():
    confusion_matrix = np.zeros((4, 4), dtype=np.int)
    i = 0
    result = 0
    nearest_file_str = StringIO()
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
        confusion_matrix[
            imf.test_files[test_f_id]["orient"] / 90, imf.train_files[img_with_min_dist]["orient"] / 90] += 1
        nearest_file_str.write(train_f_id.split('.jpg')[0] + " " + str(imf.train_files[img_with_min_dist]["orient"]) + '\n')

    print "Confusion Matrix: \n" + str(confusion_matrix)
    print "Accuracy:" + str(result * 1.0 / (i * 1.0))
    with open('nearest_output.txt', 'w') as f:
        f.write(nearest_file_str.getvalue())

#################Adaboost
# This method takes around 40 seconds for 10 stumps and provides accuracy around 52%
# 9-10 minutes for 50 stumps and provides accuracy around 66%
# 35-40 minutes for 100 stumps and provides accuracy around 69%
# This function initializes the weight of each train example to 1/N where N is the size of train data
# This is the initialization used for Adaboost
def initializeWeight(train, totalCount):
    for example in train:
        train[example]["weight"] = 1.0/totalCount

# For any instance of the train table this function gives the best suited attribute or attribute with min error
def getBestAttribute(boost, imageOrient):
    for trainFileId in imf.train_files:
        for pixels in boost:
            p = [ int(pixel) for pixel in pixels.split()]
            if (imf.train_files[trainFileId]["img"][p[0]] > imf.train_files[trainFileId]["img"][p[1]] and imf.train_files[trainFileId]["orient"] == imageOrient) or (imf.train_files[trainFileId]["img"][p[0]] < imf.train_files[trainFileId]["img"][p[1]] and imf.train_files[trainFileId]["orient"] != imageOrient):
                boost[pixels]["value"] += imf.train_files[trainFileId]["weight"]

    max_pixel = max([[pixel, boost[pixel]] for pixel in boost], key= lambda x: x[1]["value"])
    return max_pixel

# This function modifies the weights of the train examples that the selected attribute correctly identifies
def modifyWeight(modifier, stump_pixel, imageOrient):
    newSum = 0
    p = [ int(pixel) for pixel in stump_pixel.split()]
    for trainFileId in imf.train_files:
        if (imf.train_files[trainFileId]["img"][p[0]] > imf.train_files[trainFileId]["img"][p[1]] and imf.train_files[trainFileId]["orient"] == imageOrient) or (imf.train_files[trainFileId]["img"][p[0]] < imf.train_files[trainFileId]["img"][p[1]] and imf.train_files[trainFileId]["orient"] != imageOrient):
            imf.train_files[trainFileId]["weight"] *= modifier
        newSum += imf.train_files[trainFileId]["weight"]
    return newSum

# This function normalizes the weights in the train table
def normalize(normalizeValue):
    for trainFileId in imf.train_files:
        imf.train_files[trainFileId]["weight"] = imf.train_files[trainFileId]["weight"]/normalizeValue

train_file = argv[1]
test_file = argv[2]
mode = argv[3]

imf = ImageFiles()
imf.train_files = read_files2(train_file)
imf.test_files = read_files2(test_file)

if mode == "nearest":
    #Uses the k nearest neighbor algortihm
    test_nearest()

if mode == "adaboost":
    stump_count = int(argv[4])
    count_Train = len(imf.train_files)

    # Creates the dictionary of pair of pixels
    # Length of dictionary is equal to stump size
    # The pair of pixels are selected randomly 
    for i in range(0, stump_count):
        pixel1 = -1
        pixel2 = -1
        while pixel1 == -1 or pixel2 == -1 or (str(pixel1) + " " + str(pixel2)) in imf.adaboost:
            pixel1 = randint(0,191)
            pixel2 = randint(0,191)
        imf.adaboost[str(pixel1) + " " + str(pixel2)] = {"value": 0};

    # Adaboost method is used to create an ensembler for each orientation individually
    all_orientation_stump = {}
    for orient in imf.orientation:
        bestAttribute = []
        initializeWeight(imf.train_files, count_Train)

        newBoost = copy.deepcopy(imf.adaboost)
        for stump in range(0, stump_count):
            bestAttribute.append(getBestAttribute(newBoost, orient))
            totalWeight = sum([imf.train_files[train]["weight"] for train in imf.train_files])
            error = (totalWeight - bestAttribute[stump][1]["value"]) / totalWeight
            # Sometimes the pair of pixel selected randomly are so poor that the error rate is 100% so we give error rate 99% to avoid divide by zero error
            error = 0.99 if error == 1 else error

            # Calculates the modified weights to be assigned
            beta = (error)/(1-error)

            # Stores the weights of the decision stump based on error
            bestAttribute[stump].append(1 + math.log(1/beta))
            normalizeSum = modifyWeight(beta, bestAttribute[stump][0], orient)
            normalize(normalizeSum)
            del newBoost[bestAttribute[stump][0]]

            for key in newBoost:
                newBoost[key]["value"] = 0

        all_orientation_stump[orient] = bestAttribute

    # Essembler for each orientation is executed on any test data point
    # The one that gives best value is used to label the test point 
    count_correct = 0
    confusion_matrix = np.zeros((4, 4), dtype=np.int)
    file_str = StringIO()
    for testFileId in imf.test_files:
        finalDecision = {}
        for orient in all_orientation_stump:
            decisionValue = 0
            for decision_stump in all_orientation_stump[orient]:
                p = [ int(pixel) for pixel in decision_stump[0].split()]
                if (imf.test_files[testFileId]["img"][p[0]] > imf.test_files[testFileId]["img"][p[1]]):
                    decisionValue += decision_stump[2] * 1
                else:
                    decisionValue += decision_stump[2] * -1
            finalDecision[orient] = decisionValue
        decisionOrient = max([ [key, finalDecision[key]] for key in finalDecision], key = lambda x: x[1])
        if imf.test_files[testFileId]["orient"] == decisionOrient[0]:
            count_correct += 1
        confusion_matrix[imf.test_files[testFileId]["orient"] / 90, decisionOrient[0] / 90] += 1
        file_str.write(testFileId.split('.jpg')[0] + ".jpg" + " " + str(decisionOrient[0]) + '\n')

    # Prints the confusion matrix, accuracy and writes the output in file in adaboost_output.txt
    print "Confusion Matrix: \n" + str(confusion_matrix)
    print "Accuracy:" + str( (count_correct * 100.0) / len(imf.test_files) )
    with open('adaboost_output.txt', 'w') as f:
        f.write(file_str.getvalue())

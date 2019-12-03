"""
K-Means Segmentation Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to segment image using k-means clustering.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint:
Please complete all the functions that are labeled with '#to do'.
You are allowed to add your own functions if needed.
You should design you algorithm as fast as possible. To avoid repetitve calculation, you are suggested to depict clustering based on statistic histogram [0,255].
You will be graded based on the total distortion, e.g., sum of distances, the less the better your clustering is.
"""

import utils
import numpy as np
import json
import time


def kmeans(img, k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K.
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.
    """
    # TODO: implement this function.
    dict = {}
    x_num = len(img)
    y_num = len(img[0])
    # Using hash table to store gray values present in the image
    for i in range(x_num):
        for j in range(y_num):
            if img[i][j] in dict:
                dict[img[i][j]] += 1
            else:
                dict[img[i][j]] = 1
    new_img = np.reshape(img, x_num * y_num)
    min_dis = 999999999999999999
    min_label = []
    min_center = [0, 0]
    x = 0
    while x < 255:
        # We don't need to traverse gray values which not exist in img
        # You can change the interval of traverse at here
        # The smaller the interval of traversal, the better the result and the longer the running time required
        # When I traverse all combination, the solution is approximate: {"centers": [85, 162], "distance": 5401137}
        if x not in dict:
            x += 25
            continue
        y = x + 25
        while y < 256:
            if y not in dict:
                y += 25
                continue
            centers = [x, y]
            c, l, d = get_kmeans(centers, new_img)
            if min_dis > d:
                min_center, min_label, min_dis = c, l, d
            y += 25
        x += 25

    min_label = np.array(min_label).reshape(x_num, y_num)
    return min_center, min_label.tolist(), min_dis


# apply k-means algorithm
def get_kmeans(c, new_img):
    labels, cluster = get_label(c, new_img)
    new_c = get_center(cluster)
    while abs(new_c[0]-c[0]) > 0.0001 and abs(new_c[1]-c[1]) > 0.0001:
        c = new_c
        labels, cluster = get_label(c, new_img)
        new_c = get_center(cluster)
    d = get_distane(new_c, labels, new_img)
    return new_c, labels, d


# classify each gray value to cluster
def get_label(centers, img):
    labels = np.zeros(len(img), dtype=int)
    flag = {}
    cluster = {0: [], 1: []}
    center1 = centers[0]
    center2 = centers[1]
    for i, item in enumerate(img):
        if item in flag:
            labels[i] = flag[item]
            cluster[labels[i]].append(item)
        else:
            if abs(item-center1) <= abs(item-center2):
                labels[i] = 0
            else:
                labels[i] = 1
            cluster[labels[i]].append(item)
            flag[item] = labels[i]
    return labels, cluster


# find the center of each cluster
def get_center(cluster):
    center = []
    for key in cluster.keys():
        center.append(np.mean(np.array(cluster[key])))
    return np.array(center).tolist()


# calculate the distance
def get_distane(c, l, img):
    img = img.tolist()
    flag0, flag1 = {}, {}
    x, y = c[0], c[1]
    sum0, sum1 = 0, 0
    for i, item in enumerate(img):
        if item in flag0:
            sum0 += flag0[item]
        elif item in flag1:
            sum1 += flag1[item]
        else:
            if l[i] == 0:
                d = abs(item-x)
                flag0[item] = d
                sum0 += d
            else:
                d = abs(item-y)
                flag1[item] = d
                sum1 += d

    return sum0 + sum1


def visualize(centers, labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels.
    Return: Segmentation map.
    """
    # TODO: implement this function.
    l = []
    for i in range(len(centers)):
        l.append(int(round(centers[i])))

    x_nums = len(labels)
    y_nums = len(labels[0])
    res = np.zeros((x_nums, y_nums), dtype=np.int)
    for x in range(x_nums):
        for y in range(y_nums):
            res[x][y] = l[labels[x][y]]

    return np.array(res, dtype=np.uint8)


if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img, k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers": centers, "distance": sumdistance,
                                   "time": running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
"""
Denoise Problem
(Due date: Nov. 25, 11:59 P.M., 2019)
The goal of this task is to denoise image using median filter.

Do NOT modify the code provided to you.
Do NOT import ANY library or API besides what has been listed.
Hint: 
Please complete all the functions that are labeled with '#to do'. 
You are suggested to use utils.zero_pad.
"""


import utils
import numpy as np
import json


def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """
    # TODO: implement this function.
    pad_img = utils.zero_pad(img, 1, 1)
    res = np.zeros((len(img), len(img[0])), dtype=np.int)
    for x in range(1, len(pad_img) - 1):
        for y in range(1, len(pad_img[0]) - 1):
            l = [pad_img[x - 1][y - 1], pad_img[x - 1][y], pad_img[x - 1][y + 1], pad_img[x][y - 1],
                 pad_img[x][y], pad_img[x][y + 1], pad_img[x + 1][y - 1], pad_img[x + 1][y], pad_img[x + 1][y + 1]]
            l.sort()
            res[x - 1][y - 1] = l[4]
    return np.array(res, dtype=np.uint8)


def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """    
    # TODO: implement this function.
    sum = 0
    for x in range(len(img1)):
        for y in range(len(img1[0])):
            sum += (img1[x][y] - img2[x][y]) ** 2
    mse = sum / (len(img1) * len(img1[0]))
    return mse
    

if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')

    result = median_filter(img)
    error = mse(gt, result)

    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')



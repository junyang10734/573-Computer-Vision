"""
Template Matching
(Due date: Sep. 25, 3 P.M., 2019)

The goal of this task is to experiment with template matching techniques, i.e., normalized cross correlation (NCC).

Please complete all the functions that are labelled with '# TODO'. When implementing those functions, comment the lines 'raise NotImplementedError' instead of deleting them. The functions defined in 'utils.py'
and the functions you implement in 'task1.py' are of great help.

Do NOT modify the code provided to you.
Do NOT use ANY API provided by opencv (cv2) and numpy (np) in your code.
Do NOT import ANY library (function, module, etc.).
"""


import argparse
import json
import os
import time

import utils

# from task1 import *
from test1 import *

gl = []

def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img-path",
        type=str,
        default="./data/proj1-task2.jpg",
        help="path to the image")
    parser.add_argument(
        "--template-path",
        type=str,
        default="./data/proj1-task2-template.jpg",
        help="path to the template"
    )
    parser.add_argument(
        "--result-saving-path",
        dest="rs_path",
        type=str,
        default="./results/task2.json",
        help="path to file which results are saved (do not change this arg)"
    )
    args = parser.parse_args()
    return args


def norm_xcorr2d(patch, template):
    """Computes the NCC value between a image patch and a template.

    The image patch and the template are of the same size. The formula used to compute the NCC value is:
    sum_{i,j}(x_{i,j} - x^{m}_{i,j})(y_{i,j} - y^{m}_{i,j}) / (sum_{i,j}(x_{i,j} - x^{m}_{i,j}) ** 2 * sum_{i,j}(y_{i,j} - y^{m}_{i,j})) ** 0.5
    This equation is the one shown in Prof. Yuan's ppt.

    Args:
        patch: nested list (int), image patch.
        template: nested list (int), template.

    Returns:
        value (float): the NCC value between a image patch and a template.
    """
    global gl
    xn = len(template)
    yn = len(template[0])

    if gl:
        pass
    else:
        g_c = 0
        g_t = 0
        for x1 in range(xn):
            g_t += sum(template[x1])
            g_c += yn
        g_mean = g_t / g_c
        for x1 in range(xn):
            for y1 in range(yn):
                gl.append(template[x1][y1] - g_mean)

    f_t = 0
    f_c = 0
    fl = []
    for x2 in range(xn):
        f_t += sum(patch[x2])
        f_c += yn
    f_mean = f_t / f_c

    # len = len(gl)
    # a, b, c = -1, -1, -1
    for x2 in range(xn):
        for y2 in range(yn):
            # item1 = patch[x2][y2] - f_mean
            fl.append(patch[x2][y2] - f_mean)
            # fl.append(item1)
            # item2 = gl[x2*yn+y2]
            # a += item1 * item2
            # b += item2 * item2
            # c += item1 * item1

    a, b, c = -1, -1, -1
    for i in range(len(gl)):
        a += gl[i] * fl[i]
        b += gl[i] * gl[i]
        c += fl[i] * fl[i]

    conv = a / (np.sqrt(b*c))
    return conv

    raise NotImplementedError



def match(img, template):
    """Locates the template, i.e., a image patch, in a large image using template matching techniques, i.e., NCC.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        x (int): row that the character appears (starts from 0).
        y (int): column that the character appears (starts from 0).
        max_value (float): maximum NCC value.
    """
    # TODO: implement this function.
    xn = len(template)
    yn = len(template[0])

    match_matrix = [[0 for y in range(len(img[0]) - yn + 1)] for x in range(len(img) - xn + 1)]

    for m in range(len(img) - xn + 1):
        for n in range(len(img[0]) - yn + 1):
            patch = []
            for x in range(xn):
                row = img[m+x][n:n+yn]
                patch.append(row)
            conv = norm_xcorr2d(patch, template)
            match_matrix[m][n] = conv
            print('[' + str(m) + ', ' + str(n) + ']:     ' + str(conv))

    max_x, max_y, max_value = -1, -1, -1
    for x in range(len(match_matrix)):
        for y in range(len(match_matrix[0])):
            if match_matrix[x][y] > max_value:
                max_value = match_matrix[x][y]
                max_x = x
                max_y = y

    return max_x, max_y, max_value

    raise NotImplementedError


def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    start = time.time()
    global gl
    args = parse_args()

    img = read_image(args.img_path)

    # template = utils.crop(img, xmin=10, xmax=30, ymin=10, ymax=30)
    # template = np.asarray(template, dtype=np.uint8)
    # cv2.imwrite("./data/proj1-task2-template.jpg", template)

    template = read_image(args.template_path)
    x, y, max_value = match(img, template)
    max_value = round(max_value, 3)

    # The correct results are: x: 17, y: 129, max_value: 0.994
    with open(args.rs_path, "w") as file:
        json.dump({"x": x, "y": y, "value": max_value}, file)

    end = time.time()
    print('程序执行时间: ', end - start)


if __name__ == "__main__":
    main()

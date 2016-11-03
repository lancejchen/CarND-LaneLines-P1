import numpy as np
import cv2


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    lines = lines.reshape(lines.shape[0], lines.shape[2])
    slopes = (lines[:, 1] - lines[:, 3]) / (lines[:, 0] - lines[:, 2])
    distances = np.sqrt(np.square(lines[:, 1] - lines[:, 3]) + np.square(lines[:, 0] - lines[:, 2]))
    print('the distance is: ', distances[:5])
    dist_threshold = np.percentile(distances, 30, axis=0)
    long_lines = (distances > dist_threshold)

    lines = lines[~np.isnan(slopes) & ~np.isinf(slopes) & long_lines]
    slope = slopes[~np.isnan(slopes) & ~np.isinf(slopes) & long_lines]
    print(lines.shape)
    ori_lines = lines
    lines = lines.reshape([lines.shape[0] * 2, lines.shape[1] // 2])
    print(lines.shape)
    y_min = lines[:, 1].min()
    print('y_min is: ', y_min)
    y_max = img.shape[0]

    # get the right line
    right_threshold = 0
    right_slope = slope[slope > right_threshold]
    right_lines = lines[slope > right_threshold]
    print(right_lines[:5])

    right_slope_mean = np.mean(right_slope)
    # weighted slope mean
    # get the votes
    distances = np.sqrt(np.square(ori_lines[:, 1] - ori_lines[:, 3]) + np.square(ori_lines[:, 0] - ori_lines[:, 2]))
    print('right_slope shape is: ', right_slope.shape)
    print('distance shape is: ', distances.shape)
    right_slope_mean = np.dot(right_slope, distances.T)
    print('this is the right slope mean: ', right_slope_mean)
    # right_slope_mean =
    right_lines_mean = np.mean(right_lines, axis=0)
    print("this is the right_lines_mean", right_lines_mean)

    x_mean_right = right_lines_mean[0]
    y_mean_right = right_lines_mean[1]
    right_intercept = y_mean_right - right_slope_mean * x_mean_right
    x_right_lowest = float(y_min - right_intercept) / right_slope_mean
    x_right_max = float(y_max - right_intercept) / right_slope_mean
    cv2.line(img, (int(x_right_max), int(y_max)), (int(x_right_lowest), int(y_min)), color, thickness)


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    lines = lines.reshape(lines.shape[0], lines.shape[2])
    slopes = (lines[:, 3] - lines[:, 1]) / (lines[:, 2] - lines[:, 0])
    lines = lines[~np.isnan(slopes) & ~np.isinf(slopes)]
    slope = slopes[~np.isnan(slopes) & ~np.isinf(slopes)]

    y_max = img.shape[0]
    y_min = lines.reshape([lines.shape[0] * 2, lines.shape[1] // 2])[:, 1].min()
    right_threshold = 0
    right_slope = slope[slope < right_threshold]
    right_lines = lines[slope < right_threshold]

    left_threshold = 0
    left_slope = slope[slope > left_threshold]
    left_lines = lines[slope > left_threshold]
    avg_right_slope = right_slope.mean()
    avg_right_x, avg_right_y = np.mean(right_lines.reshape(right_lines.shape[0] * 2, right_lines.shape[1] // 2), axis=0)
    right_intercept = avg_right_y - (avg_right_slope * avg_right_x)
    print('y_min is: ', y_min, ' right_intercept is: ', right_intercept, ' average_right_slope is: ', avg_right_slope)
    x_right_lowest = float(y_min - right_intercept) / avg_right_slope
    x_right_max = float(y_max - right_intercept) / avg_right_slope
    cv2.line(img, (int(x_right_max), int(y_max)), (int(x_right_lowest), int(y_min)), color, thickness)

    avg_left_slope = left_slope.mean()
    avg_left_x, avg_left_y = np.mean(left_lines.reshape(left_lines.shape[0] * 2, left_lines.shape[1] // 2), axis=0)
    left_intercept = avg_left_y - (avg_left_slope * avg_left_x)
    print('y_min is: ', y_min, ' left_intercept is: ', left_intercept, ' average_left_slope is: ', avg_left_slope)
    x_left_lowest = float(y_min - left_intercept) / avg_left_slope
    x_left_max = float(y_max - left_intercept) / avg_left_slope
    cv2.line(img, (int(x_left_max), int(y_max)), (int(x_left_lowest), int(y_min)), color, thickness)
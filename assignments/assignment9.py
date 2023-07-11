import math
import pygame
import numpy as np
import os
import imageio
import matplotlib.pyplot as plt
import cv2

def rotate_backward_bilinear(im, deg, center = None):
    rad = np.deg2rad(-deg)
    c = np.cos(rad)
    s = np.sin(rad)

    if center is None: #
        center = np.array([im.shape[1], im.shape[0]]) / 2. #
    
    x0, y0 = center
    

    dst = np.zeros(im.shape, dtype='uint8')
    dst[:,:,0] = 255
#    dst[:,:,3] = 255

    for yr in range(dst.shape[0]):
        for xr in range(dst.shape[1]):
            x = xr * c - yr * s
            y = xr * s + yr * c

            x = (xr - x0)*c - (yr - y0)*s + x0
            y = (xr - x0)*s + (yr - y0)*c + y0

            xi = int(x)
            yi = int(y)

            if yi < 0 or xi < 0 or yi >= im.shape[0]-1 or xi >= im.shape[1] -1:
                continue

            # xip1 = xi + 1
            # yip1 = yi + 1

            #average = (im[yi, xi].astype(float) + im[yi, xi+1].astype(float) + im[yi+1, xi+1].astype(float) + im[yi+1, xi].astype(float)) / 4.
            #avg = np.zeros((4,), dtype='uint8')
            #for i in range(4):
            #    if average[i] > 255:
            #        avg[i] = 255
            #    else:
            #       avg[i] = average[i].astype('uint8')
            # avg[3] = 255

            # if yi < 0 or yi >= im.shape[0] or xi >= im.shape[1]:
            #     continue

            # dst[yr, xr] = im[yi, xi]
            
            def linintr(w, a, b):
                a = a.astype('float')
                b = b.astype('float') 
                c = w*b + (1. - w)*a
                return c

            alpha = x -xi
            beta = y - yi
            J0 = linintr(beta, im[yi, xi], im[yi+1, xi])
            J1 = linintr(beta, im[yi, xi+1], im[yi+1, xi+1])
            J = linintr(alpha, J0, J1)
            dst[yr, xr] = J.astype('uint8')
    #
    return dst

def main():
    im = cv2.imread("assets/mushroom1.png")
    deg = 0
    while True:
        im_rot = rotate_backward_bilinear(im, deg) #center가 주어지지 않았을떄 자동으로 screen의 center로 조정
        #im_rot = rotate_backward_bilinear(im, deg, (32, 10))
        cv2.imshow("window name", im_rot)
        deg += 10

        key = cv2.waitKey(10)
        if key == 27:
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    main()
import cv2 as cv
import numpy as np
import scipy
import math
import time
import copy
import matplotlib
#%matplotlib inline
import pylab as plt
import json
from PIL import Image
from shutil import copyfile
from skimage import img_as_float
from functools import reduce
from renderopenpose import *
import os
import argparse


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)


##### Must specifcy these parameters
parser.add_argument('--source_keypoints_dir', type=str, default='keypoints', help='directory where source keypoint files are stored, assumes .yml format for now.')
parser.add_argument('--target_keypoints_dir', type=str, default='keypoints', help='directory where target keypoint files are stored, assumes .yml format for now.')
parser.add_argument('--spread', nargs='+', type=int, help='range of frames to use for target video plus step size [start end step] e.g. 0 10000 1')
parser.add_argument('--save_dir', type=str, default='save', help='directory where to save generated files')
parser.add_argument('--err_filename', type=str, default='', help='directory where to save generated errors')


opt = parser.parse_args()
spread = tuple(opt.spread)
start = spread[0]
end = spread[1]
step = spread[2]


n = start
print(step)


# Get keypoints for source and target (generated)
source_keypoints_dir = opt.source_keypoints_dir
target_keypoints_dir = opt.target_keypoints_dir
savedir = opt.save_dir


if not os.path.exists(savedir):
    os.makedirs(savedir)


source_keypoints = sorted(os.listdir(source_keypoints_dir))
target_keypoints = sorted(os.listdir(target_keypoints_dir))


#init append to file
filename = opt.err_filename
f = open(filename+".txt", "a");


perror_acc = 0
perror_ave = 0
cntr = 1;
ave_total = []
while n <= end:
    ave = 0
    acc = 0


    filebase_name_source = os.path.splitext(source_keypoints[n])[0]
    filebase_name_target = os.path.splitext(target_keypoints[n])[0]
    source_keyname = os.path.join(source_keypoints_dir,filebase_name_source)
    target_keyname = os.path.join(target_keypoints_dir,filebase_name_target)


    source_pose = []
    target_pose = []


    source_pose = readkeypointsfile(source_keyname)
    target_pose = readkeypointsfile(target_keyname)


    print("-----------source-------------")
    print(source_pose)
   
    print("------------------------------")
    # print(len(source_pose))
    print("-----------target-------------")
    print(target_pose)
    print("------------------------------")
    # print(len(target_pose))
   
    numOfelements = 0
    
    percent_error = []
    i = 0
    
    for target_elem in target_pose:
        # print(target_elem)
        source_elem = source_pose[i]
        
        if source_elem != 0:
            error = abs(target_elem - source_elem) / abs(source_elem)
            percent_error.append(error)
        else:
            percent_error.append(0)
        
        i += 1
    ave = sum(percent_error) / len(percent_error)
    ave_total.append(ave)
    f.write(str(cntr)+": "+str(ave))
    n += step
f.close()
perror_ave = sum(ave_total) / len(ave_total) * 100
perror_ave = round(perror_ave, 2)
print(str(perror_ave) + "%")
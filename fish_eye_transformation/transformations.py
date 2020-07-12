from skimage import transform, data, io
import numpy as np
import matplotlib.pyplot as plt
from albumentations.augmentations.functional import   optical_distortion
import cv2

def fisheye(xy, **kwargs):
    r1 = kwargs["r1"]
    r2 = kwargs["r2"]
    r3 = kwargs["r3"]
    center = np.mean(xy, axis=0)
    xc, yc = (xy - center).T

    # Polar coordinates
    r = np.sqrt(xc**2 + yc**2)
    theta = np.arctan2(yc, xc)

    r = r1 * np.exp(r**(1/r2) / r3)

    return np.column_stack((
        r * np.cos(theta), r * np.sin(theta)
        )) + center

def applyFisheye(image, r1=0.8, r2=2.1, r3=1.8):
    return transform.warp(image,  fisheye, map_args={"r1": r1, "r2": r2, "r3": r3})

def applyBarrelDistorion(image, k, dx, dy):
    distortedImage = optical_distortion(image, k=k, dx=dx, dy=dy, border_mode=cv2.BORDER_CONSTANT, value=0)
    return distortedImage
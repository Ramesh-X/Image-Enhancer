from __future__ import print_function, division, absolute_import
from .abstract_filter import AbstractFilter
import cv2


class SharpenFilter(AbstractFilter):
    def apply_filter(self, src_img, slider1, slider2, slider3):
        sigma = int(slider1)
        sigma = 2 * sigma + 1
        img_blr = cv2.GaussianBlur(src_img, (0, 0), sigmaX=sigma, sigmaY=sigma)
        return cv2.addWeighted(src_img, 1+slider2, img_blr, -slider2, 0)

    def setup_sliders(self):
        return [("Sigma", 0, 10), ("Value", -1, 1)]

    def name(self):
        return "Image Sharpen"


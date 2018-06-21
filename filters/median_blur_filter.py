from __future__ import print_function, division, absolute_import
from .abstract_filter import AbstractFilter
import cv2


class MedianBlurFilter(AbstractFilter):
    def setup_sliders(self):
        return [("Kernel Size", 0, 10)]

    def name(self):
        return "Median Blur"

    def type(self):
        return "Blur"

    def apply_filter(self, src_img, slider1, slider2, slider3):
        value = int(slider1)
        value = 2 * value + 1
        return cv2.medianBlur(src_img, value)

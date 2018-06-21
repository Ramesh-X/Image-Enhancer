from .abstract_filter import AbstractFilter
import cv2
import numpy as np


class TemperatureFilter(AbstractFilter):
    def apply_filter(self, src_img, slider1, slider2, slider3):
        src_img[:, :, 0] = np.power(src_img[:, :, 0], slider1)
        src_img[:, :, 2] = np.power(src_img[:, :, 2], 2-slider1)
        src_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2HSV)
        src_img[:, :, 1] = np.power(src_img[:, :, 1], slider1)
        return cv2.cvtColor(src_img, cv2.COLOR_HSV2BGR)

    def setup_sliders(self):
        return [("Value", 0.1, 2)]

    def name(self):
        return "Adjust Temperature"


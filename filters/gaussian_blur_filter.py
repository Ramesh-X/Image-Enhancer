from .abstract_filter import AbstractFilter
import cv2


class GaussianBlurFilter(AbstractFilter):
    def setup_sliders(self):
        return [("Sigma", 0, 10)]

    def name(self):
        return "Gaussian Blur"

    def type(self):
        return "Blur"

    def apply_filter(self, src_img, slider1, slider2, slider3):
        sigma = int(slider1)
        sigma = 2 * sigma + 1
        return cv2.GaussianBlur(src_img, (0, 0), sigmaX=sigma, sigmaY=sigma)

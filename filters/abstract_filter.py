from __future__ import print_function, division, absolute_import
from abc import ABCMeta, abstractmethod


class AbstractFilter:
    __metaclass__=ABCMeta

    @abstractmethod
    def apply_filter(self, src_img, slider1, slider2, slider3):
        """
        Must be implemented.
        Take the input src_image and apply the filters with the help of slider values and return the filtered image.
        If you are not using all the 3 sliders ignore the values of them. 
        
        :param src_img: Input image as numpy array
        :param slider1: Value of slider 1 as float
        :param slider2: Value of slider 2 as float
        :param slider3: Value of slider 3 as float
        :return Processed image as a numpy array
        """
        pass

    @abstractmethod
    def setup_sliders(self):
        """
        Setup the minimum and maximum values of the sliders. The maximum number of sliders available is 3.
        
        :return: A list of tuples. Tuple includes the slider name, minimum and the maximum values of the filter[ eg: (slider_name, min_value, max_value)].
        Each tuple is corresponding to a Slider.
        Provided name will be displayed in the slider.
        Provided range will be the range of the slider.
        You can have maximum 3 sliders. Provide them in the order.
        
        Eg:
         If you want 2 sliders, first slider with range (-1, 1) with name 'ABC' and second slider with range (0, 1) with name 'DEF' you can return
         [('ABC', -1, 1), ('DEF', 0, 1)]
        """
        return [(self.name(), -1, 1)]

    @abstractmethod
    def name(self):
        """
        :return Name of the filter as a string
        Do not provide any symbol character in the name  
        """
        pass

    def type(self):
        """
        Default value is same as the filter name.
        Override this method to give different filter type. If there are more than one filter with the same filter type, 
        those filters will be added in a submenu with the filter type as the name.
        
        :return: Type of the filter as a string
        """
        return self.name()

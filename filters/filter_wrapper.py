import numpy as np


class FilterWrapper(object):
    def __init__(self, image_changer, worker_queue, parent_image, _filter, i):
        self.filter = _filter
        self.__image_changer = image_changer
        self.__child = None
        self.__worker = worker_queue
        self.__original = parent_image
        self.__edited = parent_image
        self.__name = '%s %d' % (_filter.name(), i)
        self.__current = [(value[1] + value[2])/2.0 for value in _filter.setup_sliders()]
        while len(self.__current) < 3:
            self.__current.append(0)
        self.__apply()

    def parent(self):
        return self.__original

    def child(self):
        return self.__child

    def set_child(self, child):
        self.__child = child

    def edited(self):
        return self.__edited

    def __apply(self):
        if self.__original is not None and type(self.__original) is np.ndarray:
            self.__worker.add_work(self.__name, self.__finished, self.filter.apply_filter, self.__original, *self.__current)

    def __finished(self, img):
        self.__edited = img
        if self.__child is None:
            self.__image_changer.emit(img)
        else:
            self.__child.filtered(img)

    def filtered(self, parent=None):
        if parent is not None:
            self.__original = parent
            self.__apply()
            return self
        if self.__edited is None:
            self.__apply()
            return self
        return self.__edited

    def name(self):
        return self.__name

    def apply_filter(self, i, value):
        self.__current[i] = value
        if self.__original is None:
            return
        self.__apply()
        return self

    def initialize(self, *vcs):
        values = self.filter.setup_sliders()
        [vc.hide() for vc in vcs]
        for i, value in enumerate(values):
            vcs[i].set_values(value[0], self.__current[i], value[1], value[2])
            vcs[i].show()

from util import ProcessThread


class FilterWrapper(object):
    def __init__(self, parent_image, _filter, i):
        self.filter = _filter
        self.__process = None
        self.__original = parent_image
        self.__edited = parent_image
        self.__name = '%s %d' % (_filter.name(), i)
        self.__current = [(value[1] + value[2])/2.0 for value in _filter.setup_sliders()]
        while len(self.__current) < 3:
            self.__current.append(0)

    def parent(self):
        return self.__original

    def edited(self):
        return self.__edited

    def wait(self):
        self.__process.wait()
        return self.__edited

    def __apply(self):
        print("F1")
        if self.__process is not None:
            print("turn off")
            self.__process.turn_off()
        print("F2")
        self.__process = ProcessThread(self.filter.apply_filter, self.__original, *self.__current)
        self.__process.processed.connect(self.__finished)
        print("F3")
        self.__process.start()

    def __finished(self, img):
        self.__edited = img
        self.__process = None

    def filtered(self, parent=None):
        if parent is not None:
            self.__original = parent
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

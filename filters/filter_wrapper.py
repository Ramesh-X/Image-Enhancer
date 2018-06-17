class FilterWrapper(object):
    def __init__(self, parent_image, _filter, i):
        self.filter = _filter
        self.__original = parent_image
        self.__name = '%s %d' % (_filter.name(), i)
        self.__current = [(value[1] + value[2])/2.0 for value in _filter.setup_sliders()]
        while len(self.__current) < 3:
            self.__current.append(0)

    def set_parent(self, parent_image):
        self.__original = parent_image

    def parent(self):
        return self.__original

    def filtered(self, parent=None):
        if parent is not None:
            self.__original = parent
        return self.filter.apply_filter(self.__original, *self.__current)

    def name(self):
        return self.__name

    def apply_filter(self, i, value):
        self.__current[i] = value
        if self.__original is None:
            return
        return self.filter.apply_filter(self.__original, *self.__current)

    def initialize(self, *vcs):
        values = self.filter.setup_sliders()
        [vc.hide() for vc in vcs]
        for i, value in enumerate(values):
            vcs[i].set_values(value[0], self.__current[i], value[1], value[2])
            vcs[i].show()

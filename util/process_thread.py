from __future__ import print_function, division, absolute_import
from PyQt4 import QtCore
import numpy as np


class ProcessThread(QtCore.QThread):
    processed = QtCore.pyqtSignal(object)

    def __init__(self, process, *args):
        QtCore.QThread.__init__(self)
        self.__valid = True
        self.__process = process
        self.__args = args
        self.setTerminationEnabled(True)

    def __del__(self):
        self.wait()

    def run(self):
        if type(self.__args[0]) is np.ndarray:
            args = list(self.__args)
            args[0] = np.copy(args[0])
            self.__args = tuple(args)
        ret = self.__process(*self.__args)
        if self.__valid:
            self.processed.emit(ret)


from __future__ import print_function, division, absolute_import
from PyQt4 import QtCore


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
        ret = self.__process(*self.__args)
        if self.__valid:
            self.processed.emit(ret)


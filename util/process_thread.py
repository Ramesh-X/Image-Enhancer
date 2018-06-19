from PyQt4 import QtCore
import threading


class ProcessThread(QtCore.QThread):
    processed = QtCore.pyqtSignal(object)

    def __init__(self, process, *args):
        QtCore.QThread.__init__(self)
        self.__valid = True
        self.__process = process
        self.__args = args
        self.setTerminationEnabled(True)

    def __del__(self):
        print("TERMINATED")
        #self.wait()

    def run(self):
        ret = self.__process(*self.__args)
        if self.__valid:
            self.processed.emit(ret)

    def turn_off(self):
        pass
        #self.__valid = False
        #threading.Thread(target=self.terminate).start()


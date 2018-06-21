from __future__ import print_function, division, absolute_import
from PyQt4 import QtCore

from .process_thread import ProcessThread
from .singleton import Singleton


class WorkerQueue:
    __metaclass__ = Singleton


    def __init__(self, job_changer):
        self.__work = {}
        self.__i = 0
        self.__jobChanger = job_changer
        self.__mutex = QtCore.QMutex()
        self.__thread = None
        self.__finish_func = None

    def add_work(self, name, finish_func, func, *args):
        if func is None:
            return
        try:
            self.__mutex.lock()
            self.__work[name] = (self.__i, finish_func, func, args)
            self.__i += 1
        finally:
            self.__mutex.unlock()
        self.__do_work()

    def __do_work(self):
        try:
            self.__mutex.lock()
            if self.__thread is not None and self.__thread.isRunning():
                return
            min = 99999999
            min_key = None
            func = None
            args = None
            for key in self.__work:
                if self.__work[key][0] < min:
                    min_key = key
                    min, self.__finish_func, func, args = self.__work[key]
            if func is None:
                self.__i = 0
                return
            del self.__work[min_key]
            if len(self.__work) == 0:
                self.__i = 0
            self.__thread = ProcessThread(func, *args)
            self.__thread.processed.connect(self.__finished)
            self.__thread.start()
        finally:
            self.__mutex.unlock()
            self.__jobChanger.emit()

    def __finished(self, img):
        self.__finish_func(img)
        self.__do_work()

    def wait(self):
        while len(self.__work) != 0:
            self.__do_work()
            self.__thread.wait()

    def __str__(self):
        jobs = len(self.__work)
        is_run = self.__thread is not None and self.__thread.isRunning()
        if is_run:
            s = 'Job is running..'
        else:
            s = 'No job is running..'
        return '%s %d jobs in the queue' % (s, jobs)

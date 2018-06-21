import importlib
import pkgutil
from collections import defaultdict

import cv2
import numpy as np
from PyQt4 import QtCore, QtGui

from filters import AbstractFilter, FilterWrapper
from .controller_ui import ControllerUI
from util import WorkerQueue


class MainWindow(QtGui.QMainWindow):
    imageChanger = QtCore.pyqtSignal(object)
    jobChanger = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__originalImage = None
        self.__originalImage_uint = None
        self.__editedImage = None
        self.imageChanger.connect(self.__image_changer)
        self.__imageMaxHeight = 663
        self.__imageMaxWidth = 1000
        self.__i = 0
        self.__worker = WorkerQueue(job_changer=self.jobChanger)
        for (module_loader, name, ispkg) in pkgutil.iter_modules(['./filters']):
            importlib.import_module('.' + name, 'filters')
        self.__allFilterClasses = [cls for cls in AbstractFilter.__subclasses__()]
        self.__setup_ui()

    def __setup_ui(self):
        panel_ui = QtGui.QWidget(self)
        panel_ui_w = 350
        panel_ui_h = self.__imageMaxHeight + 80
        panel_ui.resize(panel_ui_w, panel_ui_h)
        panel_ui.move(0, 0)

        image_ui = QtGui.QWidget(self)
        image_ui_w = self.__imageMaxWidth + 20
        image_ui_h = panel_ui_h
        image_ui.resize(image_ui_w, image_ui_h)
        image_ui.move(panel_ui_w, 0)

        # Open Image Button
        self.__openImageButton = QtGui.QPushButton('Open Image', panel_ui)
        self.__openImageButton.clicked.connect(self.__open_file)
        self.__openImageButton.resize(100, 25)
        self.__openImageButton.move(15, 10)

        # Save Image Button
        self.__saveImageButton = QtGui.QPushButton('Save Image', panel_ui)
        self.__saveImageButton.clicked.connect(self.__save_file)
        self.__saveImageButton.resize(100, 25)
        self.__saveImageButton.move(120, 10)

        # Original Select CheckBox
        self.__showOriginalCheckBox = QtGui.QCheckBox('Show Original\n Size', panel_ui)
        self.__showOriginalCheckBox.move(225, 8)
        self.__showOriginalCheckBox.stateChanged.connect(self.__show_original_clicked)

        # Image info label
        self.__imageInfoLabel = QtGui.QLabel("Mouse hover the image to show the original image", image_ui)
        self.__imageInfoLabel.setStyleSheet('color: #606060; font-style: italic;')
        self.__imageInfoLabel.adjustSize()
        self.__imageInfoLabel.move(10, 10)

        # Job info label
        self.__jobInfoLabel = QtGui.QLabel(self)
        self.__jobInfoLabel.setStyleSheet('color: #202020;')
        self.jobChanger.connect(self.__job_changed)
        self.__jobInfoLabel.adjustSize()
        self.__jobInfoLabel.move(10, panel_ui_h)

        # Image Label
        self.__imageLabel = QtGui.QLabel(image_ui)
        self.__imageLabel.setScaledContents(True)
        self.__imageLabel.setMinimumSize(1, 1)
        self.__imageLabel.move(10, 30)
        self.__imageLabel.installEventFilter(self)

        # Filter List Information
        self.__filterListInfoLabel = QtGui.QLabel("Right click on the list to add/remove filters", panel_ui)
        self.__filterListInfoLabel.setStyleSheet('color: #606060; font-style: italic;')
        self.__filterListInfoLabel.adjustSize()
        self.__filterListInfoLabel.move(20, 45)

        # Filter List Menu
        self.__filterListMenu = QtGui.QMenu()
        self.__filterListMenu.addAction("Remove Item")
        self.__filterListMenu.addMenu(self.__setup_filters(self.__filterListMenu))
        self.__filterListMenu.triggered.connect(self.__filter_list_menu_item_clicked)

        # Filters List
        self.__filterList = QtGui.QListWidget(panel_ui)
        self.__filterList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__filterList.customContextMenuRequested.connect(self.__filter_list_right_clicked)
        self.__filterList.currentItemChanged.connect(self.__filter_selection_changed)
        self.__filterList.resize(panel_ui_w - 40, panel_ui_h - 240)
        self.__filterList.move(20, 65)

        # Value Changer 1
        self.__valueChanger1 = ControllerUI(panel_ui, "default", 1, 10, self.__value_changer_1_changed)
        self.__valueChanger1.resize(panel_ui_w-40, 50)
        self.__valueChanger1.move(20, 58 + panel_ui_h - 230)

        # Value Changer 2
        self.__valueChanger2 = ControllerUI(panel_ui, "default", 1, 10, self.__value_changer_2_changed)
        self.__valueChanger2.resize(panel_ui_w - 40, 50)
        self.__valueChanger2.move(20, 58 + panel_ui_h - 180)

        # Value Changer 3
        self.__valueChanger3 = ControllerUI(panel_ui, "default", 1, 10, self.__value_changer_3_changed)
        self.__valueChanger3.resize(panel_ui_w - 40, 50)
        self.__valueChanger3.move(20, 58 + panel_ui_h - 130)

        self.resize(panel_ui_w + image_ui_w + 10, panel_ui_h + 20)
        self.setWindowTitle("Image Enhancer")

    def __job_changed(self):
        self.__jobInfoLabel.setText(str(self.__worker))
        self.__jobInfoLabel.adjustSize()

    def __value_changer_1_changed(self, value):
        if self.__currentWrapperIndex == -1:
            return
        self.__filterWrappers[self.__currentWrapperIndex].apply_filter(0, value)

    def __value_changer_2_changed(self, value):
        if self.__currentWrapperIndex == -1:
            return
        self.__filterWrappers[self.__currentWrapperIndex].apply_filter(1, value)

    def __value_changer_3_changed(self, value):
        if self.__currentWrapperIndex == -1:
            return
        self.__filterWrappers[self.__currentWrapperIndex].apply_filter(2, value)

    def __filter_selection_changed(self, cur_item, prev_item):
        wrapper = None
        for i, _wrapper in enumerate(self.__filterWrappers):
            if _wrapper.name() == cur_item.text():
                self.__currentWrapperIndex = i
                wrapper = _wrapper
                break
        if wrapper is None:
            return
        wrapper.initialize(self.__valueChanger1, self.__valueChanger2, self.__valueChanger3)

    def __filter_list_menu_item_clicked(self, item):
        name = item.text()
        if name == "Remove Item":
            if self.__currentWrapperIndex == -1:
                return
            limit = len(self.__filterWrappers)
            if self.__currentWrapperIndex != 0:
                if self.__currentWrapperIndex + 1 == limit:
                    self.__filterWrappers[self.__currentWrapperIndex - 1].set_child(None)
                    self.__editedImage = self.__filterWrappers[self.__currentWrapperIndex - 1].filtered()
                    self.__convert_image(False)
                else:
                    self.__filterWrappers[self.__currentWrapperIndex - 1].set_child(self.__filterWrappers[self.__currentWrapperIndex + 1])
                    self.__filterWrappers[self.__currentWrapperIndex + 1].filtered(parent=self.__filterWrappers[self.__currentWrapperIndex - 1].filtered())
            else:
                if self.__currentWrapperIndex + 1 == limit:
                    self.__editedImage = self.__originalImage_uint
                    self.__convert_image(True)
                else:
                    self.__filterWrappers[self.__currentWrapperIndex + 1].filtered(parent=self.__originalImage)
            del self.__filterWrappers[self.__currentWrapperIndex]
            self.__filterList.takeItem(self.__currentWrapperIndex)
        _filter = None
        for f in self.__allFilters:
            if f.name() == name:
                _filter = f
        if _filter is not None:
            self.__i += 1
            item = QtGui.QListWidgetItem()
            if len(self.__filterWrappers) == 0:
                wrapper = FilterWrapper(self.imageChanger, self.__worker, self.__originalImage, _filter, self.__i)
            else:
                wrapper = FilterWrapper(self.imageChanger, self.__worker, self.__filterWrappers[-1].filtered(), _filter, self.__i)
                self.__filterWrappers[-1].set_child(wrapper)
            item.setText(wrapper.name())
            self.__filterWrappers.append(wrapper)
            self.__filterList.addItem(item)

    def __setup_filters(self, parent):
        self.__allFilters = [_filter() for _filter in self.__allFilterClasses]
        self.__filterWrappers = []
        self.__currentWrapperIndex = -1
        filter_dict = defaultdict(list)
        for _filter in self.__allFilters:
            filter_dict[_filter.type()].append(_filter)
        filter_menu = QtGui.QMenu("Filters", parent)
        for filter_type in filter_dict:
            filter_list = filter_dict[filter_type]
            if len(filter_list) > 1:
                menu_item = QtGui.QMenu(filter_type, filter_menu)
                for _filter in filter_list:
                    menu_item.addAction(_filter.name())
                filter_menu.addMenu(menu_item)
            else:
                filter_menu.addAction(filter_list[0].name())
        return filter_menu

    def __filter_list_right_clicked(self, q_pos):
        parent_pos = self.__filterList.mapToGlobal(QtCore.QPoint(0, 0))
        self.__filterListMenu.move(parent_pos + q_pos)
        self.__filterListMenu.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            self.__convert_image(True)
            return True
        if event.type() == QtCore.QEvent.Leave:
            self.__convert_image(False)
            return True
        return False

    def __show_original_clicked(self, state):
        self.__imageLabel.setScaledContents(not state)

    def __open_file(self):
        self.__filename = QtGui.QFileDialog.getOpenFileName(self, "Open Image", filter="Image Files (*.png *.jpg *.bmp);;All Files (*.*)")
        if self.__filename is None or str(self.__filename).strip() == "":
            return
        self.__filename = str(self.__filename)
        self.__originalImage_uint = cv2.imread(self.__filename)
        self.__originalImage = self.__originalImage_uint.astype(np.float32) / 255.0
        self.__editedImage = self.__originalImage_uint
        if len(self.__filterWrappers) != 0:
            result = QtGui.QMessageBox.question(self, 'Open File', 'Filter list is not empty. Clear them..?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if result == QtGui.QMessageBox.Yes:
                self.__filterList.clear()
                self.__filterWrappers.clear()
                self.__convert_image(True)
                return
            self.__filterWrappers[0].filtered(parent=self.__originalImage)
        self.__convert_image(True)

    def __save_file(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, "Save Image", directory=self.__filename, filter="Image Files (*.png *.jpg *.bmp);;All Files (*.*)")
        if filename is None or filename.strip() == "":
            return
        cv2.imwrite(filename, self.__editedImage)
        QtGui.QMessageBox.information(self, "Image Saving", "Image Saved..!\n\nLocation: %s" % filename, QtGui.QMessageBox.Ok)

    def __image_changer(self, img):
        self.__editedImage = img
        self.__convert_image(False)

    def __convert_image(self, original):
        if original:
            cv_img = self.__originalImage_uint
        else:
            cv_img = self.__editedImage
        if cv_img is None:
            return
        height, width, bytes_per_component = cv_img.shape
        bytes_per_line = bytes_per_component * width
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        qt_image = QtGui.QImage(cv_img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        _height = self.__imageMaxHeight
        _width = width*_height/height
        if _width > self.__imageMaxWidth:
            _width = self.__imageMaxWidth
            _height = height*_width/width
        self.__imageLabel.resize(_width, _height)
        self.__imageLabel.setPixmap(QtGui.QPixmap.fromImage(qt_image))


from __future__ import print_function, division, absolute_import
from PyQt4 import QtCore, QtGui


class ControllerUI(QtGui.QWidget):
    def __init__(self, parent, widget_label, _min, _max, slider_changed):
        QtGui.QWidget.__init__(self, parent=parent)
        if _min > _max:
            raise ValueError("Max value should be greater than the min value..")
        self.__max = _max
        self.__min = _min
        self.__scale = (_max - _min) / 1000.0
        self.__widgetLabelText = widget_label
        self.__slider_changed = slider_changed
        self.__width = 300
        self.__height = 100
        self.__textbox_w = 30
        self.__textbox_h = 15
        self.__doubleValidator = QtGui.QDoubleValidator()
        self.__doubleValidator.setDecimals(4)
        self.__setup_ui()

    def set_values(self, widget_label, current, _min, _max):
        if _min > _max:
            raise ValueError("Max value should be greater than the min value..")
        self.__max = _max
        self.__min = _min
        self.__scale = (_max - _min) / 1000.0
        self.__widgetLabelText = widget_label
        self.__valueLabel.setText('%s: %.3f' % (widget_label, current))
        self.__valueLabel.adjustSize()
        current = (current - _min) / self.__scale
        self.__valueSlider.setValue(current)
        self.__minTextBox.setText(str(_min))
        self.__maxTextBox.setText(str(_max))

    def __setup_ui(self):
        # Value Slider Text
        self.__valueLabel = QtGui.QLabel(self.__widgetLabelText, self)
        self.__valueLabel.adjustSize()
        self.__valueLabel.move(self.__textbox_w + 5, 0)

        # Min TextBox
        self.__minTextBox = QtGui.QLineEdit(str(self.__min), self)
        QtCore.QObject.connect(self.__minTextBox, QtCore.SIGNAL("textChanged(QString)"), self.__min_text_box_changed)
        self.__minTextBox.setValidator(self.__doubleValidator)
        self.__minTextBox.setToolTip("Set minimum value here")
        self.__minTextBox.resize(self.__textbox_w, self.__textbox_h)
        self.__minTextBox.move(0, 15)

        # Max TextBox
        self.__maxTextBox = QtGui.QLineEdit(str(self.__max), self)
        QtCore.QObject.connect(self.__maxTextBox, QtCore.SIGNAL("textChanged(QString)"), self.__max_text_box_changed)
        self.__maxTextBox.setToolTip("Set maximum value here")
        self.__maxTextBox.setValidator(self.__doubleValidator)
        self.__maxTextBox.resize(self.__textbox_w, self.__textbox_h)

        # Value Slider
        self.__valueSlider = QtGui.QSlider(self)
        self.__valueSlider.setOrientation(QtCore.Qt.Horizontal)
        self.__valueSlider.setToolTip("Slide this to change the value")
        self.__valueSlider.setRange(0, 1000)
        self.__valueSlider.setValue(500)
        self.__valueSlider.setTickInterval(1)
        self.__valueSlider.setSingleStep(1)
        QtCore.QObject.connect(self.__valueSlider, QtCore.SIGNAL("valueChanged(int)"), self.__slider_value_changed)
        self.__resize_ui()
        self.hide()

    def __max_text_box_changed(self, value):
        if value is None or value == "":
            self.__maxTextBox.setText("0")
            return
        _max = float(value)
        if _max < self.__min:
            self.__maxTextBox.setText(str(self.__min))
            return
        self.__max = _max
        self.__scale = (self.__max - self.__min) / 1000.0
        self.__slider_value_changed(self.__valueSlider.value())

    def __min_text_box_changed(self, value):
        if value is None or value == "":
            self.__maxTextBox.setText("0")
            return
        _min = float(value)
        if _min > self.__max:
            self.__minTextBox.setText(str(self.__max))
            return
        self.__min = _min
        self.__scale = (self.__max - self.__min) / 1000.0
        self.__slider_value_changed(self.__valueSlider.value())

    def __slider_value_changed(self, value):
        value = self.__min + value * self.__scale
        self.__valueLabel.setText('%s: %.3f' % (self.__widgetLabelText, value))
        self.__valueLabel.adjustSize()
        self.__slider_changed(value)

    def __resize_ui(self):
        self.__valueSlider.resize(self.__width - 2*self.__textbox_w - 6, self.__textbox_h)
        self.__valueSlider.move(self.__textbox_w + 3, 15)
        self.__maxTextBox.move(self.__width - self.__textbox_w, 15)

    def resize(self, *__args):
        super(ControllerUI, self).resize(*__args)
        self.__width, self.__height = __args
        self.__resize_ui()


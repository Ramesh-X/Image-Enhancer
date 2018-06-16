from PyQt4 import QtCore, QtGui
import re


class FloatValidator(QtGui.QValidator):
    def __int__(self, parent=None):
        QtGui.QValidator.__init__(self, parent=parent)

    def fixup(self, p_object):
        p = re.compile(r'[0-9]+\.?[0-9]+')
        return p.search(p_object).group(1)

    def validate(self, p_object, p_int):
        try:
            float(p_object)
            return QtGui.QValidator.Acceptable
        except:
            return QtGui.QValidator.Invalid


class ControllerUI(QtGui.QWidget):
    def __init__(self, parent, widget_label, _max, _min, slider_changed):
        QtGui.QWidget.__init__(self, parent=parent)
        if _min >= _max:
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
        self.__setup_ui()

    def __setup_ui(self):
        # Value Slider Text
        self.__valueLabel = QtGui.QLabel(self.__widgetLabelText, self)
        self.__valueLabel.adjustSize()
        self.__valueLabel.move(self.__textbox_w + 5, 0)

        # Min TextBox
        self.__minTextBox = QtGui.QLineEdit(str(self.__min), self)
        QtCore.QObject.connect(self.__minTextBox, QtCore.SIGNAL("textChanged(QString)"), self.__min_text_box_changed)
        self.__minTextBox.setValidator(FloatValidator())
        self.__minTextBox.setToolTip("Set minimum value here")
        self.__minTextBox.resize(self.__textbox_w, self.__textbox_h)
        self.__minTextBox.move(0, 15)

        # Max TextBox
        self.__maxTextBox = QtGui.QLineEdit(str(self.__max), self)
        QtCore.QObject.connect(self.__minTextBox, QtCore.SIGNAL("textChanged(QString)"), self.__max_text_box_changed)
        self.__maxTextBox.setToolTip("Set maximum value here")
        self.__maxTextBox.setValidator(FloatValidator())
        self.__maxTextBox.resize(self.__textbox_w, self.__textbox_h)

        # Value Slider
        self.__valueSlider = QtGui.QSlider(self)
        self.__valueSlider.setOrientation(QtCore.Qt.Horizontal)
        self.__valueSlider.setRange(0, 1000)
        self.__valueSlider.setValue(500)
        self.__valueSlider.setTickInterval(1)
        self.__valueSlider.setSingleStep(1)
        QtCore.QObject.connect(self.__valueSlider, QtCore.SIGNAL("valueChanged(int)"), self.__slider_value_changed)
        self.__resize_ui()
        self.hide()

    def __max_text_box_changed(self, value):
        self.__max = float(value)
        self.__scale = (self.__max - self.__min) / 1000.0
        self.__slider_value_changed(self.__valueSlider.value())

    def __min_text_box_changed(self, value):
        self.__min = float(value)
        self.__scale = (self.__max - self.__min) / 1000.0
        self.__slider_value_changed(self.__valueSlider.value())

    def __slider_value_changed(self, value):
        value = self.__min + value * self.__scale
        self.__valueLabel.setText('%s: %f' % (self.__widgetLabelText, value))
        self.__slider_changed(value)

    def __resize_ui(self):
        self.__valueSlider.resize(self.__width - 2*self.__textbox_w - 6, self.__textbox_h)
        self.__valueSlider.move(self.__textbox_w + 3, 15)
        self.__maxTextBox.move(self.__width - self.__textbox_w, 15)

    def resize(self, *__args):
        super(ControllerUI, self).resize(*__args)
        self.__width, self.__height = __args
        self.__resize_ui()

from PyQt4 import QtCore, QtGui
import cv2

from .controller_ui import ControllerUI


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__originalImage = None
        self.__editedImage = None
        self.__imageMaxHeight = 663
        self.__imageMaxWidth = 1000
        self.__setup_ui()

    def __setup_ui(self):
        panel_ui = QtGui.QWidget(self)
        panel_ui_w = 300
        panel_ui_h = self.__imageMaxHeight + 50
        panel_ui.resize(panel_ui_w, panel_ui_h)
        panel_ui.move(0, 0)

        image_ui = QtGui.QWidget(self)
        image_ui_w = self.__imageMaxWidth + 20
        image_ui_h = panel_ui_h
        image_ui.resize(image_ui_w, image_ui_h)
        image_ui.move(panel_ui_w, 0)

        # Open Image Button
        self.__openImageButton = QtGui.QPushButton('Open Image', panel_ui)
        QtCore.QObject.connect(self.__openImageButton, QtCore.SIGNAL("clicked()"), self.__open_file)
        self.__openImageButton.move(15, 10)

        # Save Image Button
        self.__saveImageButton = QtGui.QPushButton('Save Image', panel_ui)
        QtCore.QObject.connect(self.__saveImageButton, QtCore.SIGNAL("clicked()"), self.__save_file)
        self.__saveImageButton.move(95, 10)

        # Original Select CheckBox
        self.__showOriginalCheckBox = QtGui.QCheckBox('Show Original', panel_ui)
        self.__showOriginalCheckBox.move(180, 15)
        QtCore.QObject.connect(self.__showOriginalCheckBox, QtCore.SIGNAL("stateChanged(int)"), self.__show_original_clicked)

        # Image info label
        self.__imageInfoLabel = QtGui.QLabel("Mouse hover the image to show the original image", image_ui)
        self.__imageInfoLabel.setStyleSheet('color: #606060; font-style: italic;')
        self.__imageInfoLabel.adjustSize()
        self.__imageInfoLabel.move(10, 10)

        # Image Label
        self.__imageLabel = QtGui.QLabel(image_ui)
        self.__imageLabel.setScaledContents(True)
        self.__imageLabel.setMinimumSize(1, 1)
        self.__imageLabel.move(10, 25)
        self.__imageLabel.installEventFilter(self)

        # Filter List Information
        self.__filterListInfoLabel = QtGui.QLabel("Right click on the list to add/remove filters", panel_ui)
        self.__filterListInfoLabel.setStyleSheet('color: #606060; font-style: italic;')
        self.__filterListInfoLabel.adjustSize()
        self.__filterListInfoLabel.move(20, 40)

        # Filter List Menu
        self.__filterListMenu = QtGui.QMenu()
        self.__filterListMenu.addAction("Remove Item")
        self.connect(self.__filterListMenu, QtCore.SIGNAL("triggered(QAction)"), self.__filter_list_menu_item_clicked)

        # Filters List
        self.__filterList = QtGui.QListWidget(panel_ui)
        self.__filterList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.__filterList.connect(self.__filterList, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.__filter_list_right_clicked)
        self.__filterList.resize(panel_ui_w - 40, panel_ui_h - 155)
        self.__filterList.move(20, 55)

        # Value Changer 1
        self.__valueChanger1 = ControllerUI(panel_ui, "Mess", 10, 1, self.__value_changer_1_changed)
        self.__valueChanger1.resize(panel_ui_w-40, 100)
        self.__valueChanger1.move(20, 58 + panel_ui_h - 155)
        self.__valueChanger1.show()

        self.resize(panel_ui_w + image_ui_w + 10, panel_ui_h + 15)

    def __value_changer_1_changed(self, value):
        print('Slider Changed: ', value)

    def __filter_list_menu_item_clicked(self, item):
        print("Item", item)

    def __filter_list_right_clicked(self, q_pos):
        parent_pos = self.__filterList.mapToGlobal(QtCore.QPoint(0, 0))
        self.__filterListMenu.move(parent_pos + q_pos)
        self.__filterListMenu.show()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Enter:
            print("Mouse Enter")
            return True
        if event.type() == QtCore.QEvent.Leave:
            print("Mouse Exit")
            return True
        return False

    def __show_original_clicked(self, state):
        self.__imageLabel.setScaledContents(not state)

    def __open_file(self):
        fd = QtGui.QFileDialog(self)
        self.__filename = fd.getOpenFileName()
        self.__originalImage = cv2.imread(self.__filename)
        self.__convert_image(True)

    def __save_file(self):
        pass

    def __convert_image(self, original):
        if original:
            cv_img = self.__originalImage
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


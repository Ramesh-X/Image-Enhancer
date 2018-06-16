from PyQt4 import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_notatnik()
        self.ui.setupUi(self)
        QtCore.QObject.connect(self.ui.button_open, QtCore.SIGNAL("clicked()"), self.file_dialog)
        QtCore.QObject.connect(self.ui.button_save, QtCore.SIGNAL("clicked()"), self.file_save)
        QtCore.QObject.connect(self.ui.editor_window, QtCore.SIGNAL("textChanged()"), self.enable_save)

    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.filename = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            s = codecs.open(self.filename, 'r', 'utf-8').read()
            self.ui.editor_window.setPlainText(s)
            # inserting text emits textChanged() so we disable the button :)
            self.ui.button_save.setEnabled(False)

    def enable_save(self):
        self.ui.button_save.setEnabled(True)

    def file_save(self):
        from os.path import isfile
        if isfile(self.filename):
            import codecs
            s = codecs.open(self.filename, 'w', 'utf-8')
            s.write(unicode(self.ui.editor_window.toPlainText()))
            s.close()
            self.ui.button_save.setEnabled(False)

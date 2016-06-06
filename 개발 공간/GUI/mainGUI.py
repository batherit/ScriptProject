import sys

from PyQt4 import QtGui, QtCore

import main_menu_ui
from searchGUI import *


class MyMainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        LoadXMLFromWeb()

        self.ui = main_menu_ui.Ui_Form()
        self.ui.setupUi(self)

    def menu_founds(self):
        self.foundsMenu = MyFoundsMenuForm()
        self.foundsMenu.show()
        self.close()
        return

    def menu_losts(self):
        self.lostsMenu = MyLostsMenuForm()
        self.lostsMenu.show()
        self.close()
        return



app = QtGui.QApplication(sys.argv)
myMainApp = MyMainForm()
myMainApp.show()
app.exec_()

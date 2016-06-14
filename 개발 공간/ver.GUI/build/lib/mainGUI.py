import sys

from PyQt4 import QtGui, QtCore

from searchGUI import *

def Run():
    app = QtGui.QApplication(sys.argv)
    myMainApp = MyMainForm()
    myMainApp.show()
    app.exec_()

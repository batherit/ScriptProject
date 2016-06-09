# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'losts_location_search_menu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1018, 560)
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(30, 150, 961, 331))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(10)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(230)
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 500, 121, 31))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_6 = QtGui.QPushButton(Form)
        self.pushButton_6.setGeometry(QtCore.QRect(900, 500, 93, 31))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(30, 500, 93, 31))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(530, 500, 121, 31))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(260, 20, 531, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 60, 281, 21))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(120, 30, 281, 21))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(40, 30, 64, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 60, 64, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(420, 30, 93, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL(_fromUtf8("cellClicked(int,int)")), Form.losts_print_detail)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.losts_location_search)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_back)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_prev)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_next)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.return_to_main)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "위치 기반 분실물 검색", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "품명", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "분실 일자", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "분실 위치", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "내용", None))
        self.pushButton_4.setText(_translate("Form", "<<", None))
        self.pushButton_6.setText(_translate("Form", "처음으로", None))
        self.pushButton_5.setText(_translate("Form", "뒤로 가기", None))
        self.pushButton_3.setText(_translate("Form", ">>", None))
        self.groupBox.setTitle(_translate("Form", "분실물에 관한 정보 입력", None))
        self.label.setText(_translate("Form", "분실 위치", None))
        self.label_2.setText(_translate("Form", "품명 입력", None))
        self.pushButton.setText(_translate("Form", "검색", None))


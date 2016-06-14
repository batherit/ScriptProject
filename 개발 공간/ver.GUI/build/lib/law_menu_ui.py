# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'law_menu.ui'
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
        Form.resize(689, 392)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(290, 330, 101, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 19, 671, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 641, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 511, 31))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 170, 671, 141))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(110, 100, 421, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 581, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(20, 70, 581, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "유실물 처리 절차", None))
        self.pushButton.setText(_translate("Form", "닫기", None))
        self.groupBox.setTitle(_translate("Form", "물품 이관 전", None))
        self.label_2.setText(_translate("Form", "지하철, 철도, 버스, 택시, 공항, 유관기관 : 7일 보관 후 경찰서 또는 유실물 센터로 물품이관", None))
        self.label.setText(_translate("Form", "우체국 : 즉시 경찰서 또는 유실물센터로 물품이관", None))
        self.groupBox_2.setTitle(_translate("Form", "물품 이관 후", None))
        self.label_5.setText(_translate("Form", "습득자 미수령시 3개월 기간 경과 후 -> 국고 귀속 및 폐기", None))
        self.label_3.setText(_translate("Form", "분실한 경우 : 6개월 기간 경과 후 -> 국고귀속 및 폐기", None))
        self.label_4.setText(_translate("Form", "습득한 경우 : 6개월 기간 경과 후 -> 습득자 소유권 취득", None))


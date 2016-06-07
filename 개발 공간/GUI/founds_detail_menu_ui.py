# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'founds_detail_menu.ui'
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
        Form.resize(935, 531)
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 591, 441))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(9)
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
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.tableWidget.setItem(8, 0, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(500)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(330, 480, 131, 41))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 480, 131, 41))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(482, 480, 131, 41))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(640, 70, 261, 151))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.listWidget_2 = QtGui.QListWidget(Form)
        self.listWidget_2.setGeometry(QtCore.QRect(640, 310, 261, 151))
        self.listWidget_2.setObjectName(_fromUtf8("listWidget_2"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(710, 40, 141, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(710, 280, 131, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setGeometry(QtCore.QRect(650, 480, 241, 41))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_5 = QtGui.QPushButton(Form)
        self.pushButton_5.setGeometry(QtCore.QRect(180, 480, 131, 41))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.click_close)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.transmit_email)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.put_on_list)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.transmit_email_list)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.print_image)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "습득물 상세 정보", None))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "물품명", None))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "습득 일자", None))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("Form", "습득 시간", None))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("Form", "습득 장소", None))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("Form", "관리 ID", None))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("Form", "보관 상태", None))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("Form", "보관 장소", None))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("Form", "문의번호", None))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("Form", "특이사항", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "내용", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("Form", "이메일 전송", None))
        self.pushButton_2.setText(_translate("Form", "창 닫기", None))
        self.pushButton_3.setText(_translate("Form", "정보 담기", None))
        self.label.setText(_translate("Form", "습득물 정보 목록", None))
        self.label_2.setText(_translate("Form", "분실물 정보 목록", None))
        self.pushButton_4.setText(_translate("Form", "정보 목록 이메일 전송", None))
        self.pushButton_5.setText(_translate("Form", "이미지 보기", None))


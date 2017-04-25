# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClientLogin.ui'
#
# Created: Mon Apr 24 09:52:11 2017
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(335, 255)
        Dialog.setStyleSheet(_fromUtf8("background:#FFEFD5;\n"
"color: black;"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title = QtGui.QFrame(self.widget)
        self.title.setFrameShape(QtGui.QFrame.StyledPanel)
        self.title.setFrameShadow(QtGui.QFrame.Raised)
        self.title.setObjectName(_fromUtf8("title"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.title)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.appName = QtGui.QLabel(self.title)
        self.appName.setAlignment(QtCore.Qt.AlignCenter)
        self.appName.setObjectName(_fromUtf8("appName"))
        self.horizontalLayout.addWidget(self.appName)
        spacerItem = QtGui.QSpacerItem(156, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.miniBt = QtGui.QPushButton(self.title)
        self.miniBt.setMinimumSize(QtCore.QSize(25, 25))
        self.miniBt.setMaximumSize(QtCore.QSize(25, 25))
        self.miniBt.setObjectName(_fromUtf8("miniBt"))
        self.horizontalLayout.addWidget(self.miniBt)
        self.closeBt = QtGui.QPushButton(self.title)
        self.closeBt.setMinimumSize(QtCore.QSize(25, 25))
        self.closeBt.setMaximumSize(QtCore.QSize(25, 25))
        self.closeBt.setObjectName(_fromUtf8("closeBt"))
        self.horizontalLayout.addWidget(self.closeBt)
        self.verticalLayout.addWidget(self.title)
        self.frame = QtGui.QFrame(self.widget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label = QtGui.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.username_val = QtGui.QLineEdit(self.frame)
        self.username_val.setObjectName(_fromUtf8("username_val"))
        self.horizontalLayout_3.addWidget(self.username_val)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(self.widget)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.ip = QtGui.QLabel(self.frame_2)
        self.ip.setObjectName(_fromUtf8("ip"))
        self.horizontalLayout_2.addWidget(self.ip)
        self.ip_val = QtGui.QLineEdit(self.frame_2)
        self.ip_val.setObjectName(_fromUtf8("ip_val"))
        self.horizontalLayout_2.addWidget(self.ip_val)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(self.widget)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem5 = QtGui.QSpacerItem(43, 16, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.portname = QtGui.QLabel(self.frame_3)
        self.portname.setAlignment(QtCore.Qt.AlignCenter)
        self.portname.setObjectName(_fromUtf8("portname"))
        self.horizontalLayout_4.addWidget(self.portname)
        self.port_val = QtGui.QLineEdit(self.frame_3)
        self.port_val.setObjectName(_fromUtf8("port_val"))
        self.horizontalLayout_4.addWidget(self.port_val)
        spacerItem6 = QtGui.QSpacerItem(43, 16, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout.addWidget(self.frame_3)
        self.loginBt = QtGui.QPushButton(self.widget)
        self.loginBt.setMinimumSize(QtCore.QSize(30, 30))
        self.loginBt.setObjectName(_fromUtf8("loginBt"))
        self.verticalLayout.addWidget(self.loginBt)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.appName.setText(_translate("Dialog", "五子棋", None))
        self.miniBt.setText(_translate("Dialog", "-", None))
        self.closeBt.setText(_translate("Dialog", "X", None))
        self.label.setText(_translate("Dialog", "昵称：", None))
        self.ip.setText(_translate("Dialog", "IP地址:", None))
        self.portname.setText(_translate("Dialog", "端口：", None))
        self.loginBt.setText(_translate("Dialog", "登录", None))


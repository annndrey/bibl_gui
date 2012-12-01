# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_database.ui'
#
# Created: Tue Mar 16 14:35:14 2010
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_selectDB(object):
    def setupUi(self, selectDB):
        selectDB.setObjectName("selectDB")
        selectDB.resize(287,223)
        self.gridLayout = QtGui.QGridLayout(selectDB)
        self.gridLayout.setObjectName("gridLayout")
        self.dbName = QtGui.QLabel(selectDB)
        self.dbName.setObjectName("dbName")
        self.gridLayout.addWidget(self.dbName,0,2,1,1)
        self.lineEditName = QtGui.QLineEdit(selectDB)
        self.lineEditName.setObjectName("lineEditName")
        self.gridLayout.addWidget(self.lineEditName,0,3,1,1)
        self.lineEditAddress = QtGui.QLineEdit(selectDB)
        self.lineEditAddress.setObjectName("lineEditAddress")
        self.gridLayout.addWidget(self.lineEditAddress,1,3,1,1)
        self.dbAddress = QtGui.QLabel(selectDB)
        self.dbAddress.setObjectName("dbAddress")
        self.gridLayout.addWidget(self.dbAddress,1,2,1,1)
        self.lineEditUser = QtGui.QLineEdit(selectDB)
        self.lineEditUser.setObjectName("lineEditUser")
        self.gridLayout.addWidget(self.lineEditUser,2,3,1,1)
        self.dbUser = QtGui.QLabel(selectDB)
        self.dbUser.setObjectName("dbUser")
        self.gridLayout.addWidget(self.dbUser,2,2,1,1)
        self.lineEditPasswd = QtGui.QLineEdit(selectDB)
        self.lineEditPasswd.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditPasswd.setObjectName("lineEditPasswd")
        self.gridLayout.addWidget(self.lineEditPasswd,3,3,1,1)
        self.dbPasswd = QtGui.QLabel(selectDB)
        self.dbPasswd.setObjectName("dbPasswd")
        self.gridLayout.addWidget(self.dbPasswd,3,2,1,1)
        self.buttonBox = QtGui.QDialogButtonBox(selectDB)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox,4,3,1,1)

        self.retranslateUi(selectDB)
        #QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),selectDB.accept)
        #QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),selectDB.reject)
        QtCore.QMetaObject.connectSlotsByName(selectDB)

    def retranslateUi(self, selectDB):
        selectDB.setWindowTitle(QtGui.QApplication.translate("selectDB", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.dbName.setText(QtGui.QApplication.translate("selectDB", "Название", None, QtGui.QApplication.UnicodeUTF8))
        #self.lineEditName.setText(QtGui.QApplication.translate("selectDB", "bibliography", None, QtGui.QApplication.UnicodeUTF8))
        #self.lineEditAddress.setText(QtGui.QApplication.translate("selectDB", "192.168.0.126", None, QtGui.QApplication.UnicodeUTF8))
        self.dbAddress.setText(QtGui.QApplication.translate("selectDB", "Адрес ", None, QtGui.QApplication.UnicodeUTF8))
        #self.lineEditUser.setText(QtGui.QApplication.translate("selectDB", "annndrey", None, QtGui.QApplication.UnicodeUTF8))
        self.dbUser.setText(QtGui.QApplication.translate("selectDB", "Имя пользователя", None, QtGui.QApplication.UnicodeUTF8))
        #self.lineEditPasswd.setText(QtGui.QApplication.translate("selectDB", "", None, QtGui.QApplication.UnicodeUTF8))
        self.dbPasswd.setText(QtGui.QApplication.translate("selectDB", "Пароль", None, QtGui.QApplication.UnicodeUTF8))


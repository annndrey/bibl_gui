# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auto.ui'
#
# Created: Mon May 17 12:35:58 2010
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui


#Тут мы пробуем переписать базовый класс QLineEdit, добавив туда кое-что от ListModel/ListView
class ExtLineEdit(QtGui.QLineEdit):
    def __init__(self, parent = None):
        QtGui.QLineEdit.__init__(self, parent)
    def print_ok(self):
        print "OK"












#Это класс диалога, он нам пока не понадобится.
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511,205)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ExtLineEdit = ExtLineEdit(Dialog)
        self.ExtLineEdit.setObjectName("ExtLineEdit")
        self.verticalLayout.addWidget(self.ExtLineEdit)
        self.listView = QtGui.QListView(Dialog)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        #self.comboBox = QtGui.QComboBox()
        #self.verticalLayout.addWidget(self.comboBox)
        #self.comboBox.setObjectName("comboBox")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),self.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),self.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

    def accept(self):
        print "OK"
    def reject(self):
        self.close()

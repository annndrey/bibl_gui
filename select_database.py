# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_database.ui'
#
# Created: Tue Mar  9 17:31:13 2010
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_sel_database(object):
    def setupUi(self, sel_database):
        sel_database.setObjectName("sel_database")
        sel_database.resize(416,165)
        self.verticalLayout = QtGui.QVBoxLayout(sel_database)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(sel_database)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(sel_database)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.buttonBox = QtGui.QDialogButtonBox(sel_database)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(sel_database)
        #QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),sel_database.accept)
        #QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),sel_database.reject)
        #QtCore.QMetaObject.connectSlotsByName(sel_database)

    def retranslateUi(self, sel_database):
        sel_database.setWindowTitle(QtGui.QApplication.translate("sel_database", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("sel_database", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Выбор базы данных</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("sel_database", "хитозан", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("sel_database", "хитозанплюс", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("sel_database", "хитозанминус", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'database_info.ui'
#
# Created: Tue Mar  9 16:22:44 2010
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(318,218)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtGui.QTextBrowser(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(200)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(300,200))
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.textBrowser.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600;\">База данных хитозанплюс</span></p>\n"
"<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">В базе </span><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600;\">ХИТОЗАНПЛЮС</span><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\"> содержится </span><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600;\">18750</span><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\"> записей, </span><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600;\">40</span><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\"> полей, размер базы - </span><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600;\">150</span><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\"> Mb, последний раз редактировалась </span><span style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600;\">10/11/12</span><span style=\" font-family:\'Sans Serif\'; font-size:9pt;\">.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


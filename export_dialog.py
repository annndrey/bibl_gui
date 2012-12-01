# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'export_dialog.ui'
#
# Created: Mon Nov 15 19:49:00 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class ExportDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("ExportForm")
        Dialog.resize(264, 114)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 1, 0, 1, 2)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.sep_comboBox = QtGui.QComboBox(Dialog)
        self.sep_comboBox.setObjectName("sep_comboBox")
        self.sep_comboBox.addItem("")
        self.sep_comboBox.addItem("")
        self.sep_comboBox.addItem("")
        self.sep_comboBox.setEditable(True)
        self.gridLayout.addWidget(self.sep_comboBox, 2, 1, 1, 1)
        self.typeComboBox = QtGui.QComboBox(Dialog)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.gridLayout.addWidget(self.typeComboBox, 3, 1, 1, 1)

        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        #self.pb = QtGui.QProgressBar()
        #self.gridLayout.addWidget(self.pb, 4, 0, 1, 2)
        self.retranslateUi(Dialog)
        self.connect(self.typeComboBox, QtCore.SIGNAL("currentIndexChanged(QString)"), self.change_state)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", u"Экспорт данных", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Экспортировать", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Разделитель поля:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Формат файла:", None, QtGui.QApplication.UnicodeUTF8))
        self.sep_comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "{tab}", None, QtGui.QApplication.UnicodeUTF8))
        self.sep_comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", ";", None, QtGui.QApplication.UnicodeUTF8))
        self.sep_comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", ",", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", ".csv", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", ".xls", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", ".tex", None, QtGui.QApplication.UnicodeUTF8))

    def change_state(self):
        if self.sep_comboBox:
            if self.typeComboBox.currentText() == QtCore.QString(".xls"):
                self.sep_comboBox.setEnabled(False)
            else:
                self.sep_comboBox.setEnabled(True)

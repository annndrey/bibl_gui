# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tree_form.ui'
#
# Created: Fri Sep 17 20:01:34 2010
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Tree_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("DuplForm")
        Dialog.resize(350,500)
        
        self.verticalLayout = QtGui.QGridLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtGui.QTreeView(Dialog)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView,0,0,1,4)

        self.comboBox = QtGui.QComboBox()
        self.comboBox.setObjectName('comboBox')
        for i in [u'Авторы', u'Название (ориг.)', u'Источник', u'Редактор', u'Место издания', u'Издательство']:
            self.comboBox.addItem(i)#QtGui.QApplication.translate("DuplForm", i, None, QtGui.QApplication.UnicodeUTF8))
        
        self.comboBoxProcessed = QtGui.QComboBox()
        self.comboBoxProcessed.setObjectName("comboBoxProcessed")
        for i in (u'Необработанные', u'Обработанные', u'Все'):
            self.comboBoxProcessed.addItem(i)#QtGui.QApplication.translate("DuplForm", i, None, QtGui.QApplication.UnicodeUTF8))
        
            
        self.label = QtGui.QLabel()
        self.label.setText(u"Найти дубли для")
        self.spin = QtGui.QDoubleSpinBox()
        self.spin.setRange(0,1)
        self.spin.setSingleStep(0.05)
        self.spin.setValue(0.5)
        
        self.verticalLayout.addWidget(self.label, 1,0)

        self.verticalLayout.addWidget(self.comboBox, 1,1)
        
        self.verticalLayout.addWidget(self.spin, 1,2)
        
        self.verticalLayout.addWidget(self.comboBoxProcessed, 1, 3)

        self.rmButton=QtGui.QPushButton()
        self.rmButton.setText(u'Удалить строку')
        self.verticalLayout.addWidget(self.rmButton, 2,0)

        self.addButton = QtGui.QPushButton()
        self.addButton.setText(u'Добавить строку')
        self.verticalLayout.addWidget(self.addButton, 2,1)

        self.addBranchButton = QtGui.QPushButton()
        self.addBranchButton.setText(u'Добавить ветвь')
        self.verticalLayout.addWidget(self.addBranchButton, 2,2)
        

        self.mainEntryButton = QtGui.QPushButton()
        self.mainEntryButton.setText(u'Главная запись')
        self.verticalLayout.addWidget(self.mainEntryButton, 3,0)

        self.delDuplButton = QtGui.QPushButton()
        self.delDuplButton.setText(u'Удалить дубль из базы')
        self.verticalLayout.addWidget(self.delDuplButton, 3,2)

        self.createListButton = QtGui.QPushButton()
        self.createListButton.setText(u'Заменить синонимы')
        self.verticalLayout.addWidget(self.createListButton, 3,1)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        
        self.buttonBox.setObjectName("treebuttonBox")
        self.verticalLayout.addWidget(self.buttonBox, 4,0,1,4)

        #print self.comboBox.currentText().toUtf8() 
        
        self.delDuplButton.setEnabled(False)
        self.retranslateUi(Dialog)
        self.connect(self.comboBox,QtCore.SIGNAL("currentIndexChanged(QString)"),self.changeActive)
        #QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        #QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        #QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Поиск дублей", "Поиск дублей", None, QtGui.QApplication.UnicodeUTF8))

    def changeActive(self, text):
        text = str(text.toUtf8())
        #text = self.comboBox.currentText().toUtf8()
        #print text
        #print 'Названиие (ориг.)'
        if text == 'Название (ориг.)':
            self.rmButton.setEnabled(False)
            self.addButton.setEnabled(False)
            self.addBranchButton.setEnabled(False)
            self.mainEntryButton.setEnabled(True)
            self.createListButton.setEnabled(False)
            self.delDuplButton.setEnabled(True)
        else:
            self.rmButton.setEnabled(True)
            self.addButton.setEnabled(True)
            self.addBranchButton.setEnabled(True)
            self.mainEntryButton.setEnabled(True)
            self.createListButton.setEnabled(True)
            self.delDuplButton.setEnabled(False)

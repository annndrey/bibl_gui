# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query_list.ui'
#
# Created: Wed Dec 15 15:29:34 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class QueryListForm(object):
    def setupUi(self, QueryList):
        QueryList.setObjectName("QueryList")
        QueryList.resize(277, 373)
        self.verticalLayout = QtGui.QVBoxLayout(QueryList)
        self.verticalLayout.setObjectName("verticalLayout")

        self.listView = QtGui.QListView(QueryList)
        self.listView.setSelectionMode(2)
        #self.scrollArea = QtGui.QScrollArea(self.listView)
        #self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setObjectName("scrollArea")
        #self.scrollArea.setWidget(self.listView)
        self.listView.setObjectName("listView")
        self.listView.setMinimumHeight(250)
        self.verticalLayout.addWidget(self.listView)

        self.textBrowser = QtGui.QTextEdit(QueryList)
        self.textBrowser.setObjectName("TextEdit")
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setMinimumHeight(50)
        self.verticalLayout.addWidget(self.textBrowser)


        self.prevQuery = QtGui.QPushButton()
        self.prevQuery.setObjectName("prevQuery")
        self.prevQuery.setText(u"Следующий запрос")
        self.verticalLayout.addWidget(self.prevQuery)

        self.nextQuery = QtGui.QPushButton()
        self.nextQuery.setObjectName("nextQuery")
        self.nextQuery.setText(u"Предыдущий запрос")
        self.verticalLayout.addWidget(self.nextQuery)

        self.execQueries = QtGui.QPushButton()
        self.execQueries.setObjectName("execQueries")
        self.execQueries.setText(u"Выполнить")
        self.verticalLayout.addWidget(self.execQueries)
        

        self.deleteLineButton = QtGui.QPushButton()
        self.deleteLineButton.setObjectName("deleteLineButton")
        self.deleteLineButton.setText(u"Удалить")
        self.verticalLayout.addWidget(self.deleteLineButton)

        self.buttonBox = QtGui.QDialogButtonBox(QueryList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.setMinimumHeight(350)

        self.retranslateUi(QueryList)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), QueryList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.close)
        
        #QtCore.QMetaObject.connectSlotsByName(QueryList)




    def retranslateUi(self, QueryList):
        QueryList.setWindowTitle(QtGui.QApplication.translate("QueryList", "История поиска", None, QtGui.QApplication.UnicodeUTF8))


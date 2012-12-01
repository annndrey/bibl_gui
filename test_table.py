#!/usr/bin/python                                                                                                                                    
# -*- coding: utf-8 -*-


from PyQt4 import QtGui, QtCore
import sys

class PushButtonDelegate(QtGui.QItemDelegate):
    def __init__(self, parent):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent
    def paint(self, painter, option, index):
        if index.column() == 1:
            Option = QtGui.QStyleOptionButton()
            Option.state = QtGui.QStyle.State_Enabled
            Option.direction = QtGui.QApplication.layoutDirection();
            Option.rect = option.rect;
            Option.fontMetrics = QtGui.QApplication.fontMetrics();
            Option.text = 'Button'
            QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_PushButton, Option, painter);
        else:
            QtGui.QItemDelegate.paint(self, painter, option, index)
    def createEditor(self, parent, option, index):
        editor = QtGui.QPushButton(parent)
        return editor
    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.EditRole).toString()
        editor.setText(value)
    def setModelData(self, editor, model, index):
        value = editor.text()
        model.setData(index, value, QtCore.Qt.EditRole)
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
class Model(QtCore.QAbstractTableModel):
    def __init__(self, parent):
        QtCore.QAbstractTableModel.__init__(self)
        self.gui = parent
        self.colLabels = ['Col1', 'Col2', 'Col3', 'Col4', 'Col5']
        self.cached = [
                        ['cell11','cell12','cell13','cell14','cell15',],
                        ['cell21','cell22','cell23','cell24','cell25',],
                        ['cell31','cell32','cell33','cell34','cell35',],
                        ['cell41','cell42','cell43','cell44','cell45',],
                        ['cell51','cell52','cell53','cell54','cell55',],
                        ['cell61','cell62','cell63','cell64','cell65',],
                        ['cell71','cell72','cell73','cell74','cell75',],
                        ['cell81','cell82','cell83','cell84','cell85',],
                    ]
    def rowCount(self, parent):
        return len(self.cached)
    def columnCount(self, parent):
        return len(self.colLabels)
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
            return QtCore.QVariant()
        value = ''
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.cached[row][col]
        elif role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            value = self.cached[row][col]
        return QtCore.QVariant(value)
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self.cached[index.row()][index.column()] = QtCore.QVariant(value)
            self.emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        else:
            return False
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.colLabels[section])
        return QtCore.QVariant()

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.table = QtGui.QTableView(self)
        self.table.setAlternatingRowColors(True)
        self.model = Model(self.table)
        self.table.setModel(self.model)
        self.delegate = PushButtonDelegate(self.model)
        self.table.setItemDelegate(self.delegate)
        self.setCentralWidget(self.table)
        
class App(QtGui.QApplication):
    def __init__(self, argv):
        QtGui.QApplication.__init__(self, argv)
        self.ui = MainWindow(None)
        self.ui.show()

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())

#!/usr/bin/python
# -*- coding: utf-8 -*-

# using PyQT's QListView and QAbstractListModel
# to match partially typed word to words in list
# make matching case insensitive
# tested with Python 3.1 and PyQT 4.5
# Henri

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyWindow(QWidget):
    def __init__(self, words, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 300, 320, 250)
        self.setWindowTitle("Match words with PyQT's QListView")
        self.words = words

        # create objects
        self.label = QLabel("Start typing to match words in list:")
        #self.edit = MyLineEdit()
        self.edit = QComboBox()
        self.edit.setEditable(True)
        self.lmodel = MyListModel(self, self.words)
        self.lview = QListView()
        self.lview.setModel(self.lmodel)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        layout.addWidget(self.lview)
        self.setLayout(layout)

        # one key has been pressed in edit
        self.connect(self.edit, SIGNAL("textChanged(QString)"),
                     self.update)

    def update(self):
        """
        updates the list of possible completions each time key
        is pressed, use lower() to make things case insensitive
        """
        p = str(self.edit.currentText()).lower()
        new_list = [w for w in self.words if w.lower().find(p)==0]
        self.lmodel.setAllData(new_list)


class MyListModel(QAbstractListModel):
    def __init__(self, parent, words, *args):
        """
        words is list of words
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.words = words

    def rowCount(self, parent=QModelIndex()):
        return len(self.words)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.words[index.row()])
        else:
            return QVariant()

    def setAllData(self, new_list):
        """replace old list with new list"""
        self.words = new_list
        self.reset()


# this is just test list of words
state_list = [
'Mississippi', 'Oklahoma', 'Delaware', 'Minnesota',
'Arkansas', 'New Mexico', 'Indiana', 'Louisiana',
'Texas', 'Wisconsin', 'Kansas', 'Connecticut',
'California', 'West Virginia', 'Georgia', 'North Dakota',
'Pennsylvania', 'Alaska', 'Missouri', 'South Dakota',
'Colorado', 'New Jersey', 'Washington', 'New York',
'Nevada', 'Maryland', 'Idaho', 'Wyoming', 'Maine',
'Arizona', 'Iowa', 'Michigan', 'Utah', 'Illinois',
'Virginia', 'Oregon', 'Montana', 'New Hampshire',
'Massachusetts', 'South Carolina', 'Vermont', 'Florida',
'Hawaii', 'Kentucky', 'Rhode Island', 'Nebraska',
'Ohio', 'Alabama', 'North Carolina', 'Tennessee'
]

app = QApplication(sys.argv)
win = MyWindow(state_list)
win.show()
sys.exit(app.exec_())

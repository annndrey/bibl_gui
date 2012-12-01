#!/usr/bin/python
# -*- coding: utf-8 -*-


import psycopg2
import os, sys, datetime, time, operator, copy
from PyQt4 import QtCore, QtGui
from auto import Ui_Dialog as Dialog

dbname = "bibliography"
user = 'annndrey'
host = "localhost"
passwd = "andreygon"

class MainView(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Dialog()
        self.ui.setupUi(self)
        self.words = []
        self.listModel = ListModel(self, self.words)
        self.ui.listView.setModel(self.listModel)
        self.ui.listView.hide()
        self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s'  password='%s'" % (dbname, user, host, passwd))

        self.connect(self.ui.ExtLineEdit, QtCore.SIGNAL("textChanged(QString)"), self.print_text)
        self.connect(self.ui.listView, QtCore.SIGNAL("activated(QModelIndex)"), self.set_text)
        self.connect(self.ui.ExtLineEdit, QtCore.SIGNAL("textChanged(QString)"), self.ui.ExtLineEdit.print_ok)
        self.cur = self.conn.cursor()

    #Добавляет выделенный текст к строке ввода
    def set_text(self):
        prev_string = unicode(self.ui.ExtLineEdit.text())
        
        prev_list = prev_string.split(",")
        del(prev_list[-1])
        prev_string = ",".join(prev_list) 
        list_string = unicode(self.ui.listView.currentIndex().data().toString())
        fut_string = []
        fut_string.append([prev_string, list_string])
        #print fut_string
#        print prev_string, self.ui.listView.currentIndex().data().toString()
        if len(prev_string) > 1:
            self.ui.ExtLineEdit.setText(prev_string + ", " + list_string)# + self.ui.listView.currentIndex().data().toString().lstrip(prev_string))
        else:
            self.ui.ExtLineEdit.setText(list_string)

        #print self.ui.listView.currentIndex().data().toString()
        self.listModel.setAllData([])
        self.ui.listView.hide()
        self.ui.ExtLineEdit.setFocus()

    #Осуществляет поиск последнего введенного слова
    def print_text(self):
        
        self.words.append(self.ui.ExtLineEdit.text())
        if len(self.ui.ExtLineEdit.text()) > 0:

            a = unicode(self.ui.ExtLineEdit.text()).split(",")
            for i in xrange(len(a)):
                a[i] = a[i].replace(" ", "")
                if len(a[i]) == 0:
                    del a[i]
            

            self.cur.execute("""select location from publ_location where location ilike '%s%%'""" %  unicode(a[-1]))
            rest = []
            for i in xrange(self.cur.rowcount):
                rest.append(self.cur.fetchone()[0].decode("utf-8"))
            self.ui.listView.show()
            rest.sort()
            self.listModel.setAllData(rest)

        else:
            self.ui.listView.hide()

class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent, words, *args):
        QtCore.QAbstractListModel.__init__(self, parent, *args)
        self.words = []
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.words)

    def data(self, index, role):

        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.words[index.row()])
        else:
            return QtCore.QVariant()
        
    def setAllData(self, new_list):
        self.words = new_list
        self.reset()
        
def main():

    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    window=MainView()
    window.setWindowTitle(u'База данных')
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()


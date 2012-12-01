#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import psycopg2
from search import Ui_Form as SearchUiForm

dbname='bibliography'
user='annndrey'
host='localhost'
password='andreygon'
cols = ('authors', 'name_orig', 'source', 'editor', 'year', 'language', 'file_path', 'abstract')
query = 'select authors, name_orig, year from articles'

def main():
    app = QApplication(sys.argv)
    app.setStyle('cleanlooks')
    w = tableViewWindow()
    w.show()
    sys.exit(app.exec_())

class tableViewWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s'  password='%s'" % (dbname, user, host, password))
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        self.query = query
        # create table
        table = self.createTable(self.query)
        self.uiSearch = Search_Form()
        self.uiSearch.show()
        
        # layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)
        self.connect(self.uiSearch.pushButton, SIGNAL('clicked()'), self.uiSearch.fulltext_search)
        self.connect(self.uiSearch.pushButton, SIGNAL('clicked()'), self.uiSearch.fulltext_search)

    def ft_search(self, *args):
        self.query = unicode(self.uiSearch.lineEdit.text())
        

    def createTable(qu, self):
        
        tv = QTableView()
        query = qu
        
        tm = biblTableModel(query, self)
        tv.setModel(tm)

        
        tv.setMinimumSize(640, 480)
        vh = tv.verticalHeader()
        vh.setVisible(True)

        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)


        #tv.resizeColumnsToContents()
        # set row height
        #nrows = tm.rowCount(self)
        #for row in xrange(nrows):
        #    tv.setRowHeight(row, 60)
        return tv

class biblTableModel(QAbstractTableModel):
    def __init__(self, query, parent=None, *args):
        QAbstractTableModel.__init__(self,  parent, *args)
        self.conn = psycopg2.connect("dbname='%s' user='%s' host='%s'  password='%s'" % (dbname, user, host, password))
        self.cur = self.conn.cursor()
        self.cur.execute(query)
        self.dbdata = self.cur.fetchall()

    def rowCount(self, parent):
        #кол-во строк
        return len(self.dbdata)

    def columnCount(self, parent):
        #кол-во колонок
        return len(self.dbdata[0])

    def data(self, index, role):
        #тут фунция вытягивания данных
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        # для отладки-можно видеть обращения к функции

        print QString(u"cell ")+str(index.row())+"-"+str(index.column())
        return QVariant((self.dbdata[index.row()][index.column()]).decode("utf-8"))

    def headerData(self, col, orientation, role):
        ## тут задаются заголовки
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(cols[col])
        return QVariant()


class Search_Form(QWidget, SearchUiForm):

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

    def search_show(self):
        self.show()

    def fulltext_search(self):
        text = self.lineEdit.text
        return text


if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


import psycopg2


conn = psycopg2.connect("dbname='bibliography' user='annndrey' host='piggy.thruhere.net'  password='andreygon'")
cur = conn.cursor()

class Table(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)


    cur.execute("select authors, name_orig, year from articles limit 10")
    r = cur.rowcount
    table = Table(r, 3)
    
    i = j = 0
    text = u'Превед!!'

    for j in xrange(r):
        f = cur.fetchone()
        a = f[0]
        b = f[1]
        c = f[2]
        table_item = QTableWidgetItem(QString(a))
        table.setItem(j, 0, table_item)
        table_item = QTableWidgetItem(QString(b))
        table.setItem(j, 1, table_item)
        table_item = QTableWidgetItem(QString(c))
        table.setItem(j, 2, table_item)

#        print "%s, %s, %s" % (a, b, c)
    table.resize(640, 480)
    table.show()
    app.exec_()
#    for i in xrange(cur.rowcount):
#        a = cur.fetchone()
#        for i in a:
#            print i

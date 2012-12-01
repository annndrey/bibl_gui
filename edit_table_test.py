#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, QtSql


class MyWindow(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        # create table
        table = FreezeTableWidget(self)

        # layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


class FreezeTableWidget(QtGui.QTableView):
    def __init__(self, parent = None, *args):
        QtGui.QTableView.__init__(self, parent, *args)

        # Минимальный размер окна
        self.setMinimumSize(800, 600)

        # set the table model
        tm = MyTableModel(self)

        # set the proxy model
        pm = QtGui.QSortFilterProxyModel(self)
        pm.setSourceModel(tm)

        # назначаем модель данных для TableView
        self.setModel(pm)

        # ***ВИДЖЕТ ЗАФИКСИРОВАННЫХ СТОЛБЦОВ***
        #  (будет расположен поверх основного)
        self.frozenTableView = QtGui.QTableView(self)
        # устанавливаем модель для виджета зафиксированных столбцов
        self.frozenTableView.setModel(pm)
        # скрываем заголовки строк
        self.frozenTableView.verticalHeader().hide()
        # виджет не принимает фокус
        self.frozenTableView.setFocusPolicy(QtCore.Qt.NoFocus)
        # пользователь не может изменять размер столбцов
        self.frozenTableView.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        # отключаем показ границ виджета
        self.frozenTableView.setStyleSheet('''border: none; background-color: #8EDE21; 
                                       selection-background-color: #999''')
        # режим выделения как у основного виджета
        self.frozenTableView.setSelectionModel(QtGui.QAbstractItemView.selectionModel(self))
        # убираем полосы прокрутки
        self.frozenTableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # помещает дополнительный виджет на передний план
        self.viewport().stackUnder(self.frozenTableView)

        # Вход в режим редактирования - еще одним щелчком мыши
        self.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked)

        # hide gridnt()
#        self.setShowGrid(False)

        # Установка шрифта
        self.setStyleSheet('font: 10pt "Courier New"')

        # Установка свойств заголовков столбцов
        hh = self.horizontalHeader()
        # выравнивание текста по центру
        hh.setDefaultAlignment(QtCore.Qt.AlignCenter)
        # включаем растягивание последнего столбца
        hh.setStretchLastSection(True)

        # Установка ширины столбцов по содержимому
#        self.resizeColumnsToContents()

        # Установка ширины столбцов
        ncol = tm.columnCount(self)
        for col in xrange(ncol):
            if col == 0:
                # устанавливаем размер
                self.horizontalHeader().resizeSection(col, 60)
                # фиксируем ширину
                self.horizontalHeader().setResizeMode(col, QtGui.QHeaderView.Fixed)
                # ширина фиксированных столбцов - как у основного виджета
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
            elif col == 1:
                self.horizontalHeader().resizeSection(col, 150)
                self.horizontalHeader().setResizeMode(col, QtGui.QHeaderView.Fixed)
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
            else:
                self.horizontalHeader().resizeSection(col, 100)
                # скрываем не нужные столбцы у виджета зафиксированных столбцов
                self.frozenTableView.setColumnHidden(col, True)

        # Сортировка по щелчку на заголовке столбца
        self.frozenTableView.setSortingEnabled(True)
        self.frozenTableView.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # Включаем чередующуюся подсветку строк
        self.setAlternatingRowColors(True)

        # Установка свойств заголовков строк
        vh = self.verticalHeader()
        vh.setDefaultSectionSize(25) # высота строк
        vh.setDefaultAlignment(QtCore.Qt.AlignCenter) # выравнивание текста по центру
        vh.setVisible(True)
        # высота строк - как у основного виджета
        self.frozenTableView.verticalHeader().setDefaultSectionSize(vh.defaultSectionSize())

        # Альтернативная устновка высоты строк
#        nrows = tm.rowCount(self)
#        for row in xrange(nrows):
#            self.setRowHeight(row, 25)

        # показываем наш дополнительный виджет
        self.frozenTableView.show()
        # устанавливаем ему размеры как у основного
        self.updateFrozenTableGeometry()

        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        # Создаем соединения
        tm.dataChanged.connect(self.test)
        # connect the headers and scrollbars of both tableviews together
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

    def test(self, index):
        print index.row(), index.column()

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex==0 or logicalIndex==1:
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        QtGui.QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() > 1:
            QtGui.QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                         self.frameWidth(), self.columnWidth(0) + self.columnWidth(1),
                         self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                         self.frameWidth(), self.columnWidth(0) + self.columnWidth(1),
                         self.viewport().height() + self.horizontalHeader().height())

    # переопределяем функцию moveCursor, для корректного скрола влево с клавиатуры
    def moveCursor(self, cursorAction, modifiers):
        current = QtGui.QTableView.moveCursor(self, cursorAction, modifiers)
        if cursorAction == self.MoveLeft and current.column() > 1 and self.visualRect(current).topLeft().x() < (self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)):
            newValue = self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() - (self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1))
            self.horizontalScrollBar().setValue(newValue)
        return current


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent = None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.colLabels = ['Col1', 'Col2', 'Col3', 'Col4', 'Col5', 'Col6',
                          'Col7', 'Col8', 'Col9', 'Col10'] # Заголовки столбцов
        self.dataCached = [
                        [111,'cell12','cell13','cell14','cell15','cell12','cell13','cell14','cell15','cell16'],
                        [112,'cell22','cell23','cell24','cell25','cell26','cell27','cell28','cell29','cell30'],
                        [113,'cell32','cell33','cell34','cell35','cell36','cell37','cell38','cell39','cell40'],
                        [114,'cell42','cell43','cell44','cell45','cell46','cell47','cell48','cell49','cell50'],
                        [115,'cell52','cell53','cell54','cell55','cell56','cell57','cell58','cell59','cell60'],
                        [116,'cell62','cell63','cell64','cell65','cell66','cell67','cell68','cell69','cell70'],
                        [117,'cell72','cell73','cell74','cell75','cell76','cell77','cell78','cell79','cell80'],
                        [118,'cell82','cell83','cell84','cell85','cell86','cell87','cell88','cell89','cell90'],
                        [119,'cell12','cell13','cell14','cell15','cell12','cell13','cell14','cell15','cell16'],
                        [120,'cell22','cell23','cell24','cell25','cell26','cell27','cell28','cell29','cell30'],
                        [121,'cell32','cell33','cell34','cell35','cell36','cell37','cell38','cell39','cell40'],
                        [122,'cell42','cell43','cell44','cell45','cell46','cell47','cell48','cell49','cell50'],
                        [123,'cell52','cell53','cell54','cell55','cell56','cell57','cell58','cell59','cell60'],
                        [124,'cell62','cell63','cell64','cell65','cell66','cell67','cell68','cell69','cell70'],
                        [125,'cell72','cell73','cell74','cell75','cell76','cell77','cell78','cell79','cell80'],
                        [126,'cell82','cell83','cell84','cell85','cell86','cell87','cell88','cell89','cell90'],
                        [127,'cell12','cell13','cell14','cell15','cell12','cell13','cell14','cell15','cell16'],
                        [128,'cell22','cell23','cell24','cell25','cell26','cell27','cell28','cell29','cell30'],
                        [129,'cell32','cell33','cell34','cell35','cell36','cell37','cell38','cell39','cell40'],
                        [130,'cell42','cell43','cell44','cell45','cell46','cell47','cell48','cell49','cell50'],
                        [131,'cell52','cell53','cell54','cell55','cell56','cell57','cell58','cell59','cell60'],
                        [132,'cell62','cell63','cell64','cell65','cell66','cell67','cell68','cell69','cell70'],
                        [133,'cell72','cell73','cell74','cell75','cell76','cell77','cell78','cell79','cell80'],
                        [134,'cell82','cell83','cell84','cell85','cell86','cell87','cell88','cell89','cell90'],
                        [135,'cell82','cell83','cell84','cell85','cell86','cell87','cell88','cell89','cell90'],
                        [136,'cell82','cell83','cell84','cell85','cell86','cell87','cell88','cell89','cell90']
                    ] # Область данных

    # Возвращает количество строк
    def rowCount(self, parent):
        return len(self.dataCached)

    # Возвращает количество столбцов
    def columnCount(self, parent):
        return len(self.colLabels)

    # Возвращает значение ячейки
    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.dataCached[i][j]

    # Значение и свойства ячейки данных в зависимости от роли
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        value = self.get_value(index)
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return QtCore.QVariant(value)
        elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.QVariant(QtCore.Qt.AlignCenter)
        return QtCore.QVariant()

    # Изменение значения ячейки
    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            self.dataCached[index.row()][index.column()] = QtCore.QVariant(value)
            self.emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        else:
            return False

    # Заголовки столбцов и строк
    def headerData(self, section, orientation, role):
        #заголовки столбцов
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            header = QtCore.QVariant(self.colLabels[section])
            return header
        #заголовки строк
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant("%s" % str(section + 1))

        return QtCore.QVariant()

    # Переопределяем метод flags (включаем выделение и редактирование в ячейках)
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        elif index.column() > 1:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

#!/usr/bin/python                                                              
# -*- coding: utf-8 -*-                                                        

import os, os.path, sys, datetime, time, operator, copy, string, stat, csv, smtplib, re
from xlwt import Workbook
from xlrd import open_workbook
from subprocess import call
from shutil import copy as copy_to
from PyQt4 import QtCore, QtGui
from database_info import Ui_Form
#Форма полнотекстового поиска
from search import Ui_Form as SearchUiForm
from add_form3 import Ui_Dialog as AddUiForm
from select_database import Ui_sel_database as SelectDbForm
from connect_database import Ui_selectDB as ConnectDbForm
#Форма сложного поиска 
from search_form import Ui_searchallForm as SearchAllForm
#тут мы импортировали форму для дублей. 
#теперь вместо нее будем использовать другую форму - dupl_settings для настроек поиска дублей
#и dupl_delete для обработки найденного. 
#from tree_form import Tree_Dialog 

#диалоги для настройки поиска дублей и для удаления дублей. 
from dupl_settings import Ui_duplSettingsDialog as duplSettingsDialog
from dupl_delete import Ui_duplDeleteDialog as duplDeleteDialog


from export_dialog import ExportDialog
from import_form import ImportDialog
from query_list import QueryListForm
from cStringIO import StringIO

log_message = StringIO()
#sys.stdout =  log_message #open("logs/log%s.txt"%datetime.datetime.now(), "a")
#sys.stderr = sys.stdout
#
from bibl_gui import Ui_MainWindow, dbname, user, host, passwd, port

to = 'gontchar@gmail.com'
msg = msg="""Subject: Ошибка!                                                        
Была обнаружена ошибка. Подробности ниже..."""

print QtCore.PYQT_VERSION_STR                                          
print QtCore.PYQT_VERSION
print datetime.datetime.now()

table_dict ={u'Авторы':['authors', 'name'], u"Название (ориг.)":['name_orig', 'name'], u"Источник":['src', 'source_'], u"Редактор":['editor','editor'], u"Место издания":['publ_location','location'], u"Издательство":['publ', 'publisher']}

import psycopg2, pg, psycopg2.extras
from psycopg2.extensions import adapt

#fts: порядок - A:name_orig; B:name_alt; C:abstract; D:full_txt;
#fts_keywords: порядок - A:common_keywords; B:taxon_keywords;

#Словарь с колонками таблицы
#убрано "любое поле" т.к. для этого есть полнотекстовый поиск
columns = {"authors":u"Авторы", "name_orig":u"Название (ориг.)", "name_alt":u"Название (альт.)", "source":u"Источник", "editor":u"Редактор", "publ_location":u"Место издания", "publication":u"Издательство", "year":u"Год", "volume":u"Том", "number":u"Номер", "issue":u"Выпуск", "series":u"Серия", "part":u"Часть", "pages":u"Страницы", "tables":u"Таблицы", "maps":u"Карты", "illustrations":u"Иллюстрации", "refs":u"Ссылки", "series_area":u"Область серии", "language":u"Язык", "type":u"Тип публикации", "ref_code":u"Реф. код", "udk":u"УДК", "zool_rec":u"Zool. Rec.", "issn":u"ISSN", "isbn":u"ISBN", "common_keywords":u"Ключевые слова", #"taxon_keywords":u"Таксономические ключевые слова", 
"publ_number":u"Номер публикации", "publ_date":u"Дата публикации", "publ_country":u"Страна публикации", "num_ed_mpk":u"Номер изд. МПК", "main_mpk_ind":u"Основной инд. МПК", "pat_owner":u"Владелец патента", "file_path":u"Файл", "file_size":u"Размер файла", "abstract":u"Реферат", "full_txt":u"Полный текст", "uid":u"УИН", "fulltxt_presence":u"PDF", "date_add":u"Дата добавления", "date_mod":u"Дата изменения"}

dupl_columns = {"authors":u"Авторы", "name_orig":u"Название (ориг.)", "name_alt":u"Название (альт.)", "source":u"Источник", "editor":u"Редактор", "publ_location":u"Место издания", "publication":u"Издательство", "year":u"Год", "volume":u"Том", "number":u"Номер", "issue":u"Выпуск", "series":u"Серия", "part":u"Часть", "pages":u"Страницы", "tables":u"Таблицы", "maps":u"Карты", "illustrations":u"Иллюстрации", "refs":u"Ссылки", "series_area":u"Область серии", "language":u"Язык", "type":u"Тип публикации", "ref_code":u"Реф. код", "udk":u"УДК", "zool_rec":u"Zool. Rec.", "issn":u"ISSN", "isbn":u"ISBN", "common_keywords":u"Ключевые слова","publ_number":u"Номер публикации", "publ_date":u"Дата публикации", "publ_country":u"Страна публикации", "num_ed_mpk":u"Номер изд. МПК", "main_mpk_ind":u"Основной инд. МПК", "pat_owner":u"Владелец патента","file_path":u"Файл", "file_size":u"Размер файла"}


bibl_card_head = u"""
БИБЛИОГРАФИЧЕСКИЕ КАРТОЧКИ
Результат запроса от %s
Отобрано %s записей

"""
bibl_card_entry = u"""
%s.
%s: %s
%s: %s
%s: %s
%s: %s
%s: %s
%s: %s
%s: %s
%s: %s
%s: %s
"""

bibl_list_head = u"""
БИБЛИОГРАФИЧЕСКИЙ СПИСОК
Результаты запроса от %s
Отобрано %s записей

"""
bibl_list_entry = u"""
%s. %s. %s. %s. %s.
"""

columns_to_add = [
u"Авторы",
u"Название (ориг.)",
u"Название (альт.)",
u"Источник",
u"Редактор",
u"Место издания",
u"Издательство",
u"Год",
u"Том",
u"Номер",
u"Выпуск",
u"Серия",
u"Часть",
u"Страницы",
u"Таблицы",
u"Карты",
u"Иллюстрации",
u"Ссылки",
u"Область серии",
u"Язык",
u"Дата добавления",
u"Дата изменения",
u"Тип публикации",
u"Реф. код",
u"УДК",
u"Zool. Rec.",
u"ISSN",
u"ISBN",
u"Ключевые слова",
#u"Таксономические ключевые слова",
u"Номер публикации",
u"Дата публикации",
u"Страна публикации",
u"Номер изд. МПК",
u"Основной инд. МПК",
u"Владелец патента",
u"Реферат",
u'Полный текст']

column_types = {
'text':[
[u"Авторы", u"Название (ориг.)", u"Название (альт.)", u"Источник", u"Редактор", u"Место издания", u"Издательство", u"Ключевые слова", u"Реферат", u"Полный текст"],
[u'содержит', u'не содержит', u'=', u'начинается с', u'заканчивается на']
],
'char':[
[u"Год", u"Том", u"Номер", u"Выпуск", u"Серия", u"Часть", u"Страницы", u"Таблицы", u"Карты", u"Иллюстрации", u"Ссылки", u"Область серии", u"Язык", u"Тип публикации", u"Реф. код", u"УДК", u"Zool. Rec.", u"ISSN", u"ISBN", u"Номер публикации", u"Дата публикации", u"Страна публикации", u"Номер изд. МПК", u"Основной инд. МПК", u"Владелец патента", u"Файл", u"Размер файла", u"Дата добавления", u"Дата изменения"],
[u'=', u'≠', u'содержит', u'не содержит', u'начинается с', u'заканчивается на']
],
'int':[[u"Год", u"Том", u"Номер", u"Выпуск", u"Серия", u"Часть", u"Страницы", u"Таблицы", u"Карты", u"Иллюстрации", u"Ссылки", u"Область серии",],
[u'=', u'≠', u'>', u'<', u'≥', u'≤', u'содержит', u'не содержит', u'начинается с', u'заканчивается на']
],
'tsvect':[
[u"Полный текст", u"Ключевые слова", ],
[u'подобен']],
'bool':[
[u"PDF"],
[]]
}


#столбцы для краткого вида
short_view="file_path, authors, year, name_orig, source, type, uid"
#столбцы для полного вида

#taxon_keywords убрали
long_view="file_path, authors, year, name_orig, name_alt, type, source, editor, publ_location, publication, volume, number, issue, series, part, pages, tables, maps, illustrations, refs, series_area, language, ref_code, udk, zool_rec, issn, isbn, common_keywords, publ_number, publ_date, publ_country, num_ed_mpk, main_mpk_ind, pat_owner, file_size, date_add, date_mod, uid"

#пример запроса для пункта "Словари" - выбор по значениям.
dict_query = """
SELECT "%s", count(*) AS "count" FROM articles GROUP BY "%s" ORDER BY "%s"
"""

#Размер базы данных
size_query_long = """
SELECT relname AS name, relfilenode AS oid, (relpages * 8192 / (1024*1024))::int as size_mb, reltuples  as count 
      FROM pg_class 
      WHERE relname NOT LIKE 'pg%' 
      ORDER BY relpages DESC
"""

size_query_short = """
select pg_size_pretty(pg_database_size('bibliography'))
"""

table_size_query = """
select pg_size_pretty(pg_relation_size('articles'))
"""

fts_query = """SELECT 
uid, authors, year, name_orig, name_alt, file_path,
 source,type, common_keywords, abstract, main_mpk_ind,
 volume, number, pages, publ_location, publication, language, publ_date,  
ts_headline(full_txt, to_tsquery('russian', '%s'), 'MaxWords=60, MinWords=30, ShortWord=3'),
 rank
from (SELECT uid, authors, year, name_orig, name_alt, file_path, source, type, full_txt, common_keywords, abstract, main_mpk_ind, volume, number, pages, publ_location, publication, language, publ_date, ts_rank_cd(fts, query) AS rank
FROM articles, to_tsquery('%s') query
WHERE query @@@ fts
ORDER BY rank DESC) as FOO
"""

#Тут столбцы в порядке их появления в форме добавления новых данных
edit_query = """
select
 authors,
 name_orig,
 name_alt,
 year,
 source,
 publication,
 publ_location,
 editor,
 volume,
 number,
 issue,
 series,
 part,
 pages,
 tables,
 maps,
 illustrations,
 "refs",
 zool_rec,
 "series_area",
 language,
 publ_country,
 type,
 num_ed_mpk,
 main_mpk_ind,
 pat_owner,
 publ_number,
 publ_date,
 ref_code,
 udk,
 issn,
 isbn,
 file_path,
 common_keywords,
 taxon_keywords,
 abstract
from 
 articles
where
 uid = %s
"""

abstract_query = """
SELECT
abstract
FROM
articles
WHERE
uid = %i
"""
coincidence_query = """
select ts_headline(full_txt, plainto_tsquery('%s'), 'MaxWords=20, MinWords=1, MaxFragments=100, FragmentDelimiter="<p>" ') from articles where
uid = %i
"""

fts_query_short = """SELECT
%s, ts_rank_cd(fts, query), %s 
FROM articles, to_tsquery('%s') query
WHERE fts @@@ query {0}
ORDER BY year DESC
"""#.format('')

fts_kw_query = u"""SELECT
%s, ts_rank_cd(fts_keywords, query), %s
FROM articles, to_tsquery('%s') query
WHERE fts_keywords @@@ query {0}
ORDER BY year DESC
"""

#Выбор 
query_standart  = """SELECT
%s
FROM articles 
ORDER BY authors 
ASC
"""

query_short = """SELECT
file_path, authors, year, name_orig, source, volume, type, uid
FROM articles
WHERE uid = '%s'
ORDER BY authors
ASC
"""

#После DESC можно писать LIMIT 10 OFFSET %i

#Логические операторы
log_oper = {u'И':'AND', u'ИЛИ':'OR', u'И НЕ':'AND NOT', u'ИЛИ НЕ':'OR NOT'}

sel_oper = {u'содержит':"ILIKE '%%%s%%'", u'не содержит':"NOT ILIKE '%%%s%%'", u'=':"= '%s'", u'≠':"!= '%s'", u'>':"> '%s'", u'<':r"< '%s'", u'≥':">= '%s'", u'≤':r"""<= '%s'""", u'начинается с':"ILIKE '%s%%'", u'заканчивается на': "ILIKE '%%%s'", u'подобен':'fts @@@ query %s'}

#Список запросов
class QueryList(QtGui.QWidget, QueryListForm):
    def __init__(self, cur):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.model = ListModel(self, [])
        self.listView.setModel(self.model)
        self.cur = cur
        self.connect(self.buttonBox, QtCore.SIGNAL("clicked(QAbstractButton *)"), self.model.clear)
        self.connect(self.listView, QtCore.SIGNAL("clicked(QModelIndex)"), self.settext)
        self.connect(self.deleteLineButton, QtCore.SIGNAL("clicked()"), self.deleteLine)
        
    def settext(self, index):
        #for i in  xrange(len(self.model.words[index.row()])):
            #print i, self.model.words[index.row()][i]

        query = self.model.words[index.row()][1][0]
        self.textBrowser.setText(query)

    def deleteLine(self):
        ind = self.listView.currentIndex().row()
        #print ind
        try:
            self.model.words.pop(ind)
        except IndexError:
            pass
        self.listView.reset()

class duplSettings(QtGui.QWidget, duplSettingsDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

class duplDelete(QtGui.QWidget, duplDeleteDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

class Print_Dialog(QtGui.QWidget, ExportDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.label.setText(QtGui.QApplication.translate("Dialog", "Вывести на печать:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Формат данных:", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.clear()
        self.typeComboBox.addItem(u"Список")
        self.typeComboBox.addItem(u"Карточки")
        #Удаление ненужных виджетов
        self.sep_comboBox.setVisible(False)
        self.label_2.setVisible(False)
                

class Export_Form(QtGui.QWidget, ExportDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

class Import_Form(QtGui.QWidget, ImportDialog):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)


#Класс справочного окна
class About_Form(QtGui.QWidget, Ui_Form):

    def __init__(self):
        #super(SubWindow, self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("About_Form")
        #тут дописать инфо о размере БД, кол-ве таблиц, строк, столбцов, название, дата последнего редактирования
        self.setWindowTitle(QtGui.QApplication.translate("AboutForm", "О программе", None, QtGui.QApplication.UnicodeUTF8))
    def about_show(self):
        self.setWindowTitle(QtGui.QApplication.translate("AboutForm", "О базе данных", None, QtGui.QApplication.UnicodeUTF8))
        self.show()


#Класс окна настраиваемого поиска
class SearchAll_Form(QtGui.QWidget, SearchAllForm):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(640, 220)
        self.setObjectName("SearchAll_Form")
        #Списки кнопок в строках.
        self.buttons_line0 = [self.and_comboBox1, self.field_comboBox1, self.cont_comboBox1, self.search_lineEdit1, self.rem_button1, self.add_button1]
        self.buttons_line1 = [self.and_comboBox2, self.field_comboBox2, self.cont_comboBox2, self.search_lineEdit2, self.rem_button2, self.add_button2]
            
        #Список строк 
        self.button_list = [self.buttons_line0, self.buttons_line1]
        self.add_button_last = 5
        self.rm_button_last = 4
    
        for combo in self.button_list:
            self.connect(combo[1], QtCore.SIGNAL('currentIndexChanged(QString)'), self.changeFields)

        self.connect(self.add_button0, QtCore.SIGNAL('clicked()'), self.add_search)
        self.connect(self.add_button1, QtCore.SIGNAL('clicked()'), self.add_search)
        self.connect(self.add_button2, QtCore.SIGNAL('clicked()'), self.add_search)
        self.connect(self.field_comboBox0, QtCore.SIGNAL('currentIndexChanged(QString)'), self.changeFields)
        self.connect(self.rem_button1, QtCore.SIGNAL('clicked()'), self.rem_search)
        self.connect(self.rem_button2, QtCore.SIGNAL('clicked()'), self.rem_search)

    def changeFields(self, strng):
        #print self.gridLayout.rowCount()
        #print self.gridLayout.columnCount()
        pos = self.gridLayout_2.getItemPosition(self.gridLayout_2.indexOf(self.focusWidget()))
        row, col = pos[:2]
        combobox = self.gridLayout_2.itemAtPosition(row, col+1).widget()
        for value in column_types.values():
            
            if unicode(strng) in value[0]:
                combobox.clear()
                combobox.addItems(value[1])
                
    def searchall_show(self):
        self.show()
    
    def add_search(self):
        """
        Функция добавляет строку поиска в форму
        """
        self.buttons_line = []
        self.add_button_last = self.add_button_last + 1
               
        #Добавляем combo box с выбором и|или|не
        self.and_comboBox = QtGui.QComboBox(self.groupFields)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(25)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.and_comboBox.sizePolicy().hasHeightForWidth())
        self.and_comboBox.setSizePolicy(sizePolicy)
        self.and_comboBox.setMaximumSize(QtCore.QSize(40,16777215))
        self.and_comboBox.setObjectName("and_comboBox")
        for i in ['И', 'ИЛИ', 'НЕ']:
            self.and_comboBox.addItem(QtGui.QApplication.translate("searchallForm", i, None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2.addWidget(self.and_comboBox, self.add_button_last - 1, 0, 1, 1)
        self.buttons_line.append(self.and_comboBox)
        
        #Добавляем combo box с выбором поля
        self.field_comboBox = QtGui.QComboBox(self.groupFields)
        self.field_comboBox.setObjectName("field_comboBox")
        
        #Подправить... чтобы было отсортировано 
        for i in columns_to_add:
            self.field_comboBox.addItem(i)
        self.field_comboBox.setCurrentIndex(0)
        self.gridLayout_2.addWidget(self.field_comboBox, self.add_button_last - 1, 1, 1, 1)
        self.buttons_line.append(self.field_comboBox)
        
        #Добавляем combo box с выбором содержания
        self.cont_comboBox = QtGui.QComboBox(self.groupFields)
        self.cont_comboBox.setObjectName("cont_comboBox")
        for i in [u'содержит', u'не содержит', u'=', u'≠', u'>', u'<', u'≥', u'≤', u'начинается с', u'заканчивается на', u'подобен']:
            self.cont_comboBox.addItem(QtGui.QApplication.translate("searchallForm", i, None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2.addWidget(self.cont_comboBox, self.add_button_last - 1, 2, 1, 1)
        self.buttons_line.append(self.cont_comboBox)

        #Добавляем line edit
        self.search_lineEdit3 = QtGui.QLineEdit(self.groupFields)
        self.search_lineEdit3.setObjectName("search_lineEdit")
        self.gridLayout_2.addWidget(self.search_lineEdit3, self.add_button_last - 1, 3, 1, 1)
        self.buttons_line.append(self.search_lineEdit3)

        #Добавляем кнопку удаления
        self.rem_button = QtGui.QPushButton(self.groupFields)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(25)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rem_button1.sizePolicy().hasHeightForWidth())
        self.rem_button.setSizePolicy(sizePolicy)
        self.rem_button.setMaximumSize(QtCore.QSize(30,16777215))
        self.rem_button.setObjectName("rem_button")
        self.rem_button.setText(QtGui.QApplication.translate("searchallForm", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2.addWidget(self.rem_button, self.add_button_last - 1, 4, 1, 1)
        self.buttons_line.append(self.rem_button)
        self.connect(self.rem_button, QtCore.SIGNAL('clicked()'), self.rem_search)
        

        #Добавляем кнопку добавления
        self.add_button = QtGui.QPushButton(self.groupFields)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(25)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_button1.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        self.add_button.setMaximumSize(QtCore.QSize(30,16777215))
        self.add_button.setObjectName("add_button")
        self.add_button.setText(QtGui.QApplication.translate("searchallForm", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout_2.addWidget(self.add_button, self.add_button_last - 1, 5, 1, 1)
        self.buttons_line.append(self.add_button)
        
        #добавляем список с кнопками с список списков кнопок О_о
        self.button_list.append(self.buttons_line)
        self.connect(self.field_comboBox, QtCore.SIGNAL('currentIndexChanged(QString)'), self.changeFields)
        self.connect(self.add_button, QtCore.SIGNAL('clicked()'), self.add_search)
           
    #def closeEvent(self, event):
    #    self.deleteLater()
    #    event.accept()


    def rem_search(self):
                
        for i in self.button_list[-1]:
            self.gridLayout_2.removeWidget(i)
            i.setParent(None)
            del(i)
        self.button_list.pop()
        self.adjustSize()


#Класс окна поиска по ключевым словам
class Search_Keywords_Form(QtGui.QWidget, SearchUiForm):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setObjectName("Search_Keywords_Form")
        self.label.setText(u'<html><body><center>Поиск по ключевым словам</center></body></html>')
        self.setWindowTitle(QtGui.QApplication.translate("SearchUiForm", "Поиск по ключевым словам", None, QtGui.QApplication.UnicodeUTF8))
        #Добавляем chechbox'ы
        self.checkBox_comm = QtGui.QCheckBox(self)
        self.checkBox_comm.setObjectName("checkBox_comm")
        self.checkBox_comm.setText(QtGui.QApplication.translate("searchKwForm", "Общие ключевые слова", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_comm.setCheckState(QtCore.Qt.CheckState(2))
        self.gridLayout.addWidget(self.checkBox_comm, 4, 0, 1, 1)
        
        #Пока не нужны
        #self.checkBox_taxon = QtGui.QCheckBox(self)
        #self.checkBox_taxon.setObjectName("checkBox_taxon")
        #self.checkBox_taxon.setText(QtGui.QApplication.translate("searchKwForm", "Таксономические ключевые слова", None, QtGui.QApplication.UnicodeUTF8))
        #self.gridLayout.addWidget(self.checkBox_taxon, 5, 0, 1, 1)
        #self.checkBox_taxon.setEnabled(False)

        self.checkBox_search_results = QtGui.QCheckBox(self)
        self.checkBox_search_results.setObjectName("checkBox_search_results")
        self.checkBox_search_results.setText(QtGui.QApplication.translate("searchKwForm", "Искать в найденном", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.checkBox_search_results, 2, 0, 1, 1)

        self.search_in_selected = QtGui.QCheckBox(self)
        self.search_in_selected.setObjectName("search_in_selected")
        self.search_in_selected.setText(QtGui.QApplication.translate("searchKwForm", "Искать в выделенном", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.search_in_selected, 3, 0, 1, 1)

    def search_show(self):
        self.show()

    def fulltext_search(self):
        text = self.lineEdit.text
        return text

#    def closeEvent(self, event):
#         self.deleteLater()
#         event.accept()


#Класс окна поиска
class Search_Form(QtGui.QWidget, SearchUiForm):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setObjectName("Search_Form")
        self.setWindowTitle(QtGui.QApplication.translate("SearchUiForm", "Полнотекстовый поиск на %s" % host, None, QtGui.QApplication.UnicodeUTF8))
        #Чекбоксы для настройки полнотекстового поиска
        
        #Для поиска в найденном
        self.checkBox_search_results = QtGui.QCheckBox(self)
        self.search_in_selected = QtGui.QCheckBox(self)
        self.search_in_selected.setObjectName("search_in_selected")
        self.search_in_selected.setText(u'Искать в выделенном')
        self.checkBox_search_results.setObjectName("checkBox_search_results")
        self.checkBox_search_results.setText(u'Искать в найденном')
        self.gridLayout.addWidget(self.checkBox_search_results, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.search_in_selected, 3, 0, 1, 1)
        #Для оригинального названия
        self.label.setText(u'<html><body><center>Полнотекстовый поиск</center></body></html>')
        
        #Ограничение ввода в поля!!!
        #self.validator = QtGui.QIntValidator(10,100, self)
        #self.lineEdit.setValidator(self.validator)
        self.lineEdit.setText(u'[строка поиска]')
        self.checkBox_name_orig = QtGui.QCheckBox(self)
        self.checkBox_name_orig.setObjectName("checkBox_name_orig")
        self.checkBox_name_orig.setText(u'Название')
        self.checkBox_name_orig.setCheckState(QtCore.Qt.CheckState(2))
        self.gridLayout.addWidget(self.checkBox_name_orig, 4, 0, 1, 1)
        
        #Для альтернативного названия
        #self.checkBox_name_alt = QtGui.QCheckBox(self)
        #self.checkBox_name_alt.setObjectName("checkBox_name_alt")
        #self.checkBox_name_alt.setText(u'Альтернативное название')
        #self.checkBox_name_alt.setCheckState(QtCore.Qt.CheckState(2))
        #self.gridLayout.addWidget(self.checkBox_name_alt, 5, 0, 1, 1)

        #Для абстракта
        self.checkBox_abst = QtGui.QCheckBox(self)
        self.checkBox_abst.setObjectName("checkBox_abst")
        self.checkBox_abst.setText(u'Реферат')
        self.checkBox_abst.setCheckState(QtCore.Qt.CheckState(2))
        self.gridLayout.addWidget(self.checkBox_abst, 6, 0, 1, 1)
        
        #Для полного текста
        self.checkBox_full_txt = QtGui.QCheckBox(self)
        self.checkBox_full_txt.setObjectName("checkBox_full_txt")
        self.checkBox_full_txt.setText(u'Полные тексты')
        self.checkBox_full_txt.setCheckState(QtCore.Qt.CheckState(2))
        self.gridLayout.addWidget(self.checkBox_full_txt, 7, 0, 1, 1)


    def search_show(self):
        self.show()

    
    def fulltext_search(self):
        text = self.lineEdit.text
        return text


    #def closeEvent(self, event):
    #    self.deleteLater()
    #    event.accept()


#Класс окна соединения с базой
class Connect_Form(QtGui.QWidget, ConnectDbForm):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.lineEditName.setText(dbname)
        self.lineEditUser.setText(user)
        self.lineEditAddress.setText(host)
        self.lineEditPasswd.setText(passwd)
    
        #self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.connect_to)
        #self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.close)
        #self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.close)

        #    def closeEvent(self, event):
        #        self.deleteLater()
        #        event.accept()


    def form_show(self):
        self.show()
        print "connecting"

    def connect_to(self):
        dbname = self.lineEditName.text()
        user = self.lineEditUser.text()
        host = self.lineEditAddress.text()
        passwd = self.lineEditPasswd.text()
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%d  password='%s'" % (dbname, user, host, port, passwd))
        print "connection ready"
        return conn

#Класс добавления новой записи
class Add_Form(QtGui.QScrollArea, AddUiForm):

    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
    
    def add_show(self):
        self.show()

    #def closeEvent(self, event):
    #    self.deleteLater()
    #    event.accept()


#Класс выбора базы данных
class Select_Database(QtGui.QWidget, SelectDbForm):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setObjectName("Select_Database")
    def select_show(self):
        self.show()
        
    #def closeEvent(self, event):
    #    self.deleteLater()
    #    event.accept()

#Класс для ItemDelegate в TableView для открытия/добавления pdf

class PdfDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.parent = parent
        
        #переопределить paint() и рисовать 2
        #разные картинки в качестве фона
        #в зависимости от того, есть ли публикация или нет.

        #переопределить setEditorData, setModelData и updateEditorGeometry
        #для изменения поведения. 

    

    def paint(self, painter, option, index):
     
        value = index.model().data(index, QtCore.Qt.EditRole).toString()
        image = QtGui.QPixmap()

        if os.name == 'nt':
            if os.path.isfile(os.getcwd().decode('cp1251') + os.sep + unicode(value)):
                img = '/page_white_acrobat.png'
                #print os.getcwd().decode('cp1251') + os.sep + value
            else:
                img = '/add.png'
                #print os.getcwd().decode('cp1251') + os.sep + value
        else:
            if os.path.isfile(os.getcwd() + os.sep + unicode(value)):
                img = '/page_white_acrobat.png'
            else:
                img = '/add.png'
        
        #if value.length() > 0:
        #    image.load(os.curdir + '/page_white_acrobat.png')
        #else:
        image.load(os.curdir + img)
        
        Option = QtGui.QStyleOptionButton()
        Option.state = QtGui.QStyle.State_Enabled
        Option.direction = QtGui.QApplication.layoutDirection();
        Option.rect = option.rect;
        Option.fontMetrics = QtGui.QApplication.fontMetrics();
        Option.text = 'Button'
        
        QtGui.QApplication.style().drawItemPixmap(painter, option.rect, QtCore.Qt.AlignCenter, image);



#Это пока оставлем так, потом допишем сюда и редактор для ячеек - 
#с выбором между открытием или добавлением пдф
#    def createEditor(self, parent, option, index):
#        editor = QtGui.QPushButton(parent)
#        return editor
#
#    def setEditorData(self, editor, index):
#        value = index.model().data(index, QtCore.Qt.EditRole).toString()
#        editor.setText(value)
#
#    def setModelData(self, editor, model, index):
#        value = editor.text()
#        model.setData(index, value, QtCore.Qt.EditRole)
#
#    def updateEditorGeometry(self, editor, option, index):
#        editor.setGeometry(option.rect)


class DuplThread(QtCore.QThread):
    def __init__(self, conn,  ind, item, processed, *args, **kwargs):
        QtCore.QThread.__init__(self)
        #Тут создаем новый курсор, чтобы можно было выполнять параллельные запросы к базе
        self.cur = conn.cursor()
        self.item = item
        self.args = args
        self.kwargs = kwargs
        
        self.ind = ind
        self.pr = 'TRUE'
        if processed.toUtf8() == 'Необработанные':
            self.pr = 'FALSE'
            
        #elif processed.toUtf8() == 'Обработанные':
        #    self.pr = 'TRUE'
            

        self.query_part = "where processed = %s" % self.pr
        
        if processed.toUtf8() == 'Все':
            self.query_part = " "
        
        #self.processed = [True if ]
        #теперь мы выбираем из разных таблиц
        self.query = """select distinct %s, similarity(%s, '%s') from %s where %s %% '%s' and %s != '%s' order by similarity(%s, '%s') desc limit 5"""
        #self.q2="""select distinct source, similarity(source, %s) from dupl_table where source %% %s and  source != %s  order by similarity(source, %s) desc limit 5"""
        
    def __del__(self):
        self.wait()


    def run(self):
        start_time = datetime.datetime.now()
        a=[]
        b=[]
        pb_value=0

        self.cur.execute("select distinct %s from %s %s order by %s asc" % (self.item[1], self.item[0], self.query_part, self.item[1]))
        
        if self.cur.rowcount > 0:
            for i in self.cur.fetchall():
                a.append(i[0])
            
            pb_value = len(a)
        
            self.emit(QtCore.SIGNAL('pbMax'), pb_value)
            for i in a:
                pb_value-=1
                self.emit(QtCore.SIGNAL('pbData'),pb_value)
                if i is not None and len(i) > 0:

                    c=[]

                    print "execute dupl query", self.query % (self.item[1], self.item[1], pg.escape_string(i), self.item[0], self.item[1], pg.escape_string(i), self.item[1], pg.escape_string(i), self.item[1], pg.escape_string(i) )
                    self.cur.execute(self.query % (self.item[1], self.item[1], pg.escape_string(i), self.item[0], self.item[1], pg.escape_string(i), self.item[1], pg.escape_string(i), self.item[1], pg.escape_string(i) ))
                #self.cur.execute(self.q2, (pg.escape_string(i), pg.escape_string(i), pg.escape_string(i), pg.escape_string(i)))
                    if self.cur.rowcount > 1:
                    
                    #print len(a)
                    
                    
                        c.append(i.decode('utf-8'))
                    #print i
                        d=[]
                        for j in self.cur.fetchall():
                        
                            
                            if j[1] >= self.ind:
                            #j[2] - year!!!
                                d.append(u"%s, %f" %( j[0].decode('utf-8'), j[1]))
                                c.append(d)
                        
                        #else:
                            #c.append([' '])
                        #    try:
                        #    if i.decode('utf-8') in c:
                        #    c.pop(c.index(i.decode('utf-8')))
                        #    except:
                        #        pass
                        #print j[0], j[1]
                        if len(c) > 1:
                        
                            b.append(c)
                    #print b[-1]
                        try:
                            a.pop(a.index(i))
                        except:
                            pass
            
            
        #for i in b:
        #    if len(i) < 2:
        #        b.pop(b.index(i))
                
            differ = str(datetime.datetime.now() - start_time)
            differ = differ.split(':')[-1]
            differ = float(differ)
            self.emit(QtCore.SIGNAL('dataFetched'), b)#, differ, len(data_list))
        else:
            #self.emit(QtCore.SIGNAL('pbMax'), 100)
            #self.emit(QtCore.SIGNAL('pbData'),0)
            self.emit(QtCore.SIGNAL('dataFetched'), None)#, differ, len(data_list))

class RenameThread(QtCore.QThread):
    def __init__(self, conn, query, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.conn = conn
        self.cur = self.conn.cursor()
        self.args = args
        self.kwargs = kwargs
        self.query = query
        
    def __del__(self):
       self.wait()
        
    def run(self):
        self.cur.execute(self.query)
        
class HotkeyThread(QtCore.QThread):
    def __init__(self, *args, **kwargs):
        QtCore.QThread.__init__(self)

    def __del__(self):
       self.wait()

    def run(self):
        if os.name == 'nt':
            import win32clipboard as w
            import win32con
            import time
            import sys, ctypes
            from ctypes import wintypes

            byref = ctypes.byref
            user32 = ctypes.windll.user32

            HOTKEYS = {1 : (win32con.VK_F3, win32con.MOD_WIN),}

            def handler():
                w.OpenClipboard()
                text = w.GetClipboardData(win32con.CF_TEXT)
                #print text.decode("cp1251")
                self.emit(QtCore.SIGNAL('textFetched'), unicode(text.decode("cp1251")))
                self.emit(QtCore.SIGNAL('activateWindow'), True)
                w.CloseClipboard()

            HOTKEY_ACTIONS = {1 : handler,}

            for id, (vk, modifiers) in HOTKEYS.items ():
                if not user32.RegisterHotKey (None, id, modifiers, vk):
                    print "Unable to register id", id


            #Петля-обработчик нажатий на горячие клавиши. Ее надо в отдельный поток, чтобы не мешала работать главному окну.
            try:
                msg = wintypes.MSG ()
                while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
                        if action_to_take:
                            action_to_take ()
                user32.TranslateMessage (byref (msg))
                user32.DispatchMessageA (byref (msg))
            finally:
                for id in HOTKEYS.keys ():
                    user32.UnregisterHotKey (None, id)
        else:
            print "Temporary unavailable on %s, sorry..." % os.name


class SearchThread(QtCore.QThread):
    def __init__(self, cursor, query, search_words, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.cur = cursor
        self.args = args
        self.message = (kwargs['message'] if 'message' in kwargs.keys() else None)
        self.kwargs = kwargs
        self.query = query
        self.search_words = search_words
        self.noapp = ("NoAPP" if "NoAPP" in args else None)
        self.prev_query = ''
        if len(args) > 0:
            self.prev_query = args[0]

    def __del__(self):
        self.wait()
    
    def run(self):
        start_time = datetime.datetime.now()
        #print self.query
        self.cur.execute(self.query)
        data = self.cur.fetchall()
        num_res = self.cur.rowcount
        differ = str(datetime.datetime.now() - start_time)
        differ = differ.split(':')[-1]
        differ = float(differ)
        data_list = []
        for i in data:
            data_list.append(list(i))

        #print "thread", self.search_words
        self.emit(QtCore.SIGNAL('dataFetched'), data_list, differ, num_res, self.query, self.prev_query, self.search_words, ("NoAPP" if self.noapp is not None else False), (self.message if self.message is not None else 2))
        self.emit(QtCore.SIGNAL("statusBar"), u"Данные загружены")



#Класс основного окна
class MainView(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.connect_server()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.words = []
        self.insert_query = 'INSERT INTO articles '
        self.update_query = u'UPDATE articles set '
        self.view="short"
        #это для контроля при добавлении новых данных/исправлении
        self.uid = None
        self.index = None
        self.query_queue = []
        self.query_object = []
        
        self.printDialog = Print_Dialog()
        self.printDialog.comboBox.addItem(QtGui.QApplication.translate("exportForm", u'Результаты поиска', None, QtGui.QApplication.UnicodeUTF8))
        
        #Пока не активные пункты меню
        #Вид->Результаты поиска
        self.ui.action_9.setEnabled(False)
        #Форматированные ссылки
        self.ui.action_10.setEnabled(False)
        self.ui.copy.setEnabled(False)
        self.ui.crop.setEnabled(False)
        self.ui.insert.setEnabled(False)
        self.ui.select_all.setEnabled(False)
        self.ui.undo_all.setEnabled(False)
        self.ui.preferences.setEnabled(False)
        
        #Undo/Redo:
        self.undoStack = QtGui.QUndoStack(self)

        self.uiAbout = About_Form()
        self.uiSearch = Search_Form()
        self.uiSearchKw = Search_Keywords_Form()
        self.uiSearchAll = SearchAll_Form()
        self.uiConnect = Connect_Form()
        self.uiAdd = Add_Form(self)
        self.uiSelectDb = Select_Database()

        #Для дублей
        #Тут надо заменить Tree_Form на то, что мы используем сейчас для обработки дублей
        self.uiDuplSettings = duplSettings()
        self.uiDuplDelete = duplDelete()
        
        #Форма экспорта таблиц
        self.exportForm = Export_Form()
        self.importForm = Import_Form()
        #форма списка запросов
        self.queryForm = QueryList(self.cur)
        
        self.cur.execute("select tablename from pg_tables where schemaname = 'public' order by tablename asc")
        
        #Добавляем имена таблиц в формы импорта и экспорта.
        self.exportForm.comboBox.addItem(QtGui.QApplication.translate("exportForm", u'Результаты поиска', None, QtGui.QApplication.UnicodeUTF8))
        for i in self.cur.fetchall():
            self.exportForm.comboBox.addItem(QtGui.QApplication.translate("exportForm", i[0], None, QtGui.QApplication.UnicodeUTF8))
            self.importForm.tableComboBox.addItem(QtGui.QApplication.translate("importForm", i[0], None, QtGui.QApplication.UnicodeUTF8))
            
        #for i in columns.values():
        #    self.importForm.colNameComboBox.addItem(QtGui.QApplication.translate("exportForm", i, None, QtGui.QApplication.UnicodeUTF8))
        #Добавляем имена колонок в формы
        self.get_column_names()


        #Регистрация горячих клавиш

        self.connect(self.exportForm.buttonBox, QtCore.SIGNAL("accepted()"), self.write_to)
        self.connect(self.exportForm.buttonBox, QtCore.SIGNAL("rejected()"), self.exportForm.close)


        #Показ списка запросов
        self.connect(self.ui.query_list, QtCore.SIGNAL("triggered()"), self.queryForm.show)
        
        self.connect(self.queryForm.listView, QtCore.SIGNAL("doubleClicked(QModelIndex)"), self.redo_query)
        self.connect(self.ui.print_, QtCore.SIGNAL("triggered()"), self.showPrintDialog)

        #Выполнение предыдущего и следующего запросов
        self.connect(self.ui.undo_query, QtCore.SIGNAL("triggered()"), self.nextQuery)
        self.connect(self.ui.redo_query, QtCore.SIGNAL("triggered()"), self.prevQuery)
        self.connect(self.queryForm.nextQuery, QtCore.SIGNAL("clicked()"), self.nextQuery)
        self.connect(self.queryForm.prevQuery, QtCore.SIGNAL("clicked()"), self.prevQuery)
        self.connect(self.queryForm.execQueries, QtCore.SIGNAL("clicked()"), self.execQueries)
        #Тест для поиска в выделенном - вывод выделенных индексов,
        #self.connect(self.ui.redo_query, QtCore.SIGNAL("triggered()"), self.searchInSelected)
        #сохранение результатов поиска
        #self.connect(self.ui.save_result)

        #Добавляем действия отмены и повтора в форму поиска дублей
        #self.uiDupl.addAction(self.ui.undo)
        #self.uiDupl.addAction(self.ui.redo)
        #self.obj = unicode(self.uiDupl.comboBox.currentText())
        #self.q_obj = columns.keys()[columns.values().index(self.obj)]

        #self.treeModel = TreeModel([], self.undoStack, self.conn, self.uiDupl.treeView, self.q_obj, self)
        
        #Удаление строки в TreeView
        #self.connect(self.uiDupl.rmButton, QtCore.SIGNAL("clicked()"), self.delRow)
        
        #self.connect(self.uiDupl.treeView, QtCore.SIGNAL("expanded(QModelIndex)"), self.setProcessed)
        #self.connect(self.uiDupl.treeView, QtCore.SIGNAL("collapsed(QModelIndex)"), self.setUnprocessed)

        #Добавление строки в TreeView
        #self.connect(self.uiDupl.addButton, QtCore.SIGNAL("clicked()"), self.addRow)

        #Добавление ветви в TreeView
        #self.connect(self.uiDupl.addBranchButton, QtCore.SIGNAL("clicked()"), self.add_Branch)
        
        #Изменение главной записи в TreeView
        #self.connect(self.uiDupl.mainEntryButton, QtCore.SIGNAL("clicked()"), self.setMainEntry)

        #Обозначение дубля в TreeView
        #self.connect(self.uiDupl.duplEntryButton, QtCore.SIGNAL("clicked()"), self.setDuplicate)
        
        self.connect(self.ui.dumpall, QtCore.SIGNAL("triggered()"), self.saveDump)

        #Удаление синонимов из списка
        #self.connect(self.uiDupl.createListButton, QtCore.SIGNAL("clicked()"), self.renameDuplicates)

        #Удаление дубля из базы
        #self.connect(self.uiDupl.delDuplButton, QtCore.SIGNAL("clicked()"), self.deleteDuplicate)
        
        #font = QtGui.QFont('Tahoma', 10)
        #self.uiDupl.treeView.setFont(font)
        
        #print QtCore.PYQT_VERSION_STR
        #print QtCore.PYQT_VERSION
        #for i in xrange(10):
        #    for k in xrange(10):
        #        print i,k
        #        print treeModel.data(treeModel.index(i,k)).toString().toUtf8()



        #print dir(self.uiDupl)
        #Вот он, заголовок таблицы! И его надо менять в эависимости от выбранного вида - краткий, полный, итд...
        #1. Это - стандартный вид.
        self.header=[]
        self.columns=short_view.split(", ")
        for i in self.columns:
            self.header.append(columns[i])

        self.ui.tableWidget.hide()
        self.ui.add_dataDOCK.hide()

        #Тут мы создаем первый наш поток
        self.uiTable = self.createTable('0')
        
        self.searchThread = SearchThread(self.cur, query_standart % short_view, u'')
        self.searchThread.start()
        self.connect(self.searchThread, QtCore.SIGNAL('dataFetched'), self.start_query)
        self.connect(self.searchThread, QtCore.SIGNAL('statusBar'), self.statusBar().showMessage)
        
        if os.name == 'nt':
            self.hotkeyThread = HotkeyThread()
            self.hotkeyThread.start()
            self.connect(self.hotkeyThread, QtCore.SIGNAL('textFetched'), self.fts_search)
            self.connect(self.hotkeyThread, QtCore.SIGNAL('activateWindow'), self.activateWindow)

        else:
            self.connect(self.ui.toolBarPrev, QtCore.SIGNAL("triggered()"),self.clipboard_search)

        #Выбор вида таблицы - пока краткий и полный.
        #Соединяется с ф-ей, вытаскивающей из базы данные для стандартного вида

        #Возврат ко всем полям базы, к первоначальному виду.
        self.connect(self.ui.action_home, QtCore.SIGNAL("triggered()"), self.full_view)
        self.connect(self.ui.toolBarHome, QtCore.SIGNAL("triggered()"), self.full_view)
        self.connect(self.ui.action_7, QtCore.SIGNAL("triggered()"), self.exec_query_short)
        self.connect(self.ui.action_8, QtCore.SIGNAL("triggered()"), self.exec_query_long)
 
        #Для добавления произвольных хоткеев!!! и да, оно работает!
        #self.action = QtGui.QAction(QtGui.QIcon(), "test", self)
        #self.action.setShortcut("Ctrl+Alt+Z")
        #self.addAction(self.action)

        #Отменить/повторить
        self.connect(self.ui.undo, QtCore.SIGNAL("triggered()"), self.undoStack.undo)
        self.connect(self.ui.toolBarUndo, QtCore.SIGNAL("triggered()"), self.undoStack.undo)
        self.connect(self.ui.redo, QtCore.SIGNAL("triggered()"), self.undoStack.redo)
        
        
        #Удаление записи
        self.connect(self.ui.del_, QtCore.SIGNAL("triggered()"), self.delete_entry)
        self.connect(self.ui.toolBarDeleteEntry, QtCore.SIGNAL("triggered()"), self.delete_entry)
        
        #Пока данные загружаются...
        self.statusBar().showMessage(u'Загрузка данных...')

        #Сохранение данных
        self.connect(self.ui.save, QtCore.SIGNAL("triggered()"), self.conn.commit)
        self.connect(self.ui.toolBarCommit, QtCore.SIGNAL("triggered()"), self.conn.commit)
        self.connect(self.ui.toolBarReset, QtCore.SIGNAL("triggered()"), self.conn.rollback)

        #закрытие главного окна
        self.connect(self.ui.exit_, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        #вывод информации о программе
        self.connect(self.ui.database_info, QtCore.SIGNAL('triggered()'), self.about_db)
        
        #вывод информации о базе данных
        self.connect(self.ui.about, QtCore.SIGNAL('triggered()'), self.db_info)
        
        #Форма для подключения к базе данных
        self.connect(self.ui.toolBarOpenDatabase, QtCore.SIGNAL('triggered()'), self.uiConnect.form_show)
        self.connect(self.uiConnect.buttonBox, QtCore.SIGNAL("accepted()"), self.uiConnect.connect_to)
        self.connect(self.uiConnect.buttonBox, QtCore.SIGNAL("accepted()"), self.uiConnect.close)
        self.connect(self.uiConnect.buttonBox, QtCore.SIGNAL("rejected()"), self.uiConnect.close)
        #self.connect(self.uiConnect.buttonBox, QtCore.SIGNAL("accepted()"), self.fts_model)
        
        #открытие файла (для добавления PDF)
        self.connect(self.ui.pushButton_file_path, QtCore.SIGNAL('clicked()'), self.add_file)

        #Полнотекстовый поиск, сложный поиск, поиск по ключевым словам - показ формы
        self.connect(self.ui.searchFulltext, QtCore.SIGNAL('triggered()'), self.uiSearch.search_show)
        self.connect(self.ui.searchCompl, QtCore.SIGNAL('triggered()'), self.uiSearchAll.searchall_show)
        self.connect(self.ui.searchKw,  QtCore.SIGNAL('triggered()'), self.uiSearchKw.search_show)
                
        self.connect(self.ui.searchDupl, QtCore.SIGNAL('triggered()'), self.uiDuplSettings.show)
        self.connect(self.uiDuplSettings.buttonBox, QtCore.SIGNAL('accepted()'), self.uiDuplDelete.show)
        #self.connect(self.uiDupl.buttonBox, QtCore.SIGNAL('accepted()'), self.duplSelect)
        #self.connect(self.uiDupl.buttonBox, QtCore.SIGNAL('rejected()'), self.uiDupl.close)
        #self.connect(self.uiDupl.,  QtCore.SIGNAL('clicked(QDialogButtonBox.ApplyRole)'), self.test)
        
        #Добавление новой записи - показ формы
        self.connect(self.ui.toolBarNewEntry, QtCore.SIGNAL('triggered()'), self.add_dataDOCK_show)

        #Выбор базы данных
        #self.connect(self.ui.toolBarOpenDatabase, QtCore.SIGNAL('triggered()'), self.uiSelectDb.select_show)
        
        #Поиск по ключевым словам, настраиваемый поиск
        self.connect(self.uiSearchAll.OKbuttonBox, QtCore.SIGNAL("accepted()"), self.compl_search)

        #"Полнотекстовый поиск" 
        self.connect(self.uiSearch.pushButton, QtCore.SIGNAL('clicked()'), self.uiSearch.fulltext_search)
        self.connect(self.uiSearch.pushButton, QtCore.SIGNAL('clicked()'), self.fts_search)
        self.connect(self.uiSearch.lineEdit, QtCore.SIGNAL('returnPressed()'), self.fts_search)
        
        #ключевые слова
        self.connect(self.uiSearchKw.pushButton,  QtCore.SIGNAL('clicked()'), self.kw_search)
        self.connect(self.uiSearchKw.lineEdit, QtCore.SIGNAL('returnPressed()'), self.kw_search)

        #Правка выбранной записи
        self.connect(self.ui.toolBarEditEntry, QtCore.SIGNAL('triggered()'), self.edit_entry)

        #Добавление новой записи
        self.connect(self.ui.buttonBox_add_entry, QtCore.SIGNAL("accepted()"), self.add_entry)


        #Импорт и экспорт
        self.connect(self.ui.write_from, QtCore.SIGNAL("triggered()"), self.importForm.show)
        self.connect(self.ui.write_in, QtCore.SIGNAL("triggered()"), self.exportForm.show)
        self.connect(self.importForm.pushButton, QtCore.SIGNAL("clicked()"), self.read_from)
        self.connect(self.importForm.fileLineEdit, QtCore.SIGNAL("textChanged(const QString&)"), self.read_file)
        self.connect(self.importForm.sepGroup, QtCore.SIGNAL("buttonClicked(QAbstractButton *)"), self.read_file)
        self.connect(self.importForm.tableComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.get_column_names)
        self.connect(self.importForm.colNameComboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.set_import_header)
        self.connect(self.importForm.lineSpinBox, QtCore.SIGNAL("valueChanged (int)"), self.read_file)
        self.connect(self.importForm.buttonBox, QtCore.SIGNAL("accepted()"), self.import_data)

        #Поиск из буфера
        #self.connect(self.ui.toolBarPrev, QtCore.SIGNAL("triggered()"),self.clipboard_search)

        #Объединение автора и редактора в форме добавления
        self.connect(self.ui.lineEdit_authors.lineEdit, QtCore.SIGNAL("textChanged(const QString&)"), self.ui.lineEdit_editors.lineEdit.setText)
        #Объединение даты и года публикации
        #В таком виде не работает, надобно конвертировать текст (год) в дату и так менять
        #self.connect(self.ui.lineEdit_year, QtCore.SIGNAL("textChanged(const QString&)"), self.ui.lineEdit_publ_date.setDate)
        

        
        #Сообщение об ошибке
        self.connect(self.ui.report_error, QtCore.SIGNAL("triggered()"), self.report_error)
        
        #Вывод диалога печати
        self.connect(self.printDialog.buttonBox, QtCore.SIGNAL("accepted()"), self.printDocument)

    def showPrintDialog(self):
        print "printing"
        self.printDialog.show()

    def printDocument(self):
        print "printing..."
        SEL = re.compile(r"SELECT")
        FR = re.compile(r"FROM")
        table_name = unicode(self.printDialog.comboBox.currentText())
        params = unicode(self.printDialog.typeComboBox.currentText())
        if params == u'Карточки':
            params = ' authors, name_orig, year, language, type, publ_number, file_path, file_size, abstract '
        else:
            params = ' authors, name_orig, year, publ_number '
        last_query = self.queryForm.model.words[-1][1][0]
        WHAT = last_query[SEL.search(last_query).end():FR.search(last_query).start()]
        last_query = last_query.replace(WHAT, params)
        #print last_query
        #Заменить в last_query список отбираемых столбцов на params
        #query = u"CREATE TEMPORARY TABLE results AS (%s) " % last_query
        #self.cur.execute(query)
        #Потом почти все то же самое, что и в write_to, 
        #но результат передавать в document
        if table_name == u'Результаты поиска':
            table_name = 'results'

        #query = u"CREATE TEMPORARY TABLE results AS (%s) " % last_query
        cols = []
        for i in params.split(', '):
            cols.append(columns[i.strip()])
            
        self.cur.execute(last_query)
        today = datetime.datetime.now()
        today = "%s.%s.%s" % (today.day, today.month, today.year)

        if len(cols) == 4:
            #Если выбран список
            document = bibl_list_head % (today, self.cur.rowcount)
            for i in xrange(self.cur.rowcount):
                res = self.cur.fetchone()
                document = document + bibl_list_entry % (i+1, res[0].decode("utf-8"), res[1].decode("utf-8"), res[2].decode("utf-8"), res[3].decode("utf-8"))
        else:
            #Если выбраны карточки
            document = bibl_card_head % (today, self.cur.rowcount)
            for i in xrange(self.cur.rowcount):
                res = self.cur.fetchone()
                document = document + bibl_card_entry % (i+1, cols[0], res[0].decode("utf-8"), cols[1], res[1].decode("utf-8"), cols[2], res[2].decode("utf-8"), cols[3], res[3].decode("utf-8"), cols[4], res[4].decode("utf-8"), cols[5], res[5].decode("utf-8"), cols[6], res[6].decode("utf-8"), cols[7], res[7].decode("utf-8"), cols[8], res[8].decode("utf-8"), )
            

        printer = QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        doc = QtGui.QTextDocument(document)
        
        if dialog.exec_() == True:
            doc.print_(printer)

    #Предварительная обработка запроса 
    def process_query(self, str, params):
        
        str_temp = str.split(" ")
        str_corr = []
        for i in str_temp:
            if len(i) > 0:
                #Знаки, которые надо удалять
                st = re.sub('[&! |/-:].', '', i)
                str_corr.append(st+':' + "".join(params))

        str = " & ".join(str_corr)
        #print str
        return str

    def search_results(self, cursor, query, first=0, last=-1, indexes = []):
        print 'Searching within results...'
        #Поиск в найденном
        #1. SELECT + 
        #2. (в зависимости от ф-ии: fts, compl, kw) columns
        #3. FROM articles
        #4. (объединение в зависимости от ф-ии) to_tsquery(обработанная строка поиска0) query0, plainto_tsquery(обработанная строка поиска1) query1, итд
        #5. WHERE объединенные (AND) из всех запросов (включая текущий) условия поиска.
        #6. ORDER BY year DESC
        #+сделать проверку на совпадение поисковых слов в текущем запросе и в предыдущих
        #+проверять возможность того, что в compl_search НЕ БУДЕТ полнотекстового поиска и наш
        #regexp будет возвращать Null, вызывая ошибку
        #Что-то не так со сложным поиском. При поискев найденном оно зачем-то
        #вставляет articles несколько раз...
        #обработка текущего запроса
        SEL = re.compile(r"SELECT")
        FR = re.compile(r"FROM")
        WHR = re.compile(r"WHERE")
        ORD = re.compile(r"ORDER")
        num = 0
        NUM = re.compile(' query[_\d]?')
        SELECT = """SELECT """
        WHAT = query[SEL.search(query).end():FR.search(query).start()]
        if 'query' in WHAT:
            WHAT = WHAT.replace(WHAT[NUM.search(WHAT).start():NUM.search(WHAT).end()], " query_%s"%num)
        FROM = ["FROM articles"]
        temp_fr = query[FR.search(query).end():WHR.search(query).start()].replace("articles, ", '')
        if 'query' in temp_fr:
            temp_fr = temp_fr.replace(temp_fr[NUM.search(temp_fr).start():NUM.search(temp_fr).end()], " query_%s"%num)
        FROM.append(temp_fr)
        WHERE = []
        where_tmp = query[WHR.search(query).end():ORD.search(query).start()]
        if 'query' in where_tmp:
            where_tmp = where_tmp.replace(where_tmp[NUM.search(where_tmp).start():NUM.search(where_tmp).end()], " query_%s"%num)
        WHERE.append(where_tmp)
        ORDER = "ORDER BY year DESC"
        #обработка предыдущих запросов из истории поиска
        if len(indexes) == 0:
            queries = self.queryForm.listView.model().words#[first:last] 
            print 'queries', len(queries)
            for q in queries:
                print q[1][0]
        else:
            queries = [self.queryForm.listView.model().words[x] for x in indexes]
           
        for i in queries:
            num = num+1
            prev_query = i[1][0]
            temp_from = prev_query[FR.search(prev_query).end():WHR.search(prev_query).start()].replace("articles, ", '')
            if 'query' in temp_from:
                temp_from = temp_from.replace(temp_from[NUM.search(temp_from).start():NUM.search(temp_from).end()], " query_%s"%num)
            FROM.append(temp_from)
            temp_where = prev_query[WHR.search(prev_query).end():ORD.search(prev_query).start()]
            if 'query' in temp_where:
                temp_where = temp_where.replace(temp_where[NUM.search(temp_where).start():NUM.search(temp_where).end()], " query_%s"%num)
            WHERE.append(temp_where)
            #print "prev_query", prev_query

        res_query = SELECT + WHAT + ", ".join(FROM) + " WHERE " + " AND ".join(WHERE)[1:] + ORDER
        res_query = re.sub(",\s+articles\s", '', res_query)
        #print "current query", res_query, "end"
        return res_query

    def redo_query(self, index, quer=None, fun=None, mes=None, s_words=None):
        if quer is None:
            query = self.queryForm.model.words[index.row()][1][0]
        else:
            query = quer
        if fun is None:
            func = self.queryForm.model.words[index.row()][1][1]
        else:
            func = fun
        if mes is None:
            mess = self.queryForm.model.words[index.row()][0]
        else:
            mess = mes
        if s_words is None:
            search_words = self.queryForm.model.words[index.row()][1][2]
        else:
            search_words = s_words
   

        if func == 'fts':
            self.uiSearch.lineEdit.setText(" ".join(mess.split(" ")[4:]))
            self.ftssearchThread = SearchThread(self.cur, query, '', 'NoAPP', message=mess)
            self.ftssearchThread.start()
            self.connect(self.ftssearchThread, QtCore.SIGNAL('dataFetched'), self.fts_model)
            
        elif func == 'compl':
            self.complsearchThread = SearchThread(self.cur, query, '', 'NoAPP', message=mess)
            #print '1'
            self.complsearchThread.start()
            #print '2'
            self.connect(self.complsearchThread, QtCore.SIGNAL('dataFetched'), self.compl_model)
            #print '3'
        elif func == 'kw':
            self.kwsearchThread = SearchThread(self.cur, query, '', 'NoAPP', message=mess)
            self.kwsearchThread.start()
            self.connect(self.kwsearchThread, QtCore.SIGNAL('dataFetched'), self.kw_model)
            
        self.append_query(mess, query, func, '', search_words)
        
    def report_error(self):
        serv = smtplib.SMTP("smtp.gmail.com",587)
        user = "pybliography@gmail.com"
        passwd = 'andreygon'
        
       # msg1 = log.read()
        #print msg1#+ " ".join(log.readlines())
        serv.ehlo()
        serv.starttls()
        serv.ehlo
        serv.login(user, passwd)
        serv.sendmail(user, to, msg + "\n\n" +log_message.getvalue())
        serv.close()
       

    def import_data(self):
        #print self.importForm.tableView.model().dbdata[0]
        #print self.importForm.tableView.model().header
        #self.uiTable.model()
        """
        Внесение данных, указанных в форме, в базу и таблицу.
        """

        table_name = unicode(self.importForm.tableComboBox.currentText())
        header = []

        for col in self.importForm.tableView.model().header:
            col = unicode(col)
            if col in columns.values():
                out=columns.keys()[columns.values().index(unicode(col))]
            else:
                out = col
            header.append(out)

        filename = unicode(self.importForm.fileLineEdit.text())
        print "importing selected file %s" % filename
        QtGui.QMessageBox.warning(self, u"Импорт данных", u"""Добавленные данные будут отображены после перезапуска программы.""")
        command = ImportDataCommand(self.importForm.tableView.model(), self.importForm.tableView, header, self.cur, table_name, filename, "Import to database")
        self.undoStack.push(command)


    def set_import_header(self):
        view = self.importForm.tableView
        if view.model() is not None:
            header = view.model().header
            value = self.importForm.colNameComboBox.currentText()
            index = view.currentIndex()
            column = index.column()
            header[column] = value
            view.model().setHeaderData(column, QtCore.Qt.Vertical, QtCore.QVariant(value))
            view.model().reset()

    def read_from(self):
        print "setting import filename"
        #self.importForm.show()
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        filename=unicode(dialog.getOpenFileName())
        self.importForm.fileLineEdit.setText(QtCore.QString(filename))
        
     
    def get_column_names(self):
        tablename = self.importForm.tableComboBox.currentText()
        self.cur.execute("""select column_name from information_schema.columns where table_name = '%s'""" % tablename)
        self.importForm.colNameComboBox.clear()
        for i in xrange(self.cur.rowcount):
            col_name = self.cur.fetchone()[0]
            self.importForm.colNameComboBox.addItem(QtGui.QApplication.translate("importForm", (col_name if col_name not in columns.keys() else columns[col_name]), None, QtGui.QApplication.UnicodeUTF8))

    def read_file(self):
        """
        Импорт из файла, указанного в форме импорта. Все параметры берутся оттуда же.
        """

        #при изменении значения с какой строки импортируем - расставленные заголовки
        #стираются. Надо сделать так, чтобы они оставались. 
        filename = self.importForm.fileLineEdit.text()
        from_line = self.importForm.lineSpinBox.value()
        if not filename.isEmpty():
            sep=";"
        
            if self.importForm.tabCheckBox.isChecked():
                sep = "\t"
            elif self.importForm.commaCheckBox.isChecked():
                sep = ","
            elif self.importForm.semicolCheckBox.isChecked():
                sep = ";"
            elif self.importForm.spaceCheckBox.isChecked():
                sep = " "
            elif self.importForm.otherCheckBox.isChecked():
                sep = str(self.importForm.otherLineEdit.text())
        
            #print sep
            if filename.endsWith('csv'):    
                print "import csv"
                if os.name == 'nt':
                    filename = unicode(filename).encode('cp1251')
                else:
                    filename = unicode(filename).encode('utf-8')

                file = open(filename, 'r')

                reader = csv.reader(file, delimiter=sep, quotechar = str(self.importForm.comboBox.currentText()))
                data = []
                for row in reader:
                    data.append(row)
            elif filename.endsWith('xls'):
                print 'import xls'
                if os.name == 'nt':
                    filename = unicode(filename).encode('cp1251')
                else:
                    filename = unicode(filename).encode('utf-8')

                book = open_workbook(filename)
                sheet = book.sheets()[0]
                data = []
                for row in xrange(sheet.nrows):
                    #print sheet.row_values(row)
                    temp_data = []
                    corr_data=''
                    for i in sheet.row_values(row):
                        if isinstance(i, str):
                            corr_data = i.encode("utf-8")
                        elif isinstance(i, int):
                            corr_data = i
                        elif isinstance(i, unicode):
                            corr_data = i.encode("utf-8")
                        elif isinstance(i, float):
                            corr_data = i
                            
                        
                        temp_data.append(corr_data)
                        
                    data.append(temp_data)
                    
            header = []
            for i in data[0]:
                header.append('')
            #print "aaa"
            
            model = BiblTableModel(data[from_line:], header, self.undoStack, self.conn, self.statusBar, columns, False, self)
            #Загрузка данных в окно предпросмотра
            self.importForm.tableView.setModel(model)

            

        #сделать добавление всего этого в таблицу!!!
        #сделать Thread
        #self.cur.execute("copy from %s" % filename)
            #file.close()

    def write_to(self):
        print "export"
        
        table_name = unicode(self.exportForm.comboBox.currentText())
        if table_name == u'Результаты поиска':
            table_name = 'results'
            self.cur.execute("DROP TABLE IF EXISTS results")
            query = u"CREATE TEMPORARY TABLE results AS (%s) " % self.queryForm.model.words[-1][1][0]

            self.cur.execute(query)


        sep = unicode(self.exportForm.sep_comboBox.currentText())
        ftype = unicode(self.exportForm.typeComboBox.currentText())
        if sep == '{tab}':
            sep = '\t'
        
                 
        #file = os.getcwd() + '/%s.sql'% table_name
        
        #open(file, 'w')
        #os.chmod(file, 0777)
            
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        if os.name == 'nt':
            tempfname = os.getcwd().decode('cp1251') + u'/%s%s' % (table_name,ftype)
            enc = 'cp1251'
        else:
            tempfname = os.getcwd() + u'/%s%s' % (table_name,ftype)
            enc = 'utf-8'
        filename=unicode(dialog.getSaveFileName(self, QtCore.QString(u'Сохранить как...'), QtCore.QString(tempfname)))
        
        export_file = open(filename, 'w')
        os.chmod(filename, 0766)
        if ftype == u'.csv':
            #Вот тут бы хорошо указывать кодировку, в которой мы будем писать
            #в файл, однако это сделать нельзя и приходится писать вкодировке базы, utf-8,
            #а эксель потом показывает крякозябры
            self.cur.copy_to(export_file, table_name, sep, null='')
        elif ftype == u'.xls':
            print 'xls'
            book = Workbook()
            sheet = book.add_sheet(u'Лист 1')
            self.cur.execute("""select * from %s""" % table_name)
            for row in xrange(self.cur.rowcount):
                data = self.cur.fetchone()
                for col in xrange(len(data)):
                    
                    if isinstance(data[col], str):
                        val = data[col].decode(enc)
                        sheet.write(row, col, val)
                    elif isinstance(data[col], int):
                        val = data[col]
                        sheet.write(row, col, val)
                    else:
                        sheet.row(row).set_cell_blank(col)
            
            book.save(filename)
        #execute("COPY %s TO '%s' WITH DELIMITER '%s' CSV" % (table_name, filename, sep))
        #Сделать Thread
        #self.cur.execute("copy to %s" % filename)

    def duplSelect(self):
        self.obj = unicode(self.uiDupl.comboBox.currentText())
        self.q_obj = columns.keys()[columns.values().index(self.obj)]
        item = table_dict[unicode(self.uiDupl.comboBox.currentText())]
        self.duplThread = DuplThread(self.conn, self.uiDupl.spin.value(), item, self.uiDupl.comboBoxProcessed.currentText())
        self.duplThread.start()
        self.uiDupl.pb.show()
        self.connect(self.duplThread, QtCore.SIGNAL('dataFetched'), self.ch_view_dupl)
        self.connect(self.duplThread, QtCore.SIGNAL('pbMax'), self.uiDupl.pb.setMaximum)
        self.connect(self.duplThread, QtCore.SIGNAL('pbData'), self.uiDupl.pb.setValue)
        self.uiDupl.setEnabled(False)
        
    def setUnprocessed(self, index):
        """
        Производит действие, обратное setProcessed. 
        При сворачивании отмечает выбранные записи как необработанные
        """
        item = table_dict[unicode(self.uiDupl.comboBox.currentText())]
        view=self.uiDupl.treeView
        model = view.model()
        parent = model.parent(index)
        
        self.cur.execute("update %s set processed = FALSE where %s = '%s'" % (item[0], item[1], pg.escape_string(index.internalPointer().data(1).encode('utf-8')))) 

    def setProcessed(self, index):
        """
        При разворачивании элемента списка автоматически меняет состояние на
        "обработанное". При сворачивании производит обратное действие.
        """
        item = table_dict[unicode(self.uiDupl.comboBox.currentText())]
        
        view=self.uiDupl.treeView
        model = view.model()
        parent = model.parent(index)
        #print model.obj
        #print index.internalPointer().data(1)
        #print index.internalPointer().data(1)
        #Сделать экранирование одиночных запятых и пр и пр.
        self.cur.execute("update %s set processed = TRUE where %s = '%s'" % (item[0], item[1], pg.escape_string(index.internalPointer().data(1).encode('utf-8'))))
        #for i in index.internalPointer().childItems:
        #    print i.data(1)
        

    def setMainEntry(self):
        """
        Меняет данные местами между родителем и потомком. 
        Для того, чтобы объявлять главной записью не то, что является родителем,
        а одного из потомков.
        """
        item = table_dict[unicode(self.uiDupl.comboBox.currentText())]
        view=self.uiDupl.treeView
        model = view.model()
        index = view.currentIndex()
        parent = model.parent(index)
        model.setMain(item, parent, index, view)
        
    def deleteDuplicate(self):
        view=self.uiDupl.treeView
        model = view.model()
        index = view.currentIndex()
        row = index.row()
        parent = model.parent(index)
        model.deleteDupl(index, row, 1, parent)
        
        
    def renameDuplicates(self):
        item = table_dict[unicode(self.uiDupl.comboBox.currentText())]
        view=self.uiDupl.treeView
        model = view.model()
        index = view.currentIndex()
        parent = model.parent(index)
        model.renameDupl(item, index)
        

    def delRow(self):
        item = table_dict[unicode(self.uiDupl.comboBox.currentText())]
        view=self.uiDupl.treeView
        model = view.model()
        index = view.currentIndex()
        row = index.row()
        parent = model.parent(index)
        model.removeRows(item, index, row, 1, parent)
        
    def add_Branch(self):
        view=self.uiDupl.treeView
        index = view.currentIndex()
        model = view.model()
        model.addBranch(index)
        

    def addRow(self):
        view=self.uiDupl.treeView
        model = view.model()
        index = view.currentIndex()
        row = index.row()
        item = index.internalPointer()
        parent = model.parent(index)
        model.insertRows(row, 1, parent)
        
    def ch_view_dupl(self, data_list):
        self.uiDupl.setEnabled(True)
        self.uiDupl.pb.hide()
        if data_list is not None:
            self.treeModel = TreeModel(data_list, self.undoStack, self.conn, self.uiDupl.treeView, self.q_obj, self)
            self.uiDupl.treeView.setModel(self.treeModel)
        
    #Запускает поток поиска для отображения стандартного вида
    def exec_query_short(self):
        if self.view != 'short':
            self.ui.abstractDock.setWindowTitle(u'Стандартный вид')
            self.view="short"
            #print len(self.columns)
            self.header=[]
            self.columns=short_view.split(", ")
            for i in self.columns:
                self.header.append(columns[i])
            self.uiTable.model().header=self.header
            self.searchThread = SearchThread(self.cur, query_standart % short_view, u'')
            self.searchThread.start()
            self.connect(self.searchThread, QtCore.SIGNAL('dataFetched'), self.change_view)
            self.connect(self.searchThread, QtCore.SIGNAL('statusBar'), self.statusBar().showMessage)

    #Запускает поток для отображения полного вида
    def exec_query_long(self):
        if self.view != 'long':
            self.view="long"
            #print len(self.columns)
            self.ui.abstractDock.setWindowTitle(u'Все поля')
            self.header=[]
            self.columns=long_view.split(", ")
        
            for i in self.columns:                                                
                self.header.append(columns[i])

            self.uiTable.model().header=self.header
            self.uiTable.model().columns = self.columns
            self.searchThread = SearchThread(self.cur, query_standart % long_view, '')
            self.searchThread.start()
            self.connect(self.searchThread, QtCore.SIGNAL('dataFetched'), self.change_view)
            self.connect(self.searchThread, QtCore.SIGNAL('statusBar'), self.statusBar().showMessage)


    def saveDump(self):
        """
        Сохраняет полный дамп базы данных
        в выбранном пользователем файле
        """
        print 'dumpall'
        dialog = QtGui.QFileDialog()
        #dialog.setAcceptMode(dialog.AcceptSave)
        dialog.setDefaultSuffix(QtCore.QString(".sql"))
        
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        print dialog.fileMode()
        filename=unicode(dialog.getSaveFileName())
        print filename

        #здесь надо будет сделать copy_to binary
        #вобщем, нормального решения нету...


    #*** TODO -Поиск в выделенном.
    #def searchInSelected(self):
        #print "Selected indexes", [x.row() for x in self.uiTable.selectedIndexes()]
        #Получаем список uid для выделенных строк
    #    "AND ({0})".format(", ".join(map(str, self.uiTable.model().getFromColumn(u'УИН', [x.row() for x in self.uiTable.selectedIndexes()]))))
        


    #для предыдущего и следующего запросов логика такая:
    #получаем текущий индекс в списке, если он не определен, 
    #то выполняем последний или предпоследний запрос и перемещаем индекс соответственно
    #вперед или назад.
    #если определен, то выполняем соответственно следующий или предыдущий запрос относительно 
    #индекса и переводим его на один вперед или назад.
    #*** TODO -Кнопки для выполнения предыдущего и следующего запросов из истории: bibl.py:line 1726 etc
    def prevQuery(self):
        self.prevOrNextQuery(1)
        print "prev"
    
    def nextQuery(self):
        self.prevOrNextQuery(-1)
        print "next"

    def execQueries(self):
        inds = [x for x in self.queryForm.listView.selectedIndexes()]
        if len(inds) > 1:
            rows = [x.row() for x in inds].sort()
            ind =  inds[0]
            first = self.queryForm.model.words[ind.row()]
            q = first[1][0]
            func = first[1][1]
            mess = first[0]
            words = first[1][-1]
            query = self.search_results(self.cur, q, indexes = [x.row() for x in inds[1:]])
            mess = u", ".join([self.queryForm.model.words[x.row()][0] for x in inds])
            words = u" ".join([self.queryForm.model.words[x.row()][1][-1] for x in inds]) + " " + words
            self.redo_query(ind, quer=query, fun=func, mes=mess, s_words=words)


    def prevOrNextQuery(self, direction):
        #Если листаем назад, то после выполнения пред. запроса надо сдвинуть индекс на 1 назад.
        #Если листаем вперед, то соответственно после выполнения запроса сдвигаем индекс на 1 вперед.
        #берем текущий индекс и в зависимости от направления выполняем +1 или -1 запрос
        if len(self.queryForm.model.words) > 0:
            ind = self.queryForm.listView.currentIndex()
            row = (0 if ind.row() == -1 else ind.row())
            sel = row + direction 
            if sel >= len(self.queryForm.model.words):
                sel = -1

            query = self.queryForm.model.words[sel][1][0]
            mess = self.queryForm.model.words[sel][0]
            words = self.queryForm.model.words[sel][1][-1]
            func = self.queryForm.model.words[sel][1][1]
            self.queryForm.setEnabled(False)
            self.redo_query(ind, quer=query, fun=func, mes=mess, s_words=words)
            print sel, "SELLLLLLLLLLLLLLLL"
            if sel == -1:
                next_ind = self.queryForm.listView.model().createIndex(0, 0)
            else:
                next_ind = self.queryForm.listView.model().createIndex(sel, 0)
            print "PASSEDDDDDDDDDDDDD"
            self.queryForm.listView.setCurrentIndex(next_ind)


    def about_db(self):
        self.cur.execute("SELECT CURRENT_DATABASE()")
        db_name = self.cur.fetchone()[0]
        
        self.cur.execute("select count(*) from articles")
        db_length = self.cur.fetchone()[0]

        self.cur.execute("SELECT pg_size_pretty(pg_database_size(CURRENT_DATABASE()))")
        db_size = self.cur.fetchone()[0]

        self.cur.execute("SELECT count(*) from articles")
        num_rows = self.cur.fetchone()[0]

        self.cur.execute("select count(*) from information_schema.columns where table_name='articles'")
        num_columns = self.cur.fetchone()[0]

        self.cur.execute("select count(*) from pg_tables where schemaname = 'public'")
        num_tables = self.cur.fetchone()[0]

        self.cur.execute("select max(date_mod) from articles")
        last_modif = self.cur.fetchone()[-1]
        
        print last_modif.date(), last_modif.time()
        
        if os.name == 'posix':
            hostname = os.environ['HOSTNAME']
        elif os.name == 'nt':
            hostname = os.environ['COMPUTERNAME']

        #print hostname
        #last_modified придется делать самому....
        
        self.uiAbout.textBrowser.setHtml(u"""База данных <b>%s</b> на %s, соединено с %s. <br> База содержит %s строк, %s колонок, %s таблиц (%s). Дата последнего редактирования - %s""" % (db_name, hostname, host, num_rows, num_columns, num_tables, db_size, last_modif.strftime("%d.%m.%y, %H:%M ")))
        self.uiAbout.show()

    #Для закрытия главного окна
    def closeEvent(self, event):
        widgetList = QtGui.QApplication.topLevelWidgets()
        numWindows = len(widgetList)
        form_list = ['About_Form','Search_Form', 'Search_Keywords_Form', 'SearchAll_Form', 'selectDB', 'Select_Database', 'DuplForm', 'ExportForm', 'ImportForm', 'QueryList']
        
        for i in widgetList:
            if str(i.objectName()) in form_list:
                i.close()
        
        if numWindows > 1:
            event.accept()
        else:
            event.accept()


    def add_file(self):
        #if os.name = 'nt':
            #искать xpdf в локальной папке xpdf,
        #elif os.name = posix:
        #   #вызывать системный xpdf
        dialog = QtGui.QFileDialog()
        
        filename=unicode(dialog.getOpenFileName())
        if filename.endswith("pdf") or filename.endswith("Pdf") or filename.endswith("PDF"):
            self.ui.lineEdit_file_path.setText('PDF/' + filename.split('/')[-1])
            output_directory = os.getcwd() + "/PDF/"
            in_file = filename.split(os.sep)[-1]
            out_file = os.path.splitext(unicode(in_file))[0] + '.txt'
            #И да, оно работает!!!
            if os.name == 'nt':
                #для NT посмотреть что сделать тут
                #print filename, output_directory, out_file.split('/')[-1]
                call(["modules/poppler/bin/pdftotext.exe", filename.encode("cp1251"), output_directory.encode("cp1251") + out_file.split('/')[-1].encode("cp1251")])
                copy_to(filename, output_directory)
            elif os.name == 'posix':
                call(['pdftotext', filename, output_directory + out_file])
                copy_to(filename, output_directory)

    def add_dataDOCK_show(self):
        self.ui.add_dataDOCK.setMinimumWidth(self.width()/2)
        self.ui.add_dataDOCK.setWindowTitle(u'Добавление записи')
        self.ui.lineEdit_authors.lineEdit.clear()
        self.ui.lineEdit_name_orig.clear()
        self.ui.lineEdit_name_alt.clear()
        self.ui.lineEdit_year.clear()
        self.ui.lineEdit_source.lineEdit.clear()
        self.ui.lineEdit_publisher.lineEdit.clear()
        self.ui.lineEdit_publ_place.lineEdit.clear()
        self.ui.lineEdit_editors.lineEdit.clear()
        self.ui.lineEdit_vol.clear()
        self.ui.lineEdit_number.clear()
        self.ui.lineEdit_issue.clear()
        self.ui.lineEdit_series.clear()
        self.ui.lineEdit_part.clear()
        self.ui.lineEdit_pages.clear()
        self.ui.lineEdit_tables.clear()
        self.ui.lineEdit_maps.clear()
        self.ui.lineEdit_ill.clear()
        self.ui.lineEdit_publ_numb.clear()
        self.ui.lineEdit_zool_rec.clear()
        self.ui.lineEdit_series_area.clear()
        self.ui.lineEdit_publ_lang.clear()
        self.ui.lineEdit_publ_country.lineEdit.clear()
        self.ui.lineEdit_publ_type.lineEdit.clear()
        self.ui.lineEdit_num_ed_mpk.clear()
        self.ui.lineEdit_main_ind_mpk.clear()
        self.ui.lineEdit_pat_owner.clear()
        self.ui.lineEdit_publ_number.clear()
        self.ui.dateEdit_publ_date.clear()
        self.ui.lineEdit_ref_code.clear()
        self.ui.lineEdit_udk.clear()
        self.ui.lineEdit_issn.clear()
        self.ui.lineEdit_isbn.clear()
        self.ui.lineEdit_file_path.clear()
        self.ui.lineEdit_comm_keywds.lineEdit.clear()
        self.ui.lineEdit_taxon_keywds.lineEdit.clear()
        self.ui.textEdit_abstract.clear()

        #установка значений по умолчанию.
        self.ui.lineEdit_publ_lang.setText(u'английский')
        self.ui.lineEdit_publ_type.lineEdit.setText(u'статья')

        self.ui.add_dataDOCK.show()
        
    def connect_server(self):
        #Тут: если соединение успешно создано, то ничего не делать, в противном случае 
        #выводить форму для ввода хоста, паролей и пр.
        #print ("dbname=%s user=%s host=%s  password=%s port=%d" % (dbname, user, host, passwd, port))
        self.conn = psycopg2.connect("dbname=%s user=%s host=%s  password=%s port=%d" % (dbname, user, host, passwd, port))
        self.cur = self.conn.cursor()
        self.dict_cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


    def createTable(self, datain):
        #Заголовок таблицы. Пока статичный
        header = self.header
        columns = self.columns
        #написать собственный класс таблицы
        tv = TableView()
        
        
        tm = BiblTableModel(datain, header, self.undoStack, self.conn, self.statusBar, columns, True, self)
        
        #for i in columns:
        #    print i
        self.mainSelectionModel = QtGui.QItemSelectionModel(tm)
        tv.setModel(tm)
        tv.setSelectionModel(self.mainSelectionModel)

        
        tv.setMinimumSize(800, 150)
        tv.hideColumn(6)
        tv.setColumnWidth(1, 300)
        tv.setColumnWidth(2, 60)
        tv.setColumnWidth(3, 300)
        tv.setColumnWidth(4, 300)
        
        delegate = PdfDelegate(tm)

        tv.setItemDelegateForColumn(0,delegate)
        
        vh = tv.verticalHeader()
        vh.setVisible(False)
        hh = tv.horizontalHeader()
        hh.setVisible(True)
        hh.setStretchLastSection(True)
        #Это регулирует режимы отображения горизонтального заголовка таблицы
        hh.setResizeMode(0)
        # set row height
        #nrows = tm.rowCount(self)
        #for row in xrange(nrows):
        #    tv.setRowHeight(row, 60)
        tv.setSortingEnabled(True)
        

        return tv


    #Удаление записи
    def delete_entry(self):
        command = DeleteRowCommand(self.uiTable.model(), self.uiTable, columns.keys(), self.dict_cur, "Deletion of a row")
        self.undoStack.push(command)

    #Редактирование записи 
    def edit_entry(self):
        index = self.uiTable.currentIndex()
        num = self.uiTable.model().header.index(u"УИН")
        
        uid = int(self.uiTable.model().dbdata[index.row()][num])
        self.cur.execute(edit_query % uid)
        res = list(self.cur.fetchall()[0])
        
        for i in xrange(len(res)):
            if res[i] is None:
                res[i] = ''

        #if res[0] is not None:
        self.ui.lineEdit_authors.lineEdit.setText(res[0].decode("utf-8"))

        self.ui.lineEdit_name_orig.setText(res[1].decode("utf-8"))
        #if res[2] is not None:
        self.ui.lineEdit_name_alt.setText(res[2].decode("utf-8"))
        self.ui.lineEdit_year.setText(str(res[3]))
        #if res[4] is not None:
        self.ui.lineEdit_source.lineEdit.setText(res[4].decode("utf-8"))
        self.ui.lineEdit_publisher.lineEdit.setText(res[5].decode("utf-8"))
        self.ui.lineEdit_publ_place.lineEdit.setText(res[6].decode("utf-8"))
        self.ui.lineEdit_editors.lineEdit.setText(res[7].decode("utf-8"))
        self.ui.lineEdit_vol.setText(res[8])
        self.ui.lineEdit_number.setText(res[9])
        self.ui.lineEdit_issue.setText(res[10])
        self.ui.lineEdit_series.setText(res[11])
        self.ui.lineEdit_part.setText(res[12])
        self.ui.lineEdit_pages.setText(res[13])
        self.ui.lineEdit_tables.setText(res[14])
        self.ui.lineEdit_maps.setText(res[15])
        self.ui.lineEdit_ill.setText(res[16])
        self.ui.lineEdit_publ_numb.setText(res[17])
        self.ui.lineEdit_zool_rec.setText(res[18])
        self.ui.lineEdit_series_area.setText(res[19])
        self.ui.lineEdit_publ_lang.setText(res[20].decode("utf-8"))
        self.ui.lineEdit_publ_country.lineEdit.setText(res[21].decode("utf-8"))
        self.ui.lineEdit_publ_type.lineEdit.setText(res[22].decode("utf-8"))
        self.ui.lineEdit_num_ed_mpk.setText(res[23].decode("utf-8"))
        self.ui.lineEdit_main_ind_mpk.setText(res[24].decode("utf-8"))
        self.ui.lineEdit_pat_owner.setText(res[25].decode("utf-8"))
        self.ui.lineEdit_publ_number.setText(res[26].decode("utf-8"))
        if res[27] != ".  .":
            self.ui.dateEdit_publ_date.setDate(QtCore.QDate.fromString(res[27], "dd.MM.YYYY"))
        self.ui.lineEdit_ref_code.setText(res[28].decode("utf-8"))
        self.ui.lineEdit_udk.setText(res[29].decode("utf-8"))
        self.ui.lineEdit_issn.setText(res[30].decode("utf-8"))
        self.ui.lineEdit_isbn.setText(res[31].decode("utf-8"))
        if res[32] is not None:
            self.ui.lineEdit_file_path.setText(res[32].decode("utf-8"))
        self.ui.lineEdit_comm_keywds.lineEdit.setText(res[33].decode("utf-8"))
        self.ui.lineEdit_taxon_keywds.lineEdit.setText(res[34].decode("utf-8"))
        self.ui.textEdit_abstract.setText(res[35].decode("utf-8"))
        
        self.ui.add_dataDOCK.setMinimumWidth(self.width()/2)

        self.uid = uid
        self.ui.add_dataDOCK.setWindowTitle(u'Правка записи %i' % self.uid)
        self.ui.add_dataDOCK.show()

#открывает пдф в программе для его просмотра или,
#если пдф'а нету, предлагает его загрузить
    def show_pdf(self):
        index = self.uiTable.currentIndex()
        col = self.uiTable.currentIndex().column()
        row = self.uiTable.currentIndex().row()
        num = self.uiTable.model().header.index(u"УИН")
        #print num
        uid = int(self.uiTable.model().dbdata[index.row()][num])
                
        #Если щелкнули по первому столбцу
        if col == 0:
            pdf = self.uiTable.model().dbdata[row][col]
            if isinstance(pdf, QtCore.QString):
                pdf = unicode(pdf).encode("utf-8")
                #print pdf
            #Если поле заполнено
            if pdf is not None:
                
                if len(pdf) > 0:
                    if os.name == 'nt':
                        if os.path.isfile(os.getcwd().decode('cp1251') + os.sep + pdf.decode('utf-8')):
                            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.getcwd().decode('cp1251') + os.sep + pdf.decode('utf-8')))
                        else:
                            print "File missing: %s" % (os.getcwd().decode('cp1251') + os.sep + pdf.decode('utf-8'))
                            
                    else:
                        if os.path.isfile(os.getcwd() + os.sep + pdf.decode('utf-8')):
                            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(os.getcwd() + os.sep + pdf.decode('utf-8')))
                        else:
                             print "File missing: %s" % (os.getcwd() + os.sep + pdf.decode('utf-8'))
            else:
                #если поле не заполнено
                #то добавлять в таблицу!!!
                dialog = QtGui.QFileDialog()
                filename=unicode(dialog.getOpenFileName())
                if filename.endswith("pdf") or filename.endswith("Pdf") or filename.endswith("PDF"):
                    #self.uiTable.model().dbdata[row][col] = filename.encode('utf-8')
                    output_directory = os.getcwd() + "/PDF/"
                    in_file = filename.split("/")[-1]
                    out_file =  os.path.splitext(in_file)[0] + '.txt'
                    
                    call(['pdftotext', filename, output_directory + out_file])
                    copy_to(filename, output_directory)
                    full_txt = open(output_directory + out_file)
                    db_file = '/PDF/' + filename.encode('utf-8').split('/')[-1]
                    self.uiTable.model().dbdata[row][col] = '/PDF/' + filename.encode('utf-8').split('/')[-1]#.decode('utf-8')
                    self.cur.execute("update articles set full_txt = '%s', fulltxt_presence = TRUE, file_path = '%s' where uid = %s" % (pg.escape_string(full_txt.read()), db_file, uid))
                    full_txt.close()
                    self.cur.execute("update articles set fts = setweight( coalesce(to_tsvector(name_orig), ''), 'A') || ' ' || setweight( coalesce(to_tsvector(name_alt), ''), 'A') || ' ' || setweight( coalesce(to_tsvector(abstract), ''), 'B') || ' ' || setweight( coalesce(to_tsvector(full_txt), ''), 'C') where uid = %s" % uid)
                    os.remove(output_directory + out_file)
                    self.uiTable.model().emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

    #Поиск совпадений в тексте и вывод их на вкладку "Совпадения"
    def select_coincidence(self):
        indx = self.uiTable.currentIndex()
        num = self.uiTable.model().header.index(u"УИН")
        uid = int(self.uiTable.model().dbdata[indx.row()][num])
        cur = self.conn.cursor()
        if len(self.query_queue) > 0:
            cur.execute("select full_txt from articles where uid = %i" % uid)
            text = cur.fetchone()[0]
            query = self.query_queue[-1]
            query_object = self.query_object[-1]
            if text is not None:
                #print query_object
                cur.execute(coincidence_query % (query_object, uid))
                self.ui.resultTextBrowser.setHtml(u"Вы искали: <b>%s</b>.<p>Результаты:<p>" % query_object + cur.fetchone()[0].decode('utf-8'))
                self.ui.resultTextBrowser.verticalScrollBar().setValue(0)

    def select_abstract(self):
        indx = self.uiTable.currentIndex()
        num = self.uiTable.model().header.index(u"УИН")
        #print num
        uid = int(self.uiTable.model().dbdata[indx.row()][num])
        self.cur.execute(abstract_query % uid)
        res = self.cur.fetchone()
        self.abstract = ''
        if res is None:
            pass
        else:
            self.abstract = res[0]
        self.ui.abstractDock.setWindowTitle(u'Реферат')
        self.ui.textBrowser.clear()
        if self.abstract is None:
            self.abstract = ' '
        
        self.ui.textBrowser.append(QtCore.QString(self.abstract.decode("utf-8")))
        self.ui.textBrowser.verticalScrollBar().setValue(0)

    def set_statusbar(self):
        ind = self.uiTable.currentIndex()
        mess = u"Строка: %i, столбец: %i, Значение: %s" % (ind.row()+1, ind.column()+1, self.uiTable.model().data(ind, 0).toString())
        self.statusBar().showMessage(mess)
        
    def register_hotkey(self):
        pass

    def clipboard_search(self):
        clipb = QtGui.QApplication.clipboard()
        print unicode(clipb.text())
        self.fts_search(clipb.text())

    def fts_search(self, *args):
        #*** TODO -Поиск в выделенном. 
        
        self.view="fts_search"
        if len(args) > 0:
            tx = unicode(args[0])
            self.uiSearch.lineEdit.setText(tx)
            tx_search = tx
            query_str = [u'Полнотекстовый поиск %s по' % tx]
            params = []
        else:    
            tx = unicode(self.uiSearch.lineEdit.text())
            tx_search = tx
            query_str = [u'Полнотекстовый поиск %s по' % tx]
            params = []
            if self.uiSearch.checkBox_name_orig.isChecked():# or self.uiSearch.checkBox_name_alt.isChecked():
                params.append('a')
                query_str.append(u'названию,')
        
            if self.uiSearch.checkBox_abst.isChecked():
                params.append('b')
                query_str.append(u'реферату,')

            if self.uiSearch.checkBox_full_txt.isChecked():
                params.append('c')
                query_str.append(u'полным текстам,')
        
        #если выделено всё
        
        if len(params) == 4:
            params=[]
        #self.columns.insert(4,'index')
        #self.header.insert(4, u'Индекс релевантности')
        #for i in self.header:
        #    print i,
        #print self.columns
        #надо так: в зависимости от вида query % (cols[:4], tx, params, cols[4:])
        
        if not tx.startswith("+"):
            tx_corr = self.process_query(tx, params)
        else:
            tx_corr = tx[1:]


        query = fts_query_short % (", ".join(self.columns[:4]), ", ".join(self.columns[4:]),  tx_corr)
        
        if len(tx_search) > 0:
            self.uiSearch.setEnabled(False)
            self.query_queue.append(query)
            self.query_object.append(tx)
            #Это поиск в найденном!!! 
            if self.uiSearch.checkBox_search_results.isChecked():
                query = self.search_results(self.cur, query)
                
            if self.uiSearch.search_in_selected.isChecked() and len(self.uiTable.selectedIndexes()) > 0:
                uid_list = "AND uid IN ({0})".format(", ".join(map(str, self.uiTable.model().getFromColumn(u'УИН', [x.row() for x in self.uiTable.selectedIndexes()]))))
                if len(uid_list) > 13:
                    query = query.format(uid_list)
                else:
                    query = query.format('')
            else:
                query = query.format('')
                

            self.ftsThread = SearchThread(self.cur, query, tx_corr, tx)
            

            self.ftsThread.start()
            self.connect(self.ftsThread, QtCore.SIGNAL('dataFetched'), self.fts_model)
        else:
            pass

    #поиск для TableModel, возвращает массив найденных данных
    def fts_model(self, data_list, differ, num_res, query, search_words, *args, **kwargs):
        tx = unicode(self.uiSearch.lineEdit.text())
        self.mess = (args[1] if args[1] != 2 else None)
        #print query
        self.mess = (kwargs['message'] if 'message' in kwargs.keys() else None)
        prev_query = ''
        if len(args) > 0:
            prev_query = args[0]
            #print prev_query
        if u"Индекс релевантности" not in self.header:
            self.header.insert(4,u'Индекс релевантности')
        self.ui.abstractDock.setWindowTitle(u'Результаты')
                  
        self.uiTable.model().dbdata = data_list
        self.uiTable.model().reset()
        self.ui.textBrowser.clear()
        self.uiSearch.setEnabled(True)
        self.queryForm.setEnabled(True)

        translation = u"Полнотекстовый поиск, %s записей, %s" % (str(num_res), tx)

        words = []
        for word in self.queryForm.model.words:
            words.append(word[0])
                            
        if translation not in words and not 'NoAPP' in args:
            self.append_query(translation, query, 'fts', prev_query, search_words)
        else:
            pass

        if self.mess is None:
            self.ui.textBrowser.append(QtCore.QString(u"""Вы искали: <b>"%s"</b><p>Найдено <b>%i</b> записей</p><p>Время выполнения запроса:
<b>%.4g сек.</b></p>""" % (tx, num_res, differ)))
        else:
            self.ui.textBrowser.append(QtCore.QString(u"""История поиска:<b>%s</b><p>Найдено %i записей<p>Время выполнения запроса:<b>%.4g сек.</b>"""%(self.mess, num_res, differ)))

    def full_view(self):
        self.searchThread = SearchThread(self.cur, query_standart % short_view, u'')
        self.searchThread.start()
        self.connect(self.searchThread, QtCore.SIGNAL('dataFetched'), self.change_view)
        self.connect(self.searchThread, QtCore.SIGNAL('statusBar'), self.statusBar().showMessage)


    #Первоначальный запрос
    def start_query(self, data_list, differ, num_res):
        
        self.ui.abstractDock.setWindowTitle(u'Стандартный вид')
        tx = u' '
        #print type(data_list)
        self.uiTable = self.createTable(data_list)
        
        self.ui.horizontalLayout_3.addWidget(self.uiTable)
        
        self.connect(self.uiTable, QtCore.SIGNAL('clicked(QModelIndex)'), self.show_pdf)

        self.connect(self.uiTable, QtCore.SIGNAL('clicked(QModelIndex)'), self.set_statusbar)
        self.connect(self.mainSelectionModel, QtCore.SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.select_abstract)
        self.connect(self.uiTable, QtCore.SIGNAL('activated(QModelIndex)'), self.set_statusbar)
        self.connect(self.uiTable, QtCore.SIGNAL('activated(QModelIndex)'), self.select_abstract)
        
        self.connect(self.uiTable, QtCore.SIGNAL('clicked(QModelIndex)'), self.select_coincidence)
        self.connect(self.uiTable, QtCore.SIGNAL('activated(QModelIndex)'), self.select_coincidence)

        self.ui.textBrowser.clear()
        self.ui.textBrowser.append(QtCore.QString(u"""<b>%s</b><p>Всеого в базе <b>%i</b> записей</p><p>Время загрузки:
<b>%.4g сек.</b></p>""" % (tx, num_res, differ)))

    #Составной запрос с потоком
    def compl_search(self):
        #*** TODO -Поиск в выделенном. 
        query = []
        search_words = []
        rev_cols = dict([(columns[key], key) for (key) in columns])
        first_line = [self.uiSearchAll.field_comboBox0, self.uiSearchAll.cont_comboBox0, self.uiSearchAll.search_lineEdit]
        numb = 0

        #Если в строке введен текст
        if len(first_line[2].text()) > 0:
            #Начало запроса
            #Тут также стоит учитывать краткий/полный вид
            query.append("SELECT %s FROM articles" % ", ".join(self.columns))                        

            if unicode(first_line[1].currentText()) == u'подобен':
                search_text = unicode(first_line[2].text())
                search_words.append(search_text)
                query.append(""", plainto_tsquery('%s') query """ % search_text)
                #print 'search_text', search_text
            else:
                query.append("")


            #for i in 
            #Разбиваем строку с колонками на отдельные поля
            el = rev_cols[unicode(first_line[0].currentText())].split(' ')
            #print 'el', el
            #для каждого элемента колонки
            #for j in el:
            while len(el) > 0:
                #выбираем оператор сравнения
                j = el.pop()
                t = sel_oper[unicode(first_line[1].currentText())]
                #print j, 'element'
                if unicode(first_line[1].currentText()) == u'подобен':
                    search_words.append(unicode(first_line[2].text()))
                    query[1] = """, plainto_tsquery('%s') query """ % unicode(first_line[2].text())
                else:
                    query.append("")
            
                #Добавляем к запросу
                #Приделываем к каждому элементу AND кроме последнего
                if not t.startswith('fts'):
                    search_words.append(unicode(first_line[2].text()))
                    query.append(j + ' ' + (t % (unicode(first_line[2].text()) + (" OR" if len(el) > 0 else ''))))
                else:                                
                    t = 'fts @@@ query'
                    query.append('' + t + (" OR" if len(el) > 0 else ''))

            #Теперь то же самое для остальных добавленных кнопок    
            for i in self.uiSearchAll.button_list:
                if len(i[3].text()) > 0:
                    query.append(log_oper[unicode(i[0].currentText())])
                    el = rev_cols[unicode(i[1].currentText())].split(' ')
                    
                    while len(el) > 0:
                        j = el.pop()

                        t = sel_oper[unicode(i[2].currentText())]
                        #print 'el, oper', j, t
    
                        if unicode(i[2].currentText()) == u'подобен':
                            search_words.append(unicode(i[3].text()))
                            query[1] = query[1] + """, plainto_tsquery('%s') query_%s """ % (unicode(i[3].text()), numb)
                            
                        else:
                            query.append("")
        
                        if not t.startswith('fts'):
                            search_words.append(unicode(i[3].text()))
                            query.append(j + ' ' + (t % (unicode(i[3].text()) + (" OR" if len(el) > 0 else ''))))
                        else:
                            t = 'fts @@@ query_%s' % numb
                            query.append('' + t + (" OR" if len(el) > 0 else ''))
        
                numb = numb + 1
            
        if len(query) > 0:    
            query[1] = query[1] + ' WHERE'
            #Поиск в выделенном

        if len(" ".join(query)) > 0:
            #О боже ну и ужас! :)
            self.uiTable.selectedIndexes()
            if len(self.uiTable.selectedIndexes()) > 0:
                sel_indexes = (" AND uid IN ({0})".format(", ".join(map(str, self.uiTable.model().getFromColumn(u'УИН', [x.row() for x in self.uiTable.selectedIndexes()])))) if self.uiSearchAll.search_in_selected.isChecked() else "")
            else:
                sel_indexes = ''
            compl_query = " ".join(query) + sel_indexes + " ORDER BY year DESC"
            #Замена неправильного положения запятой и удаление двойных и тройных пробелов
            compl_query = compl_query.replace(" , ", ", ")
            compl_query = re.sub("\s+" , " ", compl_query)
            search_words = u', '.join(search_words)
        
            
            if self.uiSearchAll.checkBox_search_results.isChecked():
                compl_query = self.search_results(self.cur, compl_query)
                self.complThread = SearchThread(self.cur, compl_query, search_words)
            else:
                self.complThread = SearchThread(self.cur, compl_query, search_words)
        
            self.uiSearchAll.setEnabled(False)
            self.complThread.start()
            self.connect(self.complThread, QtCore.SIGNAL('dataFetched'), self.compl_model)


            print 'compl_query', compl_query
        else:
            pass
   
    def change_data(self, data_list, differ, num_res, query, *args):
        self.uiTable.model().reset()
        self.uiTable.model().dbdata = data_list
        



    #Берет данные из потока и отображает в таблицу. Для стандартного вида
    def change_view(self, data_list, differ, num_res, query, *args):
        
        self.uiTable.model().reset()
        self.uiTable.model().dbdata = data_list
        #self.uiTable.model().reset()
        self.ui.textBrowser.clear()
        self.ui.textBrowser.append(QtCore.QString(u"""<p>Всеого в базе <b>%i</b> записей</p><p>Время загрузки:
<b>%.4g сек.</b></p>""" % (num_res, differ)))

    def compl_model(self, data_list, differ, num_res, query, prev_query, search_words, *args, **kwargs):
        
        self.mess = (args[1] if args[1] != 2 else None)
        self.search_words = search_words
        print 'search words', self.search_words
        query_transl = []
        if u'Индекс релевантности' in self.header:
            self.header.remove(u'Индекс релевантности')
        if u'Индекс релевантности' in self.uiTable.model().header:
            self.uiTable.model().header.remove(u'Индекс релевантности')
        
        #Для первой строчки кнопок формы
        query_transl.append(unicode(self.uiSearchAll.field_comboBox0.currentText()))
        query_transl.append(unicode(self.uiSearchAll.cont_comboBox0.currentText()))
        query_transl.append(unicode(self.uiSearchAll.search_lineEdit.text()))

        #Для остальных строк с кнопками
        for i in self.uiSearchAll.button_list:
            if len(i[3].text()) > 0:
                query_transl.append(unicode(i[0].currentText()))
                query_transl.append(unicode(i[1].currentText()))
                query_transl.append(unicode(i[2].currentText()))
                query_transl.append(unicode(i[3].text()))

        self.ui.abstractDock.setWindowTitle(u'Результаты')
        
        self.uiTable.model().dbdata = data_list
        
        self.uiSearchAll.setEnabled(True)
        self.queryForm.setEnabled(True)
        self.uiTable.model().reset()
        self.ui.textBrowser.clear()
        if self.mess is None:
            self.ui.textBrowser.append(QtCore.QString(u"""Вы искали: <b>"%s"</b><p>Найдено <b>%i</b> записей</p><p>Время выполнения запроса:<b>%.4g сек.</b></p>""" % (u" ".join(query_transl), num_res, differ)))
        else:
             self.ui.textBrowser.append(QtCore.QString(u"""История поиска:<b>%s</b><p>Найдено %i записей<p>Время выполнения запроса:<b>%.4g сек.</b>"""%(self.mess, num_res, differ)))
        translation = u"Составной поиск, " + u"%s записей, " % str(num_res) + u" ".join(query_transl)
        
        words = []
        for word in self.queryForm.model.words:
            words.append(word[0])
            
        if translation not in words and not 'NoAPP' in args:
            self.append_query(translation, query, 'compl', '', search_words)
        else:
            pass

    def append_query(self, translation, query, funct, prev_query, search_words, *args):
        
        self.queryForm.model.append(translation, [query, funct, prev_query, search_words])

                
    def kw_search(self):
        tx = unicode(self.uiSearchKw.lineEdit.text())
        #*** TODO -Поиск в выделенном. 
        start_time = datetime.datetime.now()
        
        #проверяет checkbox'ы и в зависимости от результата производит поиск
        
        if len(tx) > 0:
            if not self.uiSearchKw.checkBox_comm.isChecked():
                if not tx.startswith("+"):
                    tx_search = self.process_query(tx, [''])
                else:
                    tx = tx[1:]
                query = fts_kw_query % (", ".join(self.columns[:4]), ", ".join(self.columns[4:]), tx_search)
                if self.uiSearchKw.checkBox_search_results.isChecked():
                    query = self.search_results(self.cur, query)

                if self.uiSearchKw.search_in_selected.isChecked() and len(self.uiTable.selectedIndexes()) > 0:
                    uid_list = "AND uid IN ({0})".format(", ".join(map(str, self.uiTable.model().getFromColumn(u'УИН', [x.row() for x in self.uiTable.selectedIndexes()]))))
                    if len(uid_list) > 13:
                        query = query.format(uid_list)
                    else:
                        query = query.format('')
                else:
                    query = query.format('')

            elif self.uiSearchKw.checkBox_comm.isChecked():
                if not tx.startswith("+"):
                    tx_search = self.process_query(tx, ['a'])
                else:
                    tx_search = tx[1:]
                query = fts_kw_query % (", ".join(self.columns[:4]), ", ".join(self.columns[4:]), tx_search)
                if self.uiSearchKw.checkBox_search_results.isChecked():
                    query = self.search_results(self.cur, query)
                if self.uiSearchKw.search_in_selected.isChecked():
                    uid_list = "AND uid IN ({0})".format(", ".join(map(str, self.uiTable.model().getFromColumn(u'УИН', [x.row() for x in self.uiTable.selectedIndexes()]))))
                    if len(uid_list) > 13:
                        query = query.format(uid_list)
                    else:
                        query = query.format('')
                else:
                    query = query.format('')


            self.kwThread = SearchThread(self.cur, query, tx)
            self.kwThread.start()
            self.connect(self.kwThread, QtCore.SIGNAL('dataFetched'), self.kw_model)

            #elif self.uiSearchKw.checkBox_taxon.isChecked() and not self.uiSearchKw.checkBox_comm.isChecked():
            #    if not tx.startswith("+"):
            #        tx_search = self.process_query(tx, ['b'])
            #    else:
            #        tx_search = tx[1:]
            #    query = fts_kw_query % (", ".join(self.columns[:4]), ", ".join(self.columns[4:]), tx_search)
            #    if self.uiSearchKw.checkBox_search_results.isChecked():
            #        query = self.search_results(self.cur, query)
            #    if self.uiSearchKw.search_in_selected.isChecked():
            #        uid_list = "AND uid IN ({0})".format(", ".join(map(str, self.uiTable.model().getFromColumn(u'УИН', [x.row() for x in self.uiTable.selectedIndexes()]))))
            #        if len(uid_list) > 13:
            #            query = query.format(uid_list)
            #        else:
            #            query = query.format('')
            #    else:
            #        query = query.format('')

            #    self.kwThread = SearchThread(self.cur, query, tx)
            #    self.kwThread.start()
            #    self.uiSearchKw.setEnabled(False)
            #    self.connect(self.kwThread, QtCore.SIGNAL('dataFetched'), self.kw_model)
        else:
            pass

    def kw_model(self, data_list, differ, num_res, query, prev_query, list_words, *args, **kwargs):
        tx = unicode(self.uiSearchKw.lineEdit.text()) 
        self.mess = (args[1] if args[1] != 2 else None)
        self.list_words = list_words
        print 'kw_model', self.list_words
        if u"Индекс релевантности" not in self.header:
            self.header.insert(4,u'Индекс релевантности')
        self.ui.abstractDock.setWindowTitle(u'Результаты')
        
        self.uiTable.model().dbdata = data_list
        self.uiTable.model().reset()
        self.ui.textBrowser.clear()
        self.uiSearchKw.setEnabled(True)
        self.queryForm.setEnabled(True)
        translation = u"Ключевые слова, %s записей, %s" % (str(num_res), tx)

        words = []
        for word in self.queryForm.model.words:
            words.append(word[0])

        if translation not in words and not 'NoApp' in args:
            self.append_query(translation, query, 'kw', '', list_words)
        else:
            pass
        if self.mess is None:
            self.ui.textBrowser.append(QtCore.QString(u"""Вы искали: <b>"%s"</b><p>Найдено <b>%i</b> записей</p><p>Время выполнения запроса:<b>%.4g сек.</b></p>""" % (tx, num_res, differ)))
        else:
            self.ui.textBrowser.append(QtCore.QString(u"""История поиска:<b>%s</b><p>Найдено %i записей<p>Время выполнения запроса:<b>%.4g сек.</b>"""%(self.mess, num_res, differ)))



    def add_entry(self):
        
        """
        Функция для добавления новых данных. Извлекает введенные данные 
        из формы ввода и добавляет в базу. Или меняет существующую запись.
        """
        
        authors = self.ui.lineEdit_authors.lineEdit.text()
        name_orig = self.ui.lineEdit_name_orig.text()
        name_alt = self.ui.lineEdit_name_alt.text()
        year = self.ui.lineEdit_year.text()
        source = self.ui.lineEdit_source.lineEdit.text()
        publisher = self.ui.lineEdit_publisher.lineEdit.text()
        publ_place = self.ui.lineEdit_publ_place.lineEdit.text()
        editors = self.ui.lineEdit_editors.lineEdit.text()
        volume = self.ui.lineEdit_vol.text()
        number = self.ui.lineEdit_number.text()
        issue = self.ui.lineEdit_issue.text()
        series = self.ui.lineEdit_series.text()
        part = self.ui.lineEdit_part.text()
        pages = self.ui.lineEdit_pages.text()
        tables = self.ui.lineEdit_tables.text()
        maps = self.ui.lineEdit_maps.text()
        illustrations = self.ui.lineEdit_ill.text()
        refs = self.ui.lineEdit_publ_numb.text()
        publ_number = self.ui.lineEdit_publ_number.text()
        zool_rec = self.ui.lineEdit_zool_rec.text()
        series_area = self.ui.lineEdit_series_area.text()
        publ_lang = self.ui.lineEdit_publ_lang.text()
        publ_country = self.ui.lineEdit_publ_country.lineEdit.text()
        publ_type = self.ui.lineEdit_publ_type.lineEdit.text()
        num_ed_mpk = self.ui.lineEdit_num_ed_mpk.text()
        main_ind_mpk = self.ui.lineEdit_main_ind_mpk.text()
        pat_owner = self.ui.lineEdit_pat_owner.text()
        publ_date = self.ui.dateEdit_publ_date.date()
        ref_code = self.ui.lineEdit_ref_code.text()
        udk = self.ui.lineEdit_udk.text()
        issn = self.ui.lineEdit_issn.text()
        isbn = self.ui.lineEdit_isbn.text()
        file_path = self.ui.lineEdit_file_path.text()
        comm_keywords = self.ui.lineEdit_comm_keywds.lineEdit.text()
        taxon_keywords = self.ui.lineEdit_taxon_keywds.lineEdit.text()
        abstract = self.ui.textEdit_abstract.toPlainText()
                
        attr_dict = {u"authors":authors, u"name_orig":name_orig, u"name_alt":name_alt, u"source":source, u"editor":editors, u"publ_location":publ_place, u"publication":publisher, u"year":year, u"volume":volume, u"number":number, u"issue":issue, u"series":series, u"part":part, u"pages":pages, u"tables":tables, u"maps":maps, u"illustrations":illustrations, u"refs":refs, u"series_area":series_area, u"language":publ_lang, u"type":publ_type, u"ref_code":ref_code, u"udk":udk, u"zool_rec":zool_rec, u"issn":issn, u"isbn":isbn, u"common_keywords":comm_keywords, u"taxon_keywords":taxon_keywords, u"publ_number":publ_number, u"publ_date":publ_date, u"publ_country":publ_country, u"num_ed_mpk":num_ed_mpk, u"main_mpk_ind":main_ind_mpk, u"pat_owner":pat_owner, u"file_path":file_path, u"file_size":None, u"abstract":abstract}
        
        #Вот тут еще добавить потоков для вставки и правки

        #для INSERT
        
        if unicode(self.ui.add_dataDOCK.windowTitle()).startswith(u"Добавление"):
            
            command = InsertCommand(self.uiTable.model(), self.uiTable, attr_dict, self.uiTable.model().columns, self.cur, self.conn, 'Adding a row to TableModel, row %i' % (len(self.uiTable.model().dbdata) + 1))
            self.undoStack.push(command)

        #для UPDATE
        elif unicode(self.ui.add_dataDOCK.windowTitle()).startswith(u"Правка"):

            command = EditRowCommand(self.uiTable.model(), self.uiTable, self.uid, attr_dict, self.uiTable.model().columns, self.cur, "Edition of row %i" % self.uid)
            self.undoStack.push(command)
        

    def db_info(self):

        QtGui.QMessageBox.about(self, u"О программе", u"""<b>Библиографическая база данных<br>с полнотекстовым поиском</b><p><small>Написана на Python, QT4, база данных - PostgreSQL 8.4. <br>Распространяется по лицензии GPL.</small></p>""")
        
        

#Класс представления данных, переопределенный для добавления собственного контекстного меню

class TableView(QtGui.QTableView):

    def __init__(self, parent = None):
        QtGui.QTableView.__init__(self, parent)
        #self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        #quitAction = QtCore.QAction("Quit", self)
        #quitAction.triggered.connect(qApp.quit)
        #self.addAction(quitAction)
        

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        copyAction = menu.addAction(u"Копировать")
        #cropAction = menu.addAction(u'Сохранить результаты')
        selectRowAction = menu.addAction(u'Выделить строку')
        selectColAction = menu.addAction(u'Выделить столбец')
        selectAllAction = menu.addAction(u'Выделить все')
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == copyAction:
            self.copy_text()
        elif action == selectColAction:
            self.selectColumn(self.currentIndex().column())

        elif action == selectRowAction:
            self.selectRow(self.currentIndex().row())
        #elif action == cropAction:
        #    print 'crop'
        elif action == selectAllAction:
            self.selectAll()

    #Копирование текста в буфер обмена
    def copy_text(self):
        text = {}
        txt_out = []

        for i in self.selectedIndexes():
            if i.row() not in text.keys():
                text[i.row()]= {}
                if i.column() not in text[i.row()].keys():
                    text[i.row()][i.column()] = unicode(i.data().toString())
            else:
                if i.column() not in text[i.row()].keys():
                    text[i.row()][i.column()] = unicode(i.data().toString())
        for i in text.keys():
            ln = []
            for j in text[i]:
                ln.append(text[i][j])
            txt_out.append(u"\t".join(map(unicode, ln)))

        clipb = QtGui.QApplication.clipboard()
        clipb.setText(u"\n".join(map(unicode, txt_out)))


#Класс модели данных
class BiblTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain,  headerdata, undostack, conn, statusbar, columns, exec_query, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        #print dir(conn.cursor())
        self.cur = conn.cursor()
        self.statusbar = statusbar

        self.undostack = undostack
       
        self.dbdata = datain 
        self.header = headerdata
        self.columns = columns
        self.exec_query=exec_query
    
    def rowCount(self, parent):
        #кол-во строк
        return len(self.dbdata)

    def columnCount(self, parent):
        #кол-во колонок
        if len(self.dbdata) < 1:
            return 0
        else:
            return len(self.dbdata[0])

    def getFromColumn(self, col, list_ind):
        #Возвращает список значений для всех выделенных строк и определенной колонки
        #В частности. нам это нужно для получения списка UID для всех выделенных строк
        num = self.header.index(col)
        return [self.dbdata[i][num] for i in list_ind]

    def get_value(self, index):
        i = index.row()
        j = index.column()
        try:
            return self.dbdata[i][j].decode("utf-8")
        except AttributeError:
            return self.dbdata[i][j]

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        value = self.get_value(index)

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if isinstance(value, datetime.datetime):
                return QtCore.QDateTime(value)#.strftime('%d/%m/%Y, %H:%M')
            else:
                return QtCore.QVariant(value)
        elif role == QtCore.Qt.TextAlignmentRole:
                return QtCore.QVariant(QtCore.Qt.AlignCenter)
        return QtCore.QVariant()
                
        if isinstance(self.dbdata[index.row()][index.column()], str):
            return QtCore.QVariant(self.dbdata[index.row()][index.column()].decode("utf-8"))
        elif isinstance(self.dbdata[index.row()][index.column()], datetime.datetime):
            print "datetime!!!"
            return QtCore.QVariant(QtCore.QDateTime(self.dbdata[index.row()][index.column()]))#.strftime('%d/%m/%Y, %H:%M'))
        else:                           
            return QtCore.QVariant(self.dbdata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        ## тут задаются заголовки
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
                        
            #Для исправления ошибки при убирании столбца индекса релевантности
            #при переходе от полнотекстового поиска к сложному при отображении всех столбцов
            try:
                return QtCore.QVariant(self.header[col])
            except IndexError:
                return QtCore.QVariant(self.header[col-1])
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant("%s" % str(col + 1))

        return QtCore.QVariant()

    def sort(self, Ncol, order):
        
        self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.dbdata = sorted(self.dbdata, key=operator.itemgetter(Ncol))        
        if order == QtCore.Qt.DescendingOrder:
            self.dbdata.reverse()
        self.emit(QtCore.SIGNAL("layoutChanged()"))

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole:
            
            val = QtCore.QVariant(self.get_value(index))
            
            command = EditCommand(self, index.row(), index.column(), self.columns, val, QtCore.QVariant(value), self.cur, self.exec_query, 'Edition of a single cell')
            self.undostack.push(command)
            
            return True
        else:
            return False

    #установка флагов для того, чтобы ячейка становилась редактируемой
    def flags(self, index):

        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        #Это делает нередактируемыми колонки даты добавления и изменения
        if isinstance(index.data().toPyObject(), QtCore.QDateTime):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    
class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, undostack, connection, view, obj, parent=None):
        super(TreeModel, self).__init__(parent)
        self.parents=[]
        self.dbdata = data
        self.rootItem = TreeItem([u"Дубли"])
        self.setupModelData(self.dbdata, self.rootItem)
        self.undostack = undostack
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.view = view
        self.obj = obj
        
    def changeData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            item.setData(unicode(value.toString()))

    def setData(self, index, value, role):
        if index.isValid() and role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            
            prev_value = QtCore.QVariant(self.getValue(index))
            item = index.internalPointer()
            
            #item.setData(unicode(value.toString()))
            
            #print index.column(), index.row()
            command = SetData(self, index, value, prev_value, self.view)
            self.undostack.push(command)
            
            return True
        else:
            return False

    def addBranch(self, index, childname=u'Новый элемент', role = QtCore.Qt.EditRole):
        self.insertRows(0, 1, index)
        child_index = self.index(0, 0, index)
        self.setData(child_index, QtCore.QVariant(childname), role)
        return True

    def insertRows(self, position=0, count=1, parent=QtCore.QModelIndex()):
        #node = self.nodeFromIndex(parent)
        #self.beginInsertRows(parent, position, position + count - 1)
        #child = TreeItem(u'Новый элемент', node)
        #node.insertChild(child, position)
        #self.endInsertRows()
        
        command = InsertRow(self, parent, position)
        self.undostack.push(command)
        return True

    def deleteDupl(self, child, position, count=1, parent=QtCore.QModelIndex()):
        #Истинные дубли можно найти только по названию.
        #Добавить undo, redo!
        #и подумать, как же сделать redo!
        #select count (distinct aaa) from (select distinct name_orig from articles) as aaa; 16791!!!!
        #Разрешить удалять не все, одну запись обязательно оставить!!!
        data = child.internalPointer().data(1)
        
        if data[-1] in string.digits:
            data = data[:-10]
        #print data

        #if self.obj == 'name_orig':
        #Удаляем только те, у кого есть родитель, самого родителя не трогаем, чтобы осталось хоть что-то
        if parent.internalPointer() is not None:
            node = self.nodeFromIndex(parent)
            if len(node.childItems) > 0:
                #self.beginRemoveRows(parent, position, position + count -1)
                #node.childItems.pop(position)
                #self.endRemoveRows()
                #self.cursor.execute("select uid from articles where %s = '%s'" % (self.obj, data))
                #print self.cursor.fetchall()
                
                command = DeleteDupl(self, child, parent, position)
                self.undostack.push(command)
                #self.cursor.execute("delete from articles where %s = '%s'")

    def renameDupl(self, item, parent):
        parent_data = QtCore.QVariant(parent.internalPointer().data(parent.column()))
        prev_items = []
        for i in parent.internalPointer().childItems:
            prev_items.append(i.data(0))
        
        #for i in xrange(len(parent.internalPointer().childItems)):
        #    ind = self.index(i, parent.column(), parent)
        #    self.setData(ind, parent_data, QtCore.Qt.EditRole)
        #    self.view.dataChanged(ind, ind)
            #for i in parent.childItems:
            #update articles set column_name = parent_data where column_name == child_data
        command = RenameDuplicates(self, self.view, parent, parent_data, prev_items)
        self.undostack.push(command)
        
    def setMain(self, item, parent, child, view = None):
        if parent.internalPointer() is not None:
            parent_data = QtCore.QVariant(parent.internalPointer().data(parent.column()))
            child_data = QtCore.QVariant(child.internalPointer().data(child.column()))
        
        
            command = SetMain(self, parent, parent_data, child, child_data, view, self.cursor)
            self.undostack.push(command)
        
    def removeRows(self,item,  child, position, count=1, parent=QtCore.QModelIndex()):
        
        node = self.nodeFromIndex(parent)
        
        if len(node.childItems) > 0:
            command = DeleteRow(item, self, child, parent, position)
            self.undostack.push(command)
            #delete column_name from dupl_table where column_name == child_data
            #
                
    def nodeFromIndex(self, index):
        if index.isValid():
            return index.internalPointer()
        else:
            return self.rootItem
        

    #def parent(self, child):
    #    node = self.nodeFromIndex(child)
    #    if node is None:
    #        return QtCore.QModelIndex()
    #    #parent = node.parent
    #    #if parent is None:
    #    #    return QtCore.QModelIndex()
    #    #grandparent = parent.parent
    #    #if grandparent is None:
    #    #    return QtCore.QModelIndex()
    #    #row = grandparent.rowOfChild(parent)
    #    row = child.row()
    #    parent = node.parent
    #    assert row != -1
    #    return self.createIndex(row, 0, parent)


    def getValue(self, index):
        item = index.internalPointer()
        return item.data(index.column())

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        item = index.internalPointer()
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return QtCore.QVariant(item.data(index.column()))
                
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            #print self.rootItem.data(section)[0], 'header'
            #print self.rootItem.data(section)
            
            return QtCore.QVariant(self.rootItem.data(section)[0])

        return None

    def index(self, row, column, parent):

        #if not self.hasIndex(row, column, parent):
        #    return QtCore.QModelIndex()
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)


    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()


    #переделать, чтобы была поддержка нескольких столбцов
    def setupModelData(self, lines, parent):
        ind = []
        self.parents.append(parent)
        ind.append(0)
        col_numb=parent.columnCount()
        numb = 0
        #for i in xrange(col_numb):
            
            
        for line in lines:
            numb+=1
            lineData=line[0]
            #print lineData
            self.parents[-1].appendChild(TreeItem(lineData, self.parents[-1]))
            
            columnData = line[1]
            #print columnData
                
            self.parents.append(self.parents[-1].child(self.parents[-1].childCount() - 1))

            
            #print columnData
            for j in columnData:
                self.parents[-1].appendChild(TreeItem(j, self.parents[-1]))
            if len(self.parents) > 0:
                self.parents.pop()

                
    
class TreeItem(object):
    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    
    def appendChild(self, item):
        self.childItems.append(item)


    def insertChild(self, item, position):
        self.childItems.insert(position, item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData

        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0
    def setData(self, data):
        self.itemData = data

class SetData(QtGui.QUndoCommand):
     def __init__(self, treemodel, index, value, prev_value, view, description = "Setting data to an element of TreeModel"):
         super(SetData, self).__init__(description)
         self.model = treemodel
         self.index = index
         self.parent = index.internalPointer().parent()
         self.column = self.index.column()
         self.row = self.index.row()
         self.value = value
         self.prev_value = prev_value
         self.item = self.index.internalPointer()
         self.view = view
         self.prev_index = index
         
     def redo(self):
         self.item.setData(unicode(self.value.toString()))
         self.view.dataChanged(self.index, self.index)


     def undo(self):
         self.item.setData(unicode(self.prev_value.toString()))
         index = self.model.createIndex(self.row, self.column, self.item)
         self.view.dataChanged(index, index)


class RenameDuplicates(QtGui.QUndoCommand):
    def __init__(self, treemodel, treeview, parent, parent_data, prev_items, description = 'Renaming all duplicates to their parent name'):
        super(RenameDuplicates, self).__init__(description)
        self.model = treemodel
        self.view = treeview
        self.parent = parent
        self.parent_data = parent_data
        self.child_items = self.parent.internalPointer().childItems
        self.prev_items = prev_items
        self.prev_dict = {}
        self.val = None
        for i in self.prev_items:
            if i[-1] in string.digits:
                self.val = i[:-10]
            else:
                self.val = i
            
            self.prev_dict[self.val]=[]
            self.model.cursor.execute("""select uid from articles where %s = '%s' """ % (self.model.obj, pg.escape_string(self.val.encode("utf-8"))))
            for r in self.model.cursor.fetchall():
                self.prev_dict[self.val].append(r[0])
        #print self.prev_dict

    def redo(self):
        if unicode(self.parent_data.toString())[-1] in string.digits:
            print unicode(self.parent_data.toString())[:-10]
            self.parent_data = QtCore.QVariant(unicode(self.parent_data.toString())[:-10])



        for i in xrange(len(self.child_items)):
            ind = self.model.index(i, self.parent.column(), self.parent)
            self.model.changeData(ind, self.parent_data, QtCore.Qt.EditRole)
            self.view.dataChanged(ind, ind)
        temp_query = []                    
        for i in self.prev_dict.keys():
            temp_query.append("%s = '%s'" % (self.model.obj, pg.escape_string(i)))
            #print " OR ".join(temp_query)
        query = """update articles set %s = '%s' where %s """ % (self.model.obj, self.parent_data, " OR ".join(temp_query))
        self.renameThread = RenameThread(self.model.connection, query)
        self.renameThread.start()
        #self.model.cursor.execute("""update articles set %s = '%s'  where %s """ % (" OR ".join(temp_query)))
        print "executed"

    def undo(self):
        temp_query = []
        for i in xrange(len(self.child_items)):
            ind = self.model.index(i, self.parent.column(), self.parent)
            self.model.changeData(ind, QtCore.QVariant(self.prev_items[i]), QtCore.Qt.EditRole)
            self.view.dataChanged(ind, ind)
        for i in self.prev_dict.keys():
            
            for id in self.prev_dict[i]:
                query = """update articles set %s = '%s' where uid = '%s' """ % (self.model.obj, i, id)
                self.renameThread = RenameThread(self.model.connection, query)
                #self.model.cursor.execute("""update dupl_table set %s = '%s' where uid = '%s'  """ % (self.model.obj, i, id))
                

class InsertRow(QtGui.QUndoCommand):
    def __init__(self, treemodel, parent_ind, position, count=1, description='Addition of a single row from TreeModel'):
        super(InsertRow, self).__init__(description)
        self.model = treemodel
        self.parent = parent_ind
        self.position = position
        self.count = count
        #*** TODO Добавить поле "Дата добавления публикации"

    def redo(self):
        node = self.model.nodeFromIndex(self.parent)
        self.model.beginInsertRows(self.parent, self.position, self.position + self.count - 1)
        child = TreeItem(u'Новый элемент', node)
        node.insertChild(child, self.position)
        self.model.endInsertRows()
        
    def undo(self):
        node = self.model.nodeFromIndex(self.parent)
        self.model.beginRemoveRows(self.parent, self.position, self.position + self.count - 1)
        node.childItems.pop(self.position)
        self.model.endRemoveRows()

#Класс для отмены объявления главной записи в TreeModel
class SetMain(QtGui.QUndoCommand):
    def __init__(self, treemodel, parent, pdata, child, cdata, treeview, cursor, description='Setting of main entry in TreeView'):
        super(SetMain, self).__init__(description)
        self.model = treemodel
        self.view = treeview
        self.parent = parent
        self.child = child
        self.pdata = pdata
        self.cdata = cdata
        self.cursor = cursor

    def redo(self):
        self.model.setData(self.parent, self.cdata, QtCore.Qt.EditRole)
        self.model.setData(self.child, self.pdata, QtCore.Qt.EditRole)
        self.view.dataChanged(self.parent, self.child)
        

    def undo(self):
        self.model.setData(self.parent, self.pdata, QtCore.Qt.EditRole)
        self.model.setData(self.child, self.cdata, QtCore.Qt.EditRole)
        self.view.dataChanged(self.parent, self.child)
        
#Класс для удаления дубля публикации из главной таблицы
class DeleteDupl(QtGui.QUndoCommand):
    def __init__(self, treemodel, child_ind, parent_ind, position, count=1, description='Deletion of a duplicate from TreeModel'):
        super(DeleteDupl, self).__init__(description)
        self.model = treemodel
        self.child_ind = child_ind
        self.parent_ind = parent_ind
        self.row = self.child_ind.row()
        self.position = position
        self.count = count
        self.child = child_ind.internalPointer()
        self.conn = self.model.connection
        self.cur = self.conn.cursor()
        self.val = self.child.data(1)
        self.prev_dict = {}
        self.corr_val = None
        if self.val[-1] in string.digits:
            self.corr_val = self.val[:-10]
        else:
            self.corr_val = self.val
        
        self.prev_dict1 = {}
         
        #self.cur.execute("select uid from articles where %s = '%s'" % (self.model.obj, self.corr_val))
        #self.prev_dict[self.val]=[]
        #for i in self.cur.fetchall():
        #    self.prev_dict[self.val].append(i[0])
            
        self.cur.execute("select * from articles where %s = '%s'" % (self.model.obj, self.corr_val))
        for i in self.cur.fetchall():
            self.prev_dict1[i[0][-6]].append(i[0])

    def redo(self):
        node = self.model.nodeFromIndex(self.parent_ind)
        self.model.beginRemoveRows(self.parent_ind, self.position, self.position + self.count - 1)
        node.childItems.pop(self.position)
        self.model.endRemoveRows()
        
        self.cur.execute("delete from articles where %s = '%s'" % (self.model.obj, self.corr_val))
      
    def undo (self):
        node = self.model.nodeFromIndex(self.parent_ind)
        self.model.beginInsertRows(self.parent_ind, self.position, self.position + self.count - 1)
        node.insertChild(self.child, self.position)
        self.model.endInsertRows()
     
        for i in self.prev_dict1.values():
            self.cur.execute("insert into articles values (%s)" % " ,".join(i))

#Класс для отмены удаления строки в списке дублей
class DeleteRow(QtGui.QUndoCommand):
    def __init__(self, item, treemodel, child_ind, parent_ind, position, count=1, description='Deletion of a single row from TreeModel'):
        super(DeleteRow, self).__init__(description)
        self.model = treemodel
        self.item = item
        self.child_ind = child_ind
        self.parent_ind = parent_ind
        self.row = self.child_ind.row()
        self.position = position
        self.count = count
        self.child = child_ind.internalPointer()
        self.conn = self.model.connection
        self.cur = self.conn.cursor()
        self.val = self.child.data(1)
        self.prev_dict = {}
        self.corr_val = None
        if self.val[-1] in string.digits:
            self.corr_val = self.val[:-10]
        else:
            self.corr_val = self.val
        
        self.cur.execute("select uid from %s where %s = '%s'" % (self.item[0], self.item[1], self.corr_val))
        self.prev_dict[self.val]=[]
        for i in self.cur.fetchall():
            self.prev_dict[self.val].append(i[0])

    def redo(self):
        node = self.model.nodeFromIndex(self.parent_ind)
        self.model.beginRemoveRows(self.parent_ind, self.position, self.position + self.count - 1)
        node.childItems.pop(self.position)
        self.model.endRemoveRows()
        self.cur.execute("""delete from %s where %s = '%s'""" % (self.item[0], self.item[1], self.corr_val))
        #self.cur.execute("""update articles set %s = '%s' where %s = '%s' """ % (self.model.obj, 'NULL', self.model.obj, self.corr_val))

    def undo(self):
        node = self.model.nodeFromIndex(self.parent_ind)
        self.model.beginInsertRows(self.parent_ind, self.position, self.position + self.count - 1)
        node.insertChild(self.child, self.position)
        self.model.endInsertRows()
        #for id in self.prev_dict.values()[0]:
        #    print id
        #print self.corr_val, 
        for id in self.prev_dict[self.val]:
            self.cur.execute("""insert into %s (%s, uid) values ('%s', '%s') """ % (self.item[0], self.item[1], pg.escape_string(self.corr_val.encode("utf-8")), id))

#Класс для отмены редактирования ячейки
class EditCommand(QtGui.QUndoCommand):
    def __init__(self, tablemodel, row, column, columns, prev_value, value, cursor, exec_query, description, ):
        super(EditCommand, self).__init__(description)
        self.model = tablemodel
        self.row = row
        self.column = column
        self.columns = columns
        self.prev_value = prev_value
        self.value = value
        self.dbdata = self.model.dbdata
        self.cur = cursor
        self.exec_query=exec_query
        #*** TODO Добавить поле "Дата добавления публикации"

    def redo(self):
        index = self.model.index(self.row, self.column)
        #print index.row(), index.column()
        #print type(self.model.dbdata)
        #print self.value.toString()
        
        self.dbdata[index.row()][index.column()] = self.value
        if self.exec_query==True:
            try:
                self.cur.execute("""update articles set %s = '%s' where uid = %s""" % (self.columns[index.column()], unicode(self.value.toString()), (self.model.dbdata[index.row()][-1].toInt()[0] if isinstance(self.model.dbdata[index.row()][-1], QtCore.QVariant) else self.dbdata[index.row()][-1])))
            except KeyError:
                pass

        self.model.emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

    def undo(self):
        index = self.model.index(self.row, self.column)
        self.model.dbdata[index.row()][index.column()] = self.prev_value
        if self.exec_query==True:
            try:
                self.cur.execute("""update articles set %s = '%s' where uid = %s""" % (self.columns[index.column()], unicode(self.prev_value.toString()), (self.model.dbdata[index.row()][-1].toInt()[0] if isinstance(self.model.dbdata[index.row()][-1], QtCore.QVariant) else self.dbdata[index.row()][-1])))
            except KeyError:
                pass

        self.model.emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)


        
#Класс для отмены добавления новой записи
class InsertCommand(QtGui.QUndoCommand):
    def __init__(self, tablemodel, tableview, attr_dict, columns, cursor, connection, description):
        super(InsertCommand, self).__init__(description)
        self.model = tablemodel
        self.view=tableview
        self.columns = columns
        self.cursor = cursor
        self.attr_dict = attr_dict
        self.conn = connection
        
        #т.к. в таблице записи нумеруются с 0, 
        #а в граф.интерфейсе - с 1
        #Что-то надо будет с этим сделать. Не очень важно, а все равно досадно
        self.uid = len(self.model.dbdata)+1
        self.db_uid = self.uid-1
        

    def redo(self):
        column_names = []
        values = []
        table_values = {}
        table_row = []
        output_directory = os.getcwd() + "/PDF/" 
        filename = unicode(self.attr_dict["file_path"])
        
        #Если поле с pdf-файлом заполнено, то меняем значение на то, которое мы хотим добавить в базу
        if len(self.attr_dict['file_path']) > 0:
            db_filename = u"/PDF/" + unicode(self.attr_dict['file_path']).split('/')[-1]
            self.attr_dict["file_path"] = QtCore.QString(db_filename)

        if filename.endswith("pdf") or filename.endswith("Pdf") or filename.endswith("PDF"):
            in_file = self.attr_dict["file_path"].split("/")[-1]
            out_file = os.path.splitext(unicode(in_file))[0] + '.txt'
        self.cursor.execute("select setval ('articles_uid_seq', %s)" % self.db_uid)
        
        for i in xrange(len(self.model.columns)):
            table_row.append(None)
        for key in self.attr_dict:

            if isinstance(self.attr_dict[key], QtCore.QString) and len(self.attr_dict[key]) > 0:
                column_names.append(key)
                values.append(self.attr_dict[key])
                table_values[str(key)] = self.attr_dict[key]

            elif isinstance(self.attr_dict[key], QtCore.QDate):
                values.append(QtCore.QString("%i.%i.%i" % (self.attr_dict[key].day(), self.attr_dict[key].month(), self.attr_dict[key].year())))
                column_names.append(key)
                table_values[str(key)] = "%i.%i.%i" % (self.attr_dict[key].day(), self.attr_dict[key].month(), self.attr_dict[key].year())

            else:
                if self.attr_dict[key] is not None and len(self.attr_dict[key]) > 0:
                    column_names.append(key)
                    values.append(attr_dict[key])
                    table_values[str(key)] = attr_dict[key]
        table_values['uid'] = self.uid
        
                
        for i in xrange(len(values)):
            temp_value = u"%s" % unicode(values[i])
            values[i] = pg.escape_string(temp_value.encode("utf-8"))

        for i in xrange(len(column_names)):
            column_names[i] = str(column_names[i])
                
        for key in table_values:
            if key in self.model.columns:
                table_row[self.model.columns.index(key)] = table_values[key]

        index = self.model.index(self.uid, 1)
        self.model.dbdata.append(table_row)
        #self.view.updateGeometries()
        self.model.emit(QtCore.SIGNAL("layoutChanged()"))
        #print self.model.rowCount(index)
        #self.model.emit(QtCore.SIGNAL("rowsInserted(QModelIndex)"), index)
        
        self.cursor.execute(u"INSERT INTO ARTICLES " + '(' + u", ".join(i.decode("utf-8") for i in column_names) + ')' + ' VALUES ' + '(' + ", ".join(u"'%s'" % i.decode("utf-8") for i in values) + ')')
        
        #После выполнения запроса на вставку записи 
        #можно добавить полный текст, но только если это поле заполнено!
        if len(filename) > 0:
            call(['pdftotext', filename, output_directory + out_file])
            copy_to(filename, output_directory)
            self.cursor.execute("select max(uid) from articles")
            #можно попробовать last_uid = select nextval ('articles_uid_seq', false)"
            last_uid = self.cursor.fetchone()[0]
            full_txt = open(output_directory + out_file)
            
            #Вставляем текст в таблицу
            
            self.cursor.execute("update articles set full_txt = '%s', fulltxt_presence = TRUE where uid = %s" % (pg.escape_string(full_txt.read()), last_uid))
            full_txt.close()
            self.cursor.execute("update articles set fts = setweight( coalesce(to_tsvector(name_orig), ''), 'A') || ' ' || setweight( coalesce(to_tsvector(name_alt), ''), 'A') || ' ' || setweight( coalesce(to_tsvector(abstract), ''), 'B') || ' ' || setweight( coalesce(to_tsvector(full_txt), ''), 'C') where uid = %s" % last_uid)
            
            self.model.dbdata[-1][0] = db_filename
            
            #self.model.emit(QtCore.SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            #self.model.emit(QtCore.SIGNAL("layoutChanged()"))
            #и удаляем не нужный нам более текстовый файл
            os.remove(output_directory + out_file)

    def undo(self):
        index = self.model.index(self.uid, 1)
        
        #Определение строки, которую надо удалить
        del_str = 0
        for i in xrange(len(self.model.dbdata)):
            if self.model.dbdata[i][7]==self.uid:
               del_str =  i
        self.model.dbdata.pop(del_str)
        self.model.emit(QtCore.SIGNAL("layoutChanged()"))
        
        #также надо не забыть про удаление pdf-файла при удалении записи о нем
        self.cursor.execute("select file_path from articles where uid = %s" % self.uid)
        filepath = self.cursor.fetchone()[0]
        if filepath is not None:
            os.remove(os.getcwd() + filepath)
            
        self.cursor.execute("DELETE FROM articles where uid = '%s'" % self.uid)


#Класс для редактирования существующей записи
class EditRowCommand(QtGui.QUndoCommand):
    def __init__(self, tablemodel, tableview, uid, attr_dict, columns, cursor, description):
        super(EditRowCommand, self).__init__(description)
        self.model = tablemodel
        self.tableview = tableview
        self.columns = columns
        self.cursor = cursor
        self.attr_dict = attr_dict
        self.uid = uid
        self.index = self.tableview.currentIndex()
        self.prev_values = self.model.dbdata[self.index.row()]
        self.cursor.execute("select full_txt, fts, fulltxt_presence from articles where uid = '%s'" % self.uid)
        self.prev_values_fts = self.cursor.fetchone()
        #*** TODO Добавить поле "Дата добавления публикации"
        

    def redo(self):
        column_names = []
        values = []
        table_values = {}
        table_row = []
        query_part = []
        output_directory = os.getcwd() + "/PDF/"
        filename = unicode(self.attr_dict["file_path"])

        if filename.endswith("pdf") or filename.endswith("Pdf") or filename.endswith("PDF"):
            in_file = self.attr_dict["file_path"].split('/')[-1]
            out_file = os.path.splitext(unicode(in_file))[0] + '.txt'


        for i in xrange(len(self.model.columns)):
            table_row.append(None)


        for key in self.attr_dict:
          
            if isinstance(self.attr_dict[key], QtCore.QString) and len(self.attr_dict[key]) > 0:
                column_names.append(key)
                values.append(self.attr_dict[key])
                table_values[str(key)] = self.attr_dict[key]

            elif isinstance(self.attr_dict[key], QtCore.QDate):
                values.append(QtCore.QString("%i.%i.%i" % (self.attr_dict[key].day(), self.attr_dict[key].month(), self.attr_dict[key].year())))
                column_names.append(key)
                table_values[str(key)] = "%i.%i.%i" % (self.attr_dict[key].day(), self.attr_dict[key].month(), self.attr_dict[key].year())

            else:
                if self.attr_dict[key] is not None and len(self.attr_dict[key]) > 0:
                    column_names.append(key)
                    values.append(attr_dict[key])
                    table_values[str(key)] = attr_dict[key]

        table_values['uid'] = self.uid
        for i in xrange(len(values)):
            temp_value = u"%s" % unicode(values[i])
            values[i] = pg.escape_string(temp_value.encode("utf-8"))
            
        for i in xrange(len(column_names)):
            column_names[i] = str(column_names[i])
            
        for key in table_values:
            if key in self.model.columns:
                table_row[self.model.columns.index(key)] = table_values[key]
                
        
        
        self.model.dbdata[self.index.row()] = table_row
        self.model.emit(QtCore.SIGNAL("layoutChanged()"))


        for k in column_names:

            elem = table_values[k]
            temp_value = u"%s" % unicode(elem)
            query_part.append(u" %s = '%s', " % (unicode(k), unicode(pg.escape_string(temp_value.encode("utf-8")).decode("utf-8"))))
            
        self.cursor.execute(u'UPDATE articles SET ' + u" ".join(query_part)[:-2] + u" WHERE uid = %s" % self.uid)
        #После выполнения запроса на вставку записи
        #можно добавить полный текст, но только если это поле заполнено!
        #И если оно отлично от того, что уже есть!!!!!
        #if self.model.dbdata[]
        if len(filename) > 0:
            
            
            full_txt = open(output_directory + out_file)
            #Вставляем текст в таблицу 
            #И не забыть сделать escape для текста!

            #print pg.escape_string(full_txt.read())

            self.cursor.execute("update articles set full_txt = '%s', fulltxt_presence = TRUE where uid = %s" % (pg.escape_string(full_txt.read()), self.uid))
            self.cursor.execute("update articles set fts = setweight( coalesce(to_tsvector(name_orig), ''), 'A') || ' ' || setweight( coalesce(to_tsvector(name_alt), ''), 'A') || ' ' || setweight( coalesce(to_tsvector(abstract), ''), 'B') || ' ' || setweight( coalesce(to_tsvector(full_txt), ''), 'C') where uid = %s " % self.uid)
            full_txt.close()
            os.remove(output_directory + out_file)
    
    def undo(self):
         self.model.dbdata[self.index.row()] = self.prev_values
         self.model.emit(QtCore.SIGNAL("layoutChanged()"))
         query = []
         for i in xrange(len(self.prev_values)):
             query.append("%s = '%s', " % (self.columns[i], self.prev_values[i]))
         
         self.cursor.execute("UPDATE articles set " + " ".join(query)[0:-2] + " WHERE uid = %s" % (self.uid))
         self.cursor.execute("""UPDATE articles set full_txt = '%s', fts = '%s', fulltxt_presence = '%s' where uid = %s""" % (pg.escape_string(self.prev_values_fts[0]), pg.escape_string(self.prev_values_fts[1]), self.prev_values_fts[2], self.uid))

class ImportDataCommand(QtGui.QUndoCommand):
    #Сделать Thread

    def __init__(self, tablemodel, tableview, database_columns, cursor, table_name, file_name, description):
        super(ImportDataCommand, self).__init__(description)
        self.model = tablemodel
        #self.main_model = self.main_table.model()
        self.view = tableview
        self.cur = cursor
        self.dbcols = database_columns
        self.cols = {}
        self.num_rows = 0
        self.table_name = str(table_name)
        self.cur.execute("select max(uid) from %s" % table_name)
        self.last_uid = self.cur.fetchone()[0]
        self.filename = unicode(file_name)
        
        for i in xrange(len(self.dbcols)):
            if self.dbcols[i] != '':
                self.cols[i]=self.dbcols[i]
                

    def redo(self):
        #Попробовать psycopg2.copy_from
        #... хотя тогда можно будет работать 
        #только с csv...
        #
        #query = ("""insert into %s (%s) values """ % (self.table_name, ", ".join(self.cols.values())))
        #for i in xrange(len(self.model.dbdata)):
        #    data_list = []
        #    for ind in self.cols.keys():
        #        data_list.append(str(adapt(self.model.dbdata[i][ind])))
        #    final_query = query + "(" + ", ".join(data_list) + ")"
        #    self.cur.execute(final_query)
        #    print "OK, %i" % i

        query = """insert into %s (%s) values """ % (self.table_name, ", ".join(self.cols.values()))
        names = []
        
        data = []
        for col in self.cols.values():
            names.append("""%%(%s)s""" % col)

        final_query = query + "(" + ", ".join(names) + ")"


        for i in xrange(len(self.model.dbdata)):
            named_dict = {}
            for ind in self.cols.keys():
                named_dict[self.cols[ind]] = str((self.model.dbdata[i][ind]))
            data.append(named_dict)

        #print final_query, named_dict
        self.num_rows = len(data)
        self.cur.executemany(final_query, data)
        


    def undo(self):
        #print "undo"
        #print self.num_rows
        #print self.last_uid
        self.cur.execute("delete from %s where uid > %s and uid <= %s" % (self.table_name, self.last_uid, self.num_rows+self.last_uid))


class DeleteRowCommand(QtGui.QUndoCommand):
   def __init__(self, tablemodel, tableview, database_columns, cursor, description):
       super(DeleteRowCommand, self).__init__(description)
       self.model = tablemodel
       self.view = tableview
       self.cursor = cursor
       self.dbcolumns = database_columns
       self.columns = self.model.columns
       self.index = self.view.currentIndex()
       self.values = self.model.dbdata[self.index.row()]
       #print self.columns.index("uid"), self.model.dbdata[self.index.row()][self.columns.index("uid")]
       #print self.dbcolumns, "dbcolumns"
       #print self.columns, "columns"
       self.cursor.execute("select * from articles where uid = %s" % self.model.dbdata[self.index.row()][self.columns.index("uid")])
       self.dbvalues = self.cursor.fetchall()[0]

   def redo(self):
       uid = self.model.dbdata[self.index.row()][self.columns.index("uid")]
       del self.model.dbdata[self.index.row()]
       self.model.emit(QtCore.SIGNAL("layoutChanged()"))
       self.cursor.execute("select file_path from articles where uid = %s" % uid)
       file_path = self.cursor.fetchone()[0]
       
       if file_path is not None:
           os.remove(os.getcwd() + file_path)
           
               
       self.cursor.execute("delete from articles where uid = %s" % uid)
      
   def undo(self):
       self.cursor.execute("select column_name from information_schema.columns where table_name = 'articles'")
       cols = []
       vals = []
       db_cols = []
       tmp = self.cursor.fetchall()
       for i in tmp:
           db_cols.append(i[0])

       self.model.dbdata.insert(self.index.row(), self.values)
       self.model.emit(QtCore.SIGNAL("layoutChanged()"))
       for i in xrange(len(self.dbvalues)):
           if self.dbvalues[i] is not None:
               if len(str(self.dbvalues[i])) > 0:
                   cols.append("%s, " % db_cols[i])
                   vals.append("'%s', " % pg.escape_string(str(self.dbvalues[i])))

       
       self.cursor.execute("INSERT INTO articles (" + " ".join(cols)[0:-2] + ") " + "VALUES (" + " ".join(vals)[0:-2] + ")")
       
class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent, words, *args):
        QtCore.QAbstractListModel.__init__(self, parent, *args)
        self.words = words

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.words)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.words[index.row()][0])
        else:
            return QtCore.QVariant()
    
    def clear(self):
        self.words = []
        self.reset()

    def append(self, key, value):
        self.words.append([key, value])
        self.reset()
    
    def setAllData(self, new_list):
        self.words = new_list
        self.reset()

def main():
    
    app = QtGui.QApplication(sys.argv)
    splash_pict = QtGui.QPixmap("splashscreen.png")
    splash = QtGui.QSplashScreen(splash_pict, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pict.mask())
    splash.show()
    app.setStyle('cleanlooks')
    translator = QtCore.QTranslator(app)
    translator.load("qt_ru.qm")
    app.installTranslator(translator)
    window=MainView()
    window.setWindowTitle(u'База данных %s на %s' % (dbname, host))
    #time.sleep(3)
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

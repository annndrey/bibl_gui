#!/usr/bin/python                                                              
# -*- coding: utf-8 -*-

import psycopg2
import difflib
import itertools
import string
import operator as o
import datetime 
from Levenshtein import ratio
def canonize(l):
    #Убираем всякие запятые и строки короче 3 знаков (не работает для русских символов)
    stop_symbols = '.,!?:;-\n\r()[]'
    table = string.maketrans("","")
    for i, j in enumerate(l):
        l[i] = " ".join([x for x in l[i].translate(table, stop_symbols).split() if len(x) > 3])
    return dict.fromkeys(list(set(l)))

def diff(a, b):
    return difflib.SequenceMatcher(None, a, b).real_quick_ratio()

def diff2(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def calculate_ratios(strings, threshold):
    dupls = []
    while len(strings) > 0:
        i = strings.pop(0)
        l = len(i)
        minl = l - 5
        maxl =  l + 5
        #отбираем только те строки, которые попадают в заданный интервал
        #
        s = [x for x in strings if minl <= len(x) <= maxl]
        #s = [x for x in strings if len(x) == l]

        #print difflib.get_close_matches(i, s)
        #print len(s)
        d = [[i,x] for x in s if ratio(x, i) > threshold]
        if len(d) > 0:
            for e in d:
                for r in e:
                    print r
            ans = raw_input("what to do? d/p, {0} items left".format(len(strings)))
            print ans
            dupls.append(d)
    return [x for x in dupls if len(x) > 0]

sttime = datetime.datetime.now()
print "It started at", sttime
conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%d  password='%s'" % ('bibliography', 'annndrey', 'localhost', 5432, 'andreygon'))
cur = conn.cursor()
cur.execute("select lower(name_orig), lower(authors), year from articles")
a = cur.fetchall()
print "Data fetched", len(a)
for i,j in enumerate(a):
    a[i] = " ".join(j)

a = canonize(a)
print "Obvious duplicates removed", len(a)

ratio =  calculate_ratios(a.keys(), 0.8)
endtime = datetime.datetime.now()
for i in ratio:
    print "{0}\n\t{1}".format(i[0][0], i[0][1])

print "It worked for", endtime - sttime

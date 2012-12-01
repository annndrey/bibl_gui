#!/usr/bin/python                                                              
# -*- coding: utf-8 -*-

import psycopg2, pg
import difflib
import itertools
import string
import operator as o
import datetime 

sttime = datetime.datetime.now()
print "It started at", sttime
conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%d  password='%s'" % ('bibliography', 'annndrey', 'localhost', 5432, 'andreygon'))
cur = conn.cursor()
sim_query = """select distinct name_orig, similarity(name_orig, %s) as sim from articles where name_orig %% %s and name_orig != %s order by sim desc limit 5"""
name_query = "select distinct name_orig from articles order by name_orig asc"

cur.execute(name_query)
names = []

for i in cur.fetchall():
    names.append(list(itertools.repeat(i[-1], 3)))

#Оно же не проиндексировано?

cur.executemany(sim_query, names)
for i in cur.fetchall():
    print i

endtime = datetime.datetime.now()
print "It worked for", endtime - sttime

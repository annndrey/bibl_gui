#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2 as db
from pg import escape_string
import time

dbname = "bibliography"
user = "annndrey"
host = "localhost"
passwd = "andreygon"

#f = open("publ_loc.txt", "r")
conn = db.connect("dbname='%s' user='%s' host='%s'  password='%s'" % (dbname, user, host, passwd))
cur = conn.cursor()

cur.execute("select type from articles where type is not null")
a = cur.fetchall()
b = []
for i in a:
    if len(i[0]) > 0:
#        nm = i[0].split(",")
#        for j in nm:
#            k = j.split(", ")
#            for u in k:
#                if u.startswith(" "):
#                        u = u[1:]
#        
        b.append(i[0])#.replace(".", ""))

c = set(b)
c = list(c)
c.sort()


for i in c:#f.readlines():
    #f.write("%s\n" % escape_string(i))
    cur.execute("insert into type (publ_type) values ('%s')" % escape_string(i.replace("\n", "")))
    print i#.replace("\n", "")
    conn.commit()

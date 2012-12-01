#!/usr/bin/python                                                               
# -*- coding: utf-8 -*-                                                         

#Вот в таком виде оно и будет храниться:
#[[запрос1,[дубль1,дубль2]]
#[запрос2, [дубль1,дубль2]]
#итд
#
#]
#Поиск дублей!
import psycopg2, time
from pg import escape_string

dbname = "bibliography"
user = 'annndrey'
host = "localhost"
passwd = "andreygon"

col='source'

conn = psycopg2.connect("dbname='%s' user='%s' host='%s'  password='%s'" % (dbname, user, host, passwd))

cur = conn.cursor()

a = []
b=[]

cur.execute("select distinct name_orig from articles")

for i in cur.fetchall():
    a.append(i[0])

print cur.rowcount

cnt = 0

f = open("duplicates.txt", "w")
for i in a:
    if i is not None and len(i) > 0 and len(i.split(" ")) > 1:
        c=[]
        #print i
        #f.write("Строка поиска: %s\n" % i)
        c.append(i)
        
        #print '\n'
            
        cur.execute("""select distinct name_orig, similarity(name_orig, %s) as sim from dupl_table  where name_orig %% %s""",  (escape_string(i), escape_string(i)))#, escape_string(i)))
        #print 'выполняю запрос %s ' % i
        a.pop(a.index(i))
        if cur.rowcount > 1: 
            #print "Строка поиска: %s" % i
            d=[]
            qr=[ "\nЗапрос: %s" % i]
            for j in cur.fetchall():
                if i != j[0] and j[1] > 0.6:
                    qr.append(" Ответ: %s %s " % j)
                    #print " Ответ: %s %s " % j
                #print type(i)
                #print type(j[0])
                    try:
                        a.pop(a.index(j[0]))
                    except:
                        pass

            if len(qr) > 1:
                for line in qr:
                    print line

                print "Осталось: %s" % len(a)
                #if j[1] > 0.5:
              #      print "Результат: %s, схожесть:%f" %( j[0], j[1])
                #    d.append("%s, %f" %( j[0], j[1]))
             #       f.write("Результат: %s, схожесть:%f\n" %( j[0], j[1]))
            #print ('\n')
                #    c.append(d)
            #b.append(c)
            #print c




            
#for i in b:
#    print i
            #f.write("\n\n")
#        time.sleep(1)
            









            #c = []
            #b = {}
            #r = {}
            #for j in cur.fetchall():
            #    c.append(j[1])
            #    b[j[1]] = j[0]
            #    r[j[1]] = j[2]
            #d = set(c)
            #if len(d) > 1 and len(d) < 5:
            #    
            #    for u in d:
            #        if u != i:# and r[u] < 1:
            #            cnt = cnt +1
            #            print "Запрос: %s" % i
            #            f.write("Запрос: %s\n" % i)
            #            print "Возможный дубликат: rank:%s, uid:%i, назв.: %s" % (r[u], b[u], u)
            #            f.write("Возможный дубликат: rank: %s, uid:%i, назв.: %s\n" % (r[u], b[u], u))
            #        #print b[u]
            #        #print "В строке с uid %s изменим source на %s" % (str(b[u]), i)
            #        #cur.execute("update articles set source = %s", (i, ))
            #            print "\n\n"
            #            f.write("\n\n\n")
            #    #time.sleep(10)
                
#print "Всего %i кандидатов в дубли" % cnt
#f.write("Всего %i кандидатов в дубли" % cnt)
f.close()

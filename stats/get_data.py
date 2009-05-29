#!/usr/bin/python

import MySQLdb
import csv
import sys
sys.path.insert(0, '..')
from lib import Db

cur = Db.getDBH().cursor()
print 'db'
cur.execute('select wsid, count(nid), time from wn_notes'
            ' where wsid != 15'
            ' group by wsid, time order by wsid')

writer = csv.writer(open('usage.csv', 'w'))
print 'write'
writer.writerows(cur.fetchall())

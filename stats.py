#!/usr/bin/python

# this isn't really for public use, I'm just curious how webnote is being
# used

import urllib
from lib import *
from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_SHARDS, TABLE_PREFIX

message.PlainText('disabled')
import sys; sys.exit(1)

class Stats:
    def __init__(self):
        self.conn = Db.getDBH()
        self.db = self.conn.cursor()
    def __del__(self):
        self.db.close()
        self.conn.close()
    
    def mostActive(self):
        all_results = []
        for i in xrange(TABLE_SHARDS):
          notes_table = '%snotes%s' % (TABLE_PREFIX, Db.getShardNum(i))
          workspace_table = '%sworkspaces%s' % (TABLE_PREFIX, Db.getShardNum(i))
          
          sql = """SELECT wsname,
                     COUNT(distinct(%(notes)s.time)) AS numsaves,
                     max(%(workspaces)s.time)
                   FROM %(workspaces)s LEFT JOIN %(notes)s
                   USING(wsid)
                   GROUP BY wsname 
                   ORDER BY numsaves DESC
                   LIMIT 10;""" % {
                     'notes': notes_table,
                     'workspaces': workspace_table
                   }
          self.db.execute(sql)
          all_results += self.db.fetchall()
        
        # sort and take the top 10
        all_results.sort(lambda lhs, rhs: cmp(lhs[1], rhs[1]))
        all_results.reverse()
        self.printResults(all_results[:10],
                          ('Workspace Name',
                           'Number of Saves',
                           'Last Save Time'))

    def mostRecent(self):
        all_results = []
        for i in xrange(TABLE_SHARDS):
          notes_table = '%snotes%s' % (TABLE_PREFIX, Db.getShardNum(i))
          workspace_table = '%sworkspaces%s' % (TABLE_PREFIX, Db.getShardNum(i))
          
          sql = """SELECT wsname,
                     max(%(workspaces)s.time) AS lastsave,
                     count(distinct(%(notes)s.time))
                   FROM %(workspaces)s LEFT JOIN %(notes)s
                   USING(wsid)
                   GROUP BY wsname
                   ORDER BY lastsave DESC
                   LIMIT 10;""" % {
                     'notes': notes_table,
                     'workspaces': workspace_table
                   }
          self.db.execute(sql)
          all_results += self.db.fetchall()
        
        # sort and take the top 10
        all_results.sort(lambda lhs, rhs: cmp(lhs[1], rhs[1]))
        all_results.reverse()
        self.printResults(all_results[:10],
                          ('Workspace Name',
                           'Last Save Time',
                           'Number of Saves'))
    
    def printTableRow(self, tuple, tag='td'):
        def link(s):
            if len(s) == 0:
              return s
            if 'td' == tag and not(s[0] >= '0' and s[0] <= '9'):
                s = "<a href='load.py?name=" + urllib.quote(s) + "'>" + urllib.unquote(s) + "</a>"
            if s[0] >= '0' and s[0] <= '9' and len(s) == 14:
                s = s[0:4] + '-' + s[4:6] + '-' + s[6:8] + ' ' + s[8:10] + ':' + s[10:12] + ':' + s[12:]
            return s
        
        columns = map(lambda x: "<" + tag + ">" + link(str(x)) + "</" + tag + ">", tuple)
        for c in columns:
            print c
        
    def printResults(self, table, header):
        """Prints a table"""
        print "<table><tr>"
        self.printTableRow(header, 'th')
        print "</tr>"
        
        for row in table:
            print "<tr>"
            self.printTableRow(row)
            print "</tr>"

        print "</table>"

    def genStats(self):
        print "Content-type: text/html\n"
        print """<html>
  <head>
    <title>Webnote Statistics</title>
    <style type='text/css'>
table {
  text-align: center;
  border-spacing: 0;
  margin-bottom: 16px;
  background-color: #eee;
}
th {
  background-color: #ccc;
}
td {
  border-top: 1px #000 solid;
  padding: 1px 4px;
}
    </style>
  </head>"""
        print "<body>"
        
        self.mostActive()
        self.mostRecent()
        
        print "</body>\n</html>"

if __name__ == '__main__':
  try:
      s = Stats()
      s.genStats()
  except Exception, e:
      message.Error(e)

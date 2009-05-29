#!/usr/bin/python
import cgi

# Database sql table creation statments
CREATE_WORKSPACE = """
CREATE TABLE if not exists %(table_name)s (
    wsid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    wsname TEXT NOT NULL,
    nextNoteNum INT NOT NULL,
    time TIMESTAMP(14) NOT NULL,
    UNIQUE INDEX (wsname(255))
) TYPE = MyISAM;
"""

CREATE_NOTES = """
CREATE TABLE if not exists %(table_name)s (
    nid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    noteid TEXT NOT NULL,
    text TEXT NOT NULL,
    bgcolor TEXT NOT NULL,
    xposition INT NOT NULL,
    yposition INT NOT NULL,
    height INT NOT NULL,
    width INT NOT NULL,
    zindex INT NOT NULL,
    wsid INT NOT NULL,
    time TIMESTAMP(14) NOT NULL,
    KEY wsid_idx (wsid, time)
) TYPE = MyISAM;
"""
#    FOREIGN KEY (wsid) REFERENCES %(ws_table_name)s (wsid)



def start():
  print """
<p>This is a very simple install script.  It is meant to be run from a web
browser after you copy the files to your web server.  To get this file (and
the other server side files) to execute, you may need to add the following
to your .htaccess file:</p><pre>
  AddHandler cgi-script .py
  Options +ExecCGI</pre>

<p>Anyway, if you're reading this in a browser, I will now test to see that
you have <a href="http://sourceforge.net/projects/mysql-python">MySQLdb</a>, 
the python mysql driver installed.</p>

<p><a href="install.py?s=test">next</a></p>
  """

def test():
  print "<p>Checking for mysqldb . . ."
  try:
    import MySQLdb
    print """
ok.</p><p>Next we will try to create the database tables.  In common-default.py,
you need to set your database information (in the getDBH method, set your
host, username, password, and db name).  After you set your database
information, you need to rename common-default.py to common.py.</p>

<p><a href="install.py?s=create">next</a></p>"""

  except:
    print """
failed.</p><p>Please install 
<a href='http://sourceforge.net/projects/mysql-python'>MySQLdb</a> or ask
your sysadmin to install it for you.</p>"""
    raise

def create():
  print "<p>Trying to create tables . . ."
  try:
    from lib import Db
    from etc import common
    assert common.TABLE_SHARDS > 0
    assert len(common.TABLE_PREFIX) != 0
  except Exception, e:
    print "failed to read db values from config:", e
    raise

  try:
    db = Db.getDBH()
    cur = db.cursor()
    shards = common.TABLE_SHARDS
    max_digits = len(str(shards))
    # create 'workspaces' and 'notes' table for each shard
    for num in xrange(shards):
      num = Db.getShardNum(num)

      table_name = "%s%s%s" % (common.TABLE_PREFIX, "workspaces", num)
      create_sql = CREATE_WORKSPACE % {'table_name': table_name}
      cur.execute(create_sql)

      table_name = "%s%s%s" % (common.TABLE_PREFIX, "notes", num)
      create_sql = CREATE_NOTES % {'table_name': table_name}
      cur.execute(create_sql)
  except Exception, e:
    print "error creating tables:", e
    raise
  
  print "OK!</p>  Successfully installed, you should now be able to use"
  print " <a href='index.old.html'>webnote</a>."

form = cgi.FieldStorage()
print 'Content-type: text/html\n'
print '<html><body>'
go = {'test' : test, 'create' : create}

try:
  go[form['s'].value]()
except KeyError:
  start()
except Exception, e:
  from lib import message
  message.Error(e)

print '</body></html>'

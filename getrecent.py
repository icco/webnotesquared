#!/usr/bin/python

import cgi
from lib import Workspace, Db, message

def main():
  form = cgi.FieldStorage()
  ws = Workspace.Workspace()
  ws.name = form.getfirst('name', '')

  # make sure it's a valid request
  if not ws.name:
    message.PlainText('No name entered.')
    return

  table_name = Db.getTableName(ws.name, 'workspaces')
  ws.db.execute("SELECT"
                " DATE_FORMAT(time, '%%Y-%%m-%%d %%H:%%i:%%s') as T"
                " FROM " + table_name +
                " WHERE wsname=%s", ws.name)
  row = ws.db.fetchone()
  if row:
    message.PlainText(str(row[0]).strip())
    row = ws.db.fetchone()
  else:
    message.PlainText('')

if '__main__' == __name__:
  try:
    main()
  except Exception, e:
    message.Error(e)

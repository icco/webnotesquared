#!/usr/bin/python

import cgi
from etc.common import NUM_DATES
from lib import Workspace, Db, message

def main():
  form = cgi.FieldStorage()
  try:
    offset = int(form.getfirst('offset', '0'))
  except ValueError:
    offset = 0
  ws = Workspace.Workspace()
  ws.name = form.getfirst('name', '')

  # make sure it's a valid request
  if not ws.name:
    message.PlainText('No name entered.')

  ws_table_name = Db.getTableName(ws.name, 'workspaces')
  note_table_name = Db.getTableName(ws.name, 'notes')
  ws.db.execute(("SELECT distinct"
                 " DATE_FORMAT(" + note_table_name + ".time, '%%Y-%%m-%%d %%H:%%i:%%s') as T"
                 " FROM " + note_table_name +
                 " INNER JOIN " + ws_table_name + " USING(wsid)"
                 " WHERE wsname=%s ORDER BY T DESC"
                 " LIMIT %s, %s"), (ws.name, offset, NUM_DATES+1))

  loadTimes = [str(row[0]).strip() for row in ws.db.fetchall()]
  message.PlainText('|'.join(loadTimes))

if '__main__' == __name__:
  try:
    main()
  except Exception, e:
    message.Error(e)

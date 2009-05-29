################################################
# no #! line, run manually from the command line

TRUNCATE_EXISTING = True
SRC_TABLES = [
  ('wn_workspaces', 'wn_notes')
]
LIMIT = 10

from lib import Db

db = Db.getDBH()
cur = db.cursor()

def TruncateTables():
  for i in xrange(Db.TABLE_SHARDS):
    num = Db.getShardNum(i)
    for name in ('workspaces', 'notes'):
      table_name = '%s%s%s' % (Db.TABLE_PREFIX, name, num)
      cur.execute('TRUNCATE %s' % table_name)

def ShardTableNames():
  """Return a dictionary mapping shard number to a list of workspace ids
  that belong on that shard."""
  shard_map = {}
  select_sql = 'SELECT distinct wsname, wsid FROM %s'
  for workspaces, notes in SRC_TABLES:
    cur.execute(select_sql % workspaces)
    for row in cur.fetchall():
      [wsname, wsid] = row
      shard = Db.getWorkspaceShard(wsname)
      shard_map.setdefault(shard, []).append(wsid)
  return shard_map

def CopyData(shard_map):
  """Do the actual copy from SRC_TABLES into the new sharded tables."""
  insert_ws = ('INSERT INTO %s(wsid, wsname, nextNoteNum, time) '
               'SELECT wsid, wsname, nextNoteNum, time '
               'FROM %s WHERE wsid in (%s)')
  insert_notes = ('INSERT INTO %s(nid, noteid, text, bgcolor, xposition, '
                  'yposition, height, width, zindex, wsid, time) '
                  'SELECT nid, noteid, text, bgcolor, xposition, '
                  'yposition, height, width, zindex, wsid, time '
                  'FROM %s WHERE wsid in (%s)')
  for workspaces, notes in SRC_TABLES:
    for shard, values in shard_map.iteritems():
      if LIMIT:
        values = values[:LIMIT]
      table_name = '%s%s%s' % (Db.TABLE_PREFIX, 'workspaces', shard)
      insert = insert_ws % (table_name, workspaces,
                            ','.join([str(x) for x in values]))
      print insert
      cur.execute(insert)

      table_name = '%s%s%s' % (Db.TABLE_PREFIX, 'notes', shard)
      insert = insert_notes % (table_name, notes,
                               ','.join([str(x) for x in values]))
      print insert
      cur.execute(insert)

def main():
  if TRUNCATE_EXISTING:
    TruncateTables()
  shard_map = ShardTableNames()
  CopyData(shard_map)

if '__main__' == __name__:
  main()

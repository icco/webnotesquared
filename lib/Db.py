import MySQLdb, md5
from etc.common import DBHOST, DBUSER, DBPASS, DBNAME, TABLE_SHARDS, TABLE_PREFIX

def getDBH():
  return MySQLdb.connect(host = DBHOST, user = DBUSER,
                         passwd = DBPASS, db = DBNAME);

def getShardNum(num):
  """Given a shard number, return a string that is the shard number (may
  include zero padding)."""
  max_digits = len(str(TABLE_SHARDS))
  num = str(num)
  num_digits = len(num)
  if num_digits < max_digits:
    padding = '0' * (max_digits - num_digits)
    num = '%s%s' % (padding, num)
  return num

def getWorkspaceShard(workspace_name):
  """Given a workspace name, return the shard to look on."""
  key = md5.md5(workspace_name).hexdigest()[:4]
  shard = int(key, 16) % TABLE_SHARDS
  return getShardNum(shard)

def getTableName(workspace_name, table_name):
  """Given a workspace name and the table name, return the full table name."""
  return '%s%s%s' % (TABLE_PREFIX,
                     table_name,
                     getWorkspaceShard(workspace_name))

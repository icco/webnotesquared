"""Edit this file to set various features of webnote"""

# database information
DBHOST = '127.0.0.1'
DBUSER = 'dbuser'
DBPASS = 'dbpass'
DBNAME = 'dbname'
# prefix table names with this
TABLE_PREFIX = "wn_"
# number of table pieces
TABLE_SHARDS = 1

# the root url
BASEURL = 'http://www.aypwip.org/webnote/'

# your email address
HELPEMAIL = 'user@domain.com'

# Something to add to the <head> of all workspaces (e.g., a counter)
CUSTOMHEADER = ""

# should we log to a file? You need to make sure you have the right file
# permissions to use this.
ISLOGGING = 1
LOGFILENAME = '../../logs/webnote-debug.log'

# should we show debug info when the backend has a problem?
SHOWDEBUG = 0
# should we show the js debugging box?
SHOWJSDEBUG = 0

# In the load previous drop down, how many entries should we show?
NUM_DATES = 10

# Timezone uses pytz.  It doesn't really matter unless you want to control
# the timezone saved in MySQL.  See pytz documentation for more details.
try:
  import pytz
  TIMEZONE = pytz.timezone('US/Eastern')
except ImportError:
  TIMEZONE = None

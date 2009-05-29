import os
from etc import common

try:
  import logging
except ImportError:
  common.ISLOGGING = 0

if common.ISLOGGING:
  logObj = logging.getLogger()
  logObj.setLevel(logging.INFO)
  logHandler = logging.FileHandler(common.LOGFILENAME, 'a')
  logFormatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
  logHandler.setFormatter(logFormatter)
  logObj.addHandler(logHandler)

def log(msg):
  if common.ISLOGGING:
    msg = str(msg)
    logObj.info('%s %s' % (os.environ.get('HTTP_USER_AGENT', '?'), 
                           msg.replace('\n', '\\n')))

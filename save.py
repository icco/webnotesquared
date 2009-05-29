#!/usr/bin/python

from etc.common import *
from lib import *

# the main method is here
try:
    ws = Workspace.CreateSave()
    updateTime = ws.commit()
    if updateTime:
        print 'Content-type: text/xml\n'
        print ('<return>\n'
               '  <status value="ok" update="%s"/>\n'
               '</return>'
               % str(updateTime))
    else:
        retMsg('error')
except Exception, e:
  message.Error(e)

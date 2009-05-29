#!/usr/bin/python

from etc.common import *
from lib import *

if '__main__' == __name__:
  try:
    ws = Workspace.CreateLoad()
    if ws is None:
      print 'Location: .\n\n'
    else:
      ws.createHTML()
  except Exception, e:
    message.Error(e)

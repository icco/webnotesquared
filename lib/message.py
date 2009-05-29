"""Messages returned to the user."""

from lib.logger import log
from etc.common import SHOWDEBUG

def Error(ex):
  """ex is an exception"""
  print 'Content-type: text/html\n\n'
  print '<html><body><h2>Congratulations!  You found a bug in Webnote!</h2>'
  print '<p>(or perhaps the database is down)</p>'
  print ("<p>We'll try to have webnote up and running again as soon as "
         "possible</p>")
  if SHOWDEBUG:
    import cgitb
    cgitb.handler()
  print '</body></html>'
  log(str(ex))

def PlainText(s):
  print 'Content-type: text/plain\n\n'
  print s

def Redirect(url=None):
  if not url:
    url = '.'
  
  print 'Location: %s\n\n' % url

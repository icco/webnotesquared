#!/usr/bin/python

"""Generate and RSS2.0 XML file of the workspace."""

import sys, urllib, re, cgi, os, datetime, time
from etc.common import *
from lib import *

reUnicodeChar = re.compile("%u([0-9A-F]{4})")
reHtmlComments = re.compile("<!--.+-->", re.M | re.S)

def unquote(s):
  return reUnicodeChar.sub(lambda x: unichr(int(x.group(1), 16)), s)

def str2datetime(s):
    ret = datetime.datetime.fromtimestamp(time.mktime(time.strptime(s, 
                                          '%Y-%m-%d %H:%M:%S')))
    if TIMEZONE:
      ret = ret - TIMEZONE._utcoffset
    return ret

def findTags(tag, text):
  reTag = re.compile(r"""
      <%(tag)s>          # opening tag
        (?P<value>.+?)   # everything in between the tags.  Non-greedy.
      </%(tag)s>         # the closing tag must match the opening tag
      """ % locals(), re.M | re.S | re.X)
  matches = reTag.findall(text)
  if matches:
    return matches[0]
  return None

if '__main__' == __name__:
  try:
    import datetime
    ws = Workspace.CreateLoad()
    if ws is None:
      message.Redirect()
    else:
      entries = []
      
      for note in ws.notes:
        text = urllib.unquote(unquote(str(note.text)))
      
        # extract geo data
        glat = findTags('geo:lat', text)
        glong = findTags('geo:long', text)
        
        # remove html comments
        text = reHtmlComments.sub('', text)
        
        rssitem = GeoRss2.GeoRssItem(
                    title=cgi.escape(text.strip().split('\n')[0][:60]),
                    description=text,
                    guid=PyRSS2Gen.Guid(os.path.join(BASEURL, 
                                        '%s#%s' % (ws.name, note.noteid))),
                    extras = {'geo:lat': glat,
                              'geo:long': glong})
        entries.append(rssitem)

      # put the recent entries first
      entries.reverse()

      if ws.lasttime:
        dt = str2datetime(ws.lasttime)
      else:
        dt = datetime.datetime.utcnow()
      rss = GeoRss2.GeoRss2(
              title = urllib.unquote(ws.name),
              description = 'Webnote RSS feed',
              link = '%s%s' % (BASEURL, urllib.quote(urllib.quote(ws.name))),
              lastBuildDate = dt,
              items = entries)

      print "Content-type: text/xml\n"
      rss.write_xml(sys.stdout)
  except ImportError:
    message.PlainText('RSS feeds require python2.3+')
  except Exception, e:
    message.Error(e)

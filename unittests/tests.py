import sys
import os
import time
import unittest
import urllib
import urllib2
import re

# include the parent directory so we can import the db
sys.path.insert(0, '..')
from lib import Db
from etc import common

# we need to remove times from the generated page to pass the assert equal
# test
kRemoveTime = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
kRemoveRfcTime = re.compile("\w\w\w, \d\d \w\w\w \d{4} \d\d:\d\d:\d\d GMT")
kJSDebug = re.compile("debugOn = (true|false)")

_BASE = common.BASEURL
_WORKSPACE = urllib.quote(urllib.quote('webnote devel'))
_WORKSPACE_BLANK = urllib.quote(urllib.quote('__wn_devel_3874297'))
_GOLDEN = '2005-05-30 18:17:28'

LOADKNOWN = os.path.join(_BASE, 'load.py?name=webnote%2520devel'
                                '&time=2005-05-30+18%3A17%3A28')
LOAD = os.path.join(_BASE, urllib.quote('webnote%2520devel'))
#RSS  = os.path.join(_BASE, '%s.xml' % _WORKSPACE)
RSS = os.path.join(_BASE, 'rss.py?name=webnote%2520devel'
                          '&time=2005-05-30+18%3A17%3A28')
SAVE = os.path.join(_BASE, 'save.py')
DATES  = os.path.join(_BASE, 'getdates.py?name=%s' % _WORKSPACE)
DATES_BLANK  = os.path.join(_BASE, 'getdates.py?name=%s' % _WORKSPACE_BLANK)
RECENT  = os.path.join(_BASE, 'getrecent.py?name=%s' % _WORKSPACE)
RECENT_BLANK  = os.path.join(_BASE, 'getrecent.py?name=%s' % _WORKSPACE_BLANK)

WSBLANK = """
<workspace name='webnote%20devel' nextNoteNum='3'>
</workspace>"""

WSNOTES = """
<workspace name='webnote%20devel' nextNoteNum='3'>
  <note noteid='note0' bgcolor='#ffff30' xposition='37' yposition='55' height='150' width='250' zindex='1'> test1 </note>
  <note noteid='note1' bgcolor='#ffff30' xposition='37' yposition='242' height='150' width='250' zindex='2'> a%20basic%20test%20with%20some%20html%0A%3Cem%3Efoo%3C/em%3E%0A%0A%3Cstrong%3Erar%3C/strong%3E%0A%0A%3Ca%20href%3D%22http%3A//www.google.com%22%3Egoogle%3C/a%3E </note>
  <note noteid='note2' bgcolor='#ffff30' xposition='342' yposition='244' height='150' width='250' zindex='3'> some%20unicode%20characters%0A%0A%u7528%u6700%u7B80%u5355%u7684%u8BDD%u63CF%u8FF0%u5C31%u662F </note>
</workspace>"""

class WebnoteBackendTests(unittest.TestCase):
  def assertEqualPages(self, received, expected):
    """When comparing pages, some text needs to be removed."""
    # lastloadtime needs to be removed
    received = kRemoveTime.sub('', received)
    expected = kRemoveTime.sub('', expected)
    
    # in the rss feed, the time is in a different format
    received = kRemoveRfcTime.sub('', received)
    expected = kRemoveRfcTime.sub('', expected)
    
    # js debug flag needs to be removed
    received = kJSDebug.sub('', received)
    expected = kJSDebug.sub('', expected)
    
    # replace settings in expected
    expected = expected.replace('$email', common.HELPEMAIL)
    expected = expected.replace('$base', common.BASEURL)
    expected = expected.replace('$numDates', str(common.NUM_DATES))
    
    self.assertEqual(received, expected)

  def testBasicLoad(self):
    """Tests the loading of a page"""
    txt = urllib2.urlopen(LOADKNOWN).read()
    expected = open('testBasicLoad').read()
    self.assertEqualPages(txt, expected)
  
  def testRSS(self):
    """rss feed test"""
    txt = urllib2.urlopen(RSS).read()
    expected = open('testRSS').read()
    file('tmp', 'w').write(txt)
    self.assertEqualPages(txt, expected)
  
  def testGetRecent(self):
    txt = urllib2.urlopen(RECENT).read().strip()
    # make sure the text returned is a valid date
    t = time.strptime(txt, '%Y-%m-%d %H:%M:%S')

    txt = urllib2.urlopen(RECENT_BLANK).read().strip()
    self.assertEqual(txt, '')
  
  def testSave(self):
    """test save.py"""
    urllib2.urlopen(SAVE, WSBLANK)
    # now load the page to see if it's blank
    txt = urllib2.urlopen(LOAD).read()
    expected = open('testSaveBlank').read()
    
    self.assertEqualPages(txt, expected)
    
    # save a workspace, then load it to verify that it happened
    urllib2.urlopen(SAVE, WSNOTES)
    # now load the page to see if it's blank
    txt = urllib2.urlopen(LOAD).read()
    expected = open('testBasicLoad').read()
    
    self.assertEqualPages(txt, expected)

  def testGetDates(self):
    txt = urllib2.urlopen(DATES).read()
    txt = txt.strip()
    self.assertEqual(txt, '2005-05-30 22:24:38|2005-05-30 22:24:31|'
                          '2005-05-30 22:24:29|2005-05-30 22:24:24|'
                          '2005-05-30 22:24:17|2005-05-30 18:17:28')
    txt = urllib2.urlopen(DATES_BLANK).read()
    txt = txt.strip()
    self.assertEqual(txt, '')
  
  def __del__(self):
    """Some cleanup code so the database doesn't get too icky"""
    db = Db.getDBH()
    cur = db.cursor()
    cur.execute('SELECT wsid FROM wn_workspaces where wsname=%s',
                [urllib.unquote(_WORKSPACE)])
    wsid = cur.fetchone()[0]
    cur.execute('DELETE FROM wn_notes WHERE wsid=%s AND time > %s',
                [wsid, '20050530222438'])
    

if __name__ == '__main__':
  unittest.main()

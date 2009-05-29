#!/usr/bin/python

"""An abstraction representing a Note."""

import sys, MySQLdb

from etc.common import *

class Note:
  """An abstraction representing a Note."""
  
  # 'text' must be the last key for printJavascript method
  JSKEYS = ('id', 'xPos', 'yPos', 'height', 'width',
            'bgcolor', 'zIndex', 'text')
  DBKEYS = ('noteid', 'xposition', 'yposition', 'height', 'width',
            'bgcolor', 'zindex', 'text')

  def FromTuple(*args):
    note = Note()
    d = dict(zip(Note.DBKEYS, args))
    note.__dict__.update(d)
    return note
  FromTuple = staticmethod(FromTuple)

  def FromXML(node):
    note = Note()
    for i in range(node.attributes.length):
      attr = node.attributes.item(i)
      if attr.name in Note.DBKEYS: # only use valid attributes
        # remove characters that might cause problems with the db
        setattr(note, attr.name, attr.nodeValue.replace("'", ''))
    note.text = node.firstChild.nodeValue.strip().replace("'", '')
    return note
  FromXML = staticmethod(FromXML)
  
  def getValues(self):
    """Return a list of the keys in db order."""
    return [getattr(self, key) for key in self.DBKEYS]

  def __cmp__(self, rhs):
    return cmp(self.noteid, rhs.noteid)

  def printJavascript(self):
    print "  workspace.createNote( {"
    for js, db in zip(self.JSKEYS, self.DBKEYS)[:-1]:
      print "      '%s': '%s'," % (js, getattr(self, db))
    print "      'text': unescape('%s')" % (self.text)
    print "  }, true);"

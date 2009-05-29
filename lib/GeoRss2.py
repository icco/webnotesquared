
try:
  from lib import PyRSS2Gen
except ImportError:
  import PyRSS2Gen

# this is a better name
StringElement = PyRSS2Gen.IntElement

class GeoRss2(PyRSS2Gen.RSS2):
  rss_attrs = {"version": "2.0",
               "xmlns:geo": "http://www.w3.org/2003/01/geo/wgs84_pos#"}

class GeoRssItem(PyRSS2Gen.RSSItem):
  def __init__(self,
               title = None,  # string
               link = None,   # url as string
               description = None, # string
               author = None,      # email address as string
               categories = None,  # list of string or Category
               comments = None,  # url as string
               enclosure = None, # an Enclosure
               guid = None,    # a unique string
               pubDate = None, # a datetime
               source = None,  # a Source
               extras = {}): # extra tags
    PyRSS2Gen.RSSItem.__init__(self, title, link, description, author,
                               categories, comments, enclosure, guid,
                               pubDate, source)
    self.extraTags = [StringElement(name, value) for name, value 
                      in extras.iteritems() if value]

  def publish_extensions(self, handler):
    for tag in self.extraTags:
      tag.publish(handler)

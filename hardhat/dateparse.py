import dateutil.parser
import datetime

class NotADate(Exception):
  pass

class PartialDate(Exception):
  pass

def dateparse(s):
  # crashes if partial date (good!)
  info=dateutil.parser.parserinfo(dayfirst=True)
  value=dateutil.parser.parser(info)._parse(s)
  if value==None:
    raise NotADate("Could not parse %r"%s)
  d=[value.year, value.month, value.day]
  if d.count(None)>0:
    raise PartialDate("Unable to fully parse date: %r => %r"%(s, value))
  return datetime.date(year=value.year, month=value.month, day=value.day)

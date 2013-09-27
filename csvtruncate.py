import csv, codecs, cStringIO, os
from collections import Counter, OrderedDict
import math

"""
Ensure that no cell in a CSV file contains >32K characters.
"""

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

MAX_SIZE=25000

def dofilevert(filename):
  print filename
  out=open(filename+".out", "w")
  outcsv=UnicodeWriter(out)
  with open(filename, 'r') as f:
    for row in UnicodeReader(f):
        maxlen = max([len(x) for x in row])
        for i in range(0,maxlen,25000):
            if i>0: print i
            reducedrow=[x[i:i+25000] for x in row]
            outcsv.writerow(reducedrow)
  out.close()

def dofilehorz(filename):
    print filename
    out=open(filename.replace(".csv", ".trunc.csv"), "w")
    outcsv=UnicodeWriter(out)
    # do preparse
    with open(filename, 'r') as f:
        for i, row in enumerate(UnicodeReader(f)):
            if i==0:
                header = row
                headers=Counter(row)
                continue
            for c,cell in enumerate(row):
                size = (len(cell)/MAX_SIZE)+1 # integer division is horrid.
                headers[header[c]]=max(headers[header[c]], size)
    # pass 2
    with open(filename, 'r') as f:
        for i, row in enumerate(UnicodeReader(f)):
            if i==0:
                newrow=[]
                for c,cell in enumerate(header):
                    newrow.extend(['%s_%d'%(cell, r) for r in range(headers[cell])])
                outcsv.writerow(newrow)
                continue
            # populate dictionary
            d=OrderedDict()
            for c, cell in enumerate(row):
                for r in range(headers[header[c]]):
                    d["%s_%d"%(header[c],r)]=cell[MAX_SIZE*r:MAX_SIZE*(r+1)]
            outcsv.writerow(d.values())
    out.close()

def dofile(filename):
    dofilehorz(filename)

import sys
csv.field_size_limit(1000000000)
dofile(sys.argv[1])
#for i in os.listdir('http/others'):
  #print i

        



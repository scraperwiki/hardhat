import csv, os
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

def csv_to_dict(csvfile,*args,**kwargs):
    "Turn a csv file into a list of dicts"
    r= csv.reader(csvfile,*args,**kwargs)
    header = [keyify(key) for key in r.next()]
    d = [dict(zip(header,row)) for row in r]
    return d

def _convert_na_string(data, na_string):
    'Convert the NA string in a list of dicts.'
    for row in data:
        for k,v in row.items():
            if v == na_string:
                row[k] = None
    return data

def read_csv(file_or_url, na_strings = "NA"):
    'Like R\'s read.csv'

    # Open the file handle.
    if os.path.exists(file_or_url):
        h = open(file_or_url)
    else:
        h = urlopen(file_or_url)

    d = csv_to_dict(h)

    # Convert NAs to None
    if na_strings != None:
        d = _convert_na_string(data, na_strings)

    return d

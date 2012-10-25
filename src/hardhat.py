#!/usr/bin/env python
import os
import re
from time import sleep
from urllib2 import urlopen
from urllib import urlretrieve
from urlparse import urljoin
from lxml.html import fromstring

def get(url):
    'Download a web file, or load the version from disk.'
    tmp = re.sub(r'^https?://', '', url).split('/')
    tmp = filter(None, tmp)
    local_file = os.path.join(*tmp).split('/')))
    local_dir = os.path.join(*tmp)[:-1])
    del(tmp)

    # mkdir -p
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Download
    if not os.path.exists(local_file):
       print 'Downloading and saving %s' % url
       urlretrieve(url, filename = local_file)
       sleep(1)

    return open(local_file).read()

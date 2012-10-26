#!/usr/bin/env python
import os
import re
from time import sleep
from random import normalvariate

# HTTP
from urllib2 import urlopen
from urllib import urlretrieve
from urlparse import urljoin

# HTML
from lxml.html import fromstring

def get(url, cachedir = '.'):
    'Download a web file, or load the version from disk.'
    tmp1 = re.sub(r'^https?://', '', url)
    tmp2 = [cachedir] + filter(None, tmp1.split('/'))
    local_file = os.path.join(*tmp2)
    local_dir = os.path.join(*tmp2[:-1])
    del(tmp1)
    del(tmp2)

    # mkdir -p
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    # Download
    if not os.path.exists(local_file):
       print 'Downloading and saving %s' % url
       urlretrieve(url, filename = local_file)
       randomsleep(1, 0.5)

    return open(local_file).read()


def randomsleep(mean = 8, sd = 4):
    "Sleep for a random amount of time"
    seconds=normalvariate(mean, sd)
    if seconds>0:
        sleep(seconds)



# Select one node from a css selector or xpath.
from lxml.html import fromstring, HtmlElement
def _one_selector_func(selector_type):
    def _one_selector(self, selector):
        results = getattr(self, selector_type)(selector)
 
        if len(results) != 1:
            msg = 'I expected one match for %s, but I found %d.'
            raise ValueError(msg % (selector, len(results)))
 
        return results[0]
    return _one_selector

HtmlElement.one_xpath = _one_selector_func('xpath')
HtmlElement.one_cssselect = _one_selector_func('cssselect')
del(_one_selector_func)


def digits(text):
    'Extract the digits from the text.'
    return filter(lambda letter: letter in '12534567890', text)

# Postal codes
# http://stackoverflow.com/questions/578406/what-is-the-ultimate-postal-code-and-zip-regex

def chrome_headers(raw_headers):
    '''
Convert Chrome headers to Python's Requests dictionary.
https://gist.github.com/3424623
    '''
    return dict([[h.partition(':')[0], h.partition(':')[2]] for h in raw_headers.split('\n')])

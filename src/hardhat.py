#!/usr/bin/env python
import os
import re
from time import sleep
from random import normalvariate

# Cache
import pickle

# HTTP
from urllib2 import urlopen
from urllib import urlretrieve
from urlparse import urljoin

# HTML
from lxml.html import fromstring, tostring

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

def options(parentnode,ignore_first=False,ignore_value=None,ignore_text=None,textname="text",valuename="value"):
    """
    Provide a list of option nodes. Receive parent of values and text()s.
    The node list can be an lxml nodes or a text representation.
    In either case, all child option tags will be used.

    You may specify that the first node, the node with a particular value or the node with a particular text be ignored.
    """
    if type(parentnode)==str:
        parentnode=fromstring(parentnode)

    if ignore_first!=None:
        nodes=parentnode.xpath('option[position()>1]')
    elif ignore_value!=None:
        nodes=parentnode.xpath('option[@value!="%s"]'%ignore_value)
    elif ignore_text!=None:
        nodes=parentnode.xpath('option[text()!="%s"]'%ignore_text)
    else:
        nodes=parentnode.xpath('option')

    return [{textname:node.text,valuename:node.xpath('attribute::value')[0]} for node in nodes]

def get_select_value(node):
    # node is an LXML element (SELECT tag)
    try:
        return node.cssselect("option[selected='selected']")[0].text
    except IndexError:
        return node.cssselect("option")[0].text

def htmltable2matrix(tablehtml,cell_xpath=None):
    """
    Takes an html table or an lxml tree whose current node is the table of interest

    Optionally takes an xpath to be applied at the cell level
    """
    if type(tablehtml) in [str, unicode]:
        tablehtml=fromstring(tablehtml)
    trs=tablehtml.cssselect('tr')
    tablematrix=[]
    for tr in trs:
        tablematrix_row=[]
        tds=tr.cssselect('td')
        for td in tds:
            #If it has a colspan attribute, repeat that many times
            if 'colspan' in [key.lower() for key in td.attrib.keys()]:
                repeats=int(td.attrib['colspan'])
            else:
                repeats=1

            for r in range(repeats):
                if cell_xpath==None:
                    cell=td.text_content()
                else:
                    cell=''.join(td.xpath(cell_xpath))
                tablematrix_row.append(cell)

        tablematrix.append(tablematrix_row)

    return tablematrix


def save(key, value, cache_dir = os.path.expanduser(os.path.join('~', '.cache'))):
    'Save an object to the cache_dir.'
    cache_path = os.path.join(cache_dir, key + '.p')
    cache_file = open(cache_path, 'wb')
    pickle.dump(value, cache_file)
    cache_file.close()

def load(key, cache_dir = os.path.expanduser(os.path.join('~', '.cache'))):
    'Load an object from the cache_dir.'
    cache_path = os.path.join(cache_dir, key + '.p')
    if os.path.exists(cache_path):
        cache_file = open(cache_path, 'rb')
        data = pickle.load(cache_file)
        cache_file.close()
    else:
        raise KeyError(key)
    return data

def cache(key, func, cache_dir = os.path.expanduser(os.path.join('~', '.cache'))):
    '''
    Check if a value is in the cache.
    Load and cache it from the function if it isn\'t already cached.
    '''
    cache_path = os.path.join(cache_dir, key + '.p')

    if os.path.exists(cache_path):
        data = load(key, cache_dir = cache_dir)
    else:
        # Run the function
        data = func()

        # Cache
        save(key, data, cache_dir = cache_dir)

    return data

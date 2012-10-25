#!/usr/bin/env python
'''
USPS Address Lookup client
'''

from urllib2 import urlopen, URLError
from urllib import urlencode
from lxml.html import fromstring

ADDRESS_LOOKUP_URL = 'https://tools.usps.com/go/ZipLookupResultsAction!input.action?'

def _parse(text):
    'Give html text from the web page, extract the list of addresses.'

    if '''<li class="error">Unfortunately, this address wasn't found.</li>''' in text and \
        '''<li class="error">Please double-check it and try again.</li>''' in text:
        return []

    elif 'The address you provided is not recognized by the US Postal Service as an address we serve. Mail sent to this address may be returned.' in text:
        return []

    resultstart = '<div id="results-content" class="cap-middle">'
    text = resultstart + text.split(resultstart)[1].split('<div id="result-bottom" class="result-bottom">')[0].replace('&trade;', '')
    html = fromstring(text)
    out = []
    for std_address in html.cssselect('#result-list p.std-address'):
        spans = std_address.xpath('span[@class != "address1 range" and @class != "hyphen"]')
        outaddress = {unicode(span.attrib['class'].replace(' range', '')): unicode(span.text) for span in spans}

        addresses1 = std_address.xpath('span[@class="address1 range"]')
        outaddress[u'address1'] = addresses1[-1].text
        if len(addresses1) == 2:
            outaddress[u'name'] = addresses1[0].text

        if outaddress[u'zip4'] == 'None':
            outaddress[u'zip4'] = None

        # Strip padding
        for k, v in outaddress.items():
            outaddress[k] = v.strip()

        out.append(outaddress)

    return out

def lookup(address1, address2, city, state, zipcode):
    'Look up an address, and return the usps version.'
    address = {
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "resultMode": 0,
        "companyName": "",
        "urbanCode": "",
        "postalCode": "",
    }
    url = ADDRESS_LOOKUP_URL + urlencode(address)

    try:
        handle = urlopen(url)
    except:
        print url
        raise

    return _parse(handle.read())

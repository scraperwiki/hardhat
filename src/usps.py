#!/usr/bin/env python
'''
USPS Address Lookup client
'''

from urllib2 import urlopen, URLError
from urllib import urlencode
from lxml.html import fromstring

ADDRESS_LOOKUP_URL = 'https://tools.usps.com/go/ZipLookupResultsAction!input.action?'
EXPECTED_KEYS = {'address1', 'address2', 'city', 'state', 'zip'}

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

def contains_address(db, address):
    params = [address[u'Street Address'], address[u'Hash'], address[u'City'], address[u'State'], address[u'Zip Code']]
    count = db.execute('''
select count(*) from usps
WHERE [Street Address]= ?
  AND Hash = ?
  AND City = ?
  AND State = ?
  AND [Zip Code] = ?
''', params)[0]['count(*)']
    return count > 0

def check_and_format(address):
    '''
    `address` is a dictionary of the paramaters.
    Validated it, then add the paramaters that are necessary for
    the call to the USPS page.
    '''

    # Hack to deal with legacy code
    address = {k: [v] for k, v in address.items()}

    # Dunno why they come as lists
    for k, v in address.items():
        address[k] = v[0]

    if set(address.keys()) == {'address1', 'city', 'state', 'zip'}:
        address['address2'] = ''

    if set(address.keys()) == EXPECTED_KEYS:
        address.update({
            "resultMode": 0,
            "companyName": "",
            "urbanCode": "",
            "postalCode": "",
        })
    else:
        raise ValueError(
            'Your request has these extra keys: %s. '
            'Your request is missing these keys: %s' % (
                set(address.keys()).difference(EXPECTED_KEYS),
                EXPECTED_KEYS.difference(set(address.keys()))
            )
        )
    return address

def do_request(address):
    '''
    `address` is a dictionary of paramaters for the USPS request.
    Make the request, parse the output and return the json that
    will be printed.
    '''

    url = ADDRESS_LOOKUP_URL + urlencode(address)
    output = {'url': url, 'addresses': []}
    while True:
        try:
            handle = urlopen(url)
        except URLError:
            randomsleep()
        else:
            text = handle.read()
            break


    return output

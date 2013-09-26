import re
import hashlib


def rep(char):
    if re.match(r"^[0-9A-Za-z]$", char):
        return char
    else:
        percent = "%%%02x" % ord(char)  # %% -> literal %
        return percent.upper()


def gethash(url):
    h = hashlib.sha1(url).hexdigest()
    return "-" + h


def goodstub(url):
    assert type(url) == str  # i.e. NOT UNICODE
    chars = list(url)
    stub = ''.join(rep(char) for char in chars)
    return stub[:200] + gethash(url)

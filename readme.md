Hard Hat
========
These are helpers for general data cleaning and for some specific webby cleaning stuff.

Functions

* `get(url)`: Make a get request for a url and cache it,
    or load it from a cache if it has already been downloaded.
* `randomsleep(mean = 8, sd = 4)`: Sleep for a normal-random
    number of seconds.
* `fromstring` and `HtmlElement`: These are extended versions of the
    respective components of `lxml.html` that provide two extra functions:
  * `HtmlElement.one_xpath`: Select one node based on an xpath; return
      an error if multiple or no nodes match this xpath.
  * `HtmlElement.one_cssselect` Select one node based on a css selector;
      return an error if multiple or no nodes match this xpath.

## Running tests

    source activate
    nosetests

import os
import nose.tools as n

import usps

class TestParse:
    def _(self, fixture, expected):
        observed = usps._parse(open(self._fixture(fixture)).read())
        n.assert_list_equal(observed, expected)

    @staticmethod
    def _fixture(filename):
        return os.path.join('fixtures', 'usps', filename)

    def test_multiple_results(self):
        self._('ZipLookupResultsAction!input.action?city=Washington&zip=20500&companyName=&address1=1600+Pennsylvania+Avenue+NW&address2=&postalCode=&state=DC&resultMode=0&urbanCode=', [{"city": "WASHINGTON ", "state": "DC", "address1": "1600 PENNSYLVANIA AVE NW", "zip": "20500", "zip4": "0003"}, {"city": "WASHINGTON ", "name": "WHITE HOUSE", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0003"}, {"city": "WASHINGTON ", "name": "PRESIDENT", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0001"}, {"city": "WASHINGTON ", "name": "FIRST LADY", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0002"}, {"city": "WASHINGTON ", "name": "THE WHITE HOUSE", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0004"}, {"city": "WASHINGTON ", "state": "DC", "address1": "1600 PENNSYLVANIA AVE NW", "zip": "20500", "zip4": "0005"}, {"city": "WASHINGTON ", "name": "GREETINGS OFFICE", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0039"}, {"city": "WASHINGTON ", "name": "WHITE HOUSE STATION", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "0049"}, {"city": "WASHINGTON ", "name": "AMER FUND FOR AFGHAN CHILD", "zip": "20500", "address1": "1600 PENNSYLVANIA AVE NW", "state": "DC", "zip4": "1600"}])

#   def test_no_results(self):
#       self._('', [])

    def test_one_result(self):
        self._('ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=19+Bayhill+RD&address2=&city=Dellwood&state=MN&urbanCode=&postalCode=&zip=55110', [{
            u'address1': '19 BAYHILL RD',
            u'address2': '',
            u'city': 'DELLWOOD',
            u'state': 'MN',
            u'zip': '55110',
            u'zip4': '6178',
        }])

#   def test_not_found(self):
        

    def test_not_recognized(self):
        with n.assert_raises(ValueError):
            usps._parse(self._fixture('ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=26130+Birch+AVE&address2=&city=Ni%0Asswa&state=MN&urbanCode=&postalCode=&zip=56468'))

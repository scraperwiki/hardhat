import usps

class TestParse:
    def _(self, fixture, expected):
        path = os.path.join('fixtures', 'usps', fixture)
        observed = usps._parse(open(path).read())
        n.assert_list_equal(observed, expected)

    def test_multiple_results(self):
        self._('', [{
            u'address1': '',
            u'address2': '',
            u'city': '',
            u'state': '',
            u'zip': '',
        },{
            u'address1': '',
            u'address2': '',
            u'city': '',
            u'state': '',
            u'zip': '',
        }])

    def test_no_results(self):
        self._('', [])

    def test_one_result(self):
        self._('ZipLookupResultsAction!input.action?resultMode=0&companyName=&address1=19+Bayhill+RD&address2=&city=Dellwood&state=MN&urbanCode=&postalCode=&zip=55110', {
            u'address1': '',
            u'address2': '',
            u'city': '',
            u'state': '',
            u'zip': '',
        })

    def test_not_found(self):

    def test_not_recognized(self):

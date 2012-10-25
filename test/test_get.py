import nose.tools as n
import hardhat

def test_get():
    observed = hardhat.get('http://not.a.domain/stuff.html', cachedir = 'fixtures')
    expected = 'This is not a website.\n'
    n.assert_equal(observed, expected)

from lxml.html import fromstring
import nose.tools as n

def test():
    observed1=options(fromstring("""<option value="1">Macaroni</option><option value="2">Cheese</option>"""),textname="text",valuename="text")
    expected1=[{"text":"Macaroni","value":"1"},{"text":"Cheese","value":"2"}]
    n.assert_list_equal(observed1, expected1)

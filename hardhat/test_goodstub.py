import unittest
import hashlib
from goodstub import goodstub, gethash

testcases = [["http://www.google.com", "http%3A%2F%2Fwww%2Egoogle%2Ecom"],
             ["123-456 789", "123%2D456%20789"],
             ["x"*300, "x"*200+"-"+hashlib.sha1("x"*300).hexdigest()]]


class TestStubs(unittest.TestCase):
    def test_stub(self):
        for test in testcases:
            if "-" not in test[1]:
                test[1] = test[1] + gethash(test[0])
            assert goodstub(test[0]) == test[1], \
                (test[0], test[1], goodstub(test[0]))
            assert len(test[1]) < 255, \
                len(test[1])

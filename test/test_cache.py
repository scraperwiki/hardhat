import os
import nose.tools as n
import tempfile

import hardhat

class TestCache():
    @classmethod
    def setup_class(self):
        self.cache_dir = tempfile.mkdtemp()
        self.test_path = os.path.join(self.cache_dir, 'test_file')

    def setup(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_save(self):
        n.assert_equal(3, hardhat.cache('test_file', lambda: 3))

    def test_save_and_load(self):
        n.assert_equal(3, hardhat.cache('test_file', lambda: 3))
        n.assert_equal(3, hardhat.cache('test_file', lambda: 4))

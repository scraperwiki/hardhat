import os
import nose.tools as n
import tempfile

import hardhat

class TestCache():
    @classmethod
    def setup_class(self):
        self.cache_dir = tempfile.mkdtemp()
        self.test_path = os.path.join(self.cache_dir, 'test_file.p')

    @classmethod
    def teardown_class(self):
        os.removedirs(self.cache_dir)

    def setup(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)
    teardown = setup

    def test_save(self):
        n.assert_equal(3, hardhat.cache('test_file', lambda: 3, cache_dir = self.cache_dir))
        n.assert_true(os.path.exists(self.test_path))

    def test_save_and_load(self):
        n.assert_equal(3, hardhat.cache('test_file', lambda: 3, cache_dir = self.cache_dir))
        n.assert_equal(3, hardhat.cache('test_file', lambda: 4, cache_dir = self.cache_dir))

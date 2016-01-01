import os
import cmplync
import unittest
import tempfile

class CmplyncTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, cmplync.app.config['DATABASE'] = tempfile.mkstemp()
        cmplync.app.config['TESTING'] = True
        self.app = cmplync.app.test_client()
#        cmplync.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(cmplync.app.config['DATABASE'])

    def test_root(self):
        rv = self.app.get('/')
        assert 'hello' in rv.data

if __name__ == '__main__':
    unittest.main()

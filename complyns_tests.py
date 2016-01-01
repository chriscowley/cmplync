import os
import complyns
import unittest
import tempfile

class ComplyncTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, complyns.app.config['DATABASE'] = tempfile.mkstemp()
        complyns.app.config['TESTING'] = True
        self.app = complyns.app.test_client()
#        complyns.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(complyns.app.config['DATABASE'])

    def test_root(self):
        rv = self.app.get('/')
        assert 'hello' in rv.data

if __name__ == '__main__':
    unittest.main()

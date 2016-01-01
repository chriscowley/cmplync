import os
import cmplync
import unittest
import tempfile

package_data = {
    "fqdn": "paul.chriscowley.lan",
    "package_arch": "i686",
    "package_name": "sqlite",
    "version_available": "3.9.2-1.fc23",
    "version_installed": "3.9.0-1.fc23"
}


class CmplyncTestCase(unittest.TestCase):

    def setUp(self):

        self.db_fd, cmplync.app.config['DATABASE'] = tempfile.mkstemp()
        print(cmplync.app.config['DATABASE'])
        cmplync.app.config['TESTING'] = True
        cmplync.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + cmplync.app.config['DATABASE']
        self.app = cmplync.app.test_client()
        cmplync.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(cmplync.app.config['DATABASE'])

    def test_root(self):
        rv = self.app.get('/')
        assert 'hello' in rv.data

if __name__ == '__main__':
    unittest.main()

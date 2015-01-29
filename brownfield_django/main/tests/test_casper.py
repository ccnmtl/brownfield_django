from casper.tests import CasperTestCase
import os.path

class MyTest(CasperTestCase):
    def test_something(self):
        self.assertTrue(self.casper(
            os.path.join(os.path.dirname(__file__),
                'media/js/tests/tests.js')))
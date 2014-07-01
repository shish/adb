from pyramid import testing

from adbweb.tests import AdbWebTest
from adbweb.views import index


class TestIndex(AdbWebTest):
    def test(self):
        request = testing.DummyRequest()
        info = index(request)
        #self.assertEqual(info, {})

from pyramid import testing
from pyramid.exceptions import NotFound

from adbweb.models import User
from adbweb.tests import AdbWebTest
from adbweb.views import session_create, session_delete


class TestSessionCreate(AdbWebTest):
    def test_pass(self):
        request = testing.DummyRequest(json_body={"username": u"test", "password": u"test"})
        resp = session_create(request)
        self.assertEqual(resp.status, "ok")

    def test_fail(self):
        request = testing.DummyRequest(json_body={"username": u"test", "password": u"arrr"})
        resp = session_create(request)
        self.assertEqual(resp.status, "error")


class TestSessionDelete(AdbWebTest):
    def test_pass(self):
        request = testing.DummyRequest()
        request.user = User.by_username("shish")
        resp = session_delete(request)
        self.assertEqual(resp.status, "ok")

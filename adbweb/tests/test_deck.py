from pyramid import testing
from pyramid.exceptions import NotFound

from adbweb.tests import AdbWebTest
from adbweb.views import deck_list, deck_create, deck_read, deck_delete


class TestDeckList(AdbWebTest):
    def test(self):
        request = testing.DummyRequest()
        response = deck_list(request)
        self.assertEqual(response[0].title, 'Test Deck')


class TestDeckCreate(AdbWebTest):
    def test(self):
        request = testing.DummyRequest(user=self.user, json_body={
            "title": u"A new deck",
        })
        resp = deck_create(request)
        self.assertEqual(resp.status, "ok")

        request = testing.DummyRequest(matchdict={"deck_id": resp.deck_id})
        response = deck_read(request)
        self.assertEqual(response.deck.title, u"A new deck")


class TestDeckRead(AdbWebTest):
    def test_pass(self):
        request = testing.DummyRequest(matchdict={"deck_id": "1"})
        response = deck_read(request)
        self.assertEqual(response.deck.title, "Test Deck")

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"deck_id": "9999"})
        self.assertRaises(NotFound, deck_read, request)


class TestDeckDelete(AdbWebTest):
    def test_pass(self):
        request = testing.DummyRequest(user=self.user, json_body={
            "title": u"A new deck",
        })
        resp = deck_create(request)
        self.assertEqual(resp.status, "ok")
        self.assertIsNotNone(resp.deck_id)

        request = testing.DummyRequest(matchdict={"deck_id": resp.deck_id})
        resp2 = deck_delete(request)
        self.assertEqual(resp2.status, "ok")

        request = testing.DummyRequest(matchdict={"deck_id": resp.deck_id})
        self.assertRaises(NotFound, deck_read, request)

    def test_fail(self):
        request = testing.DummyRequest(matchdict={"deck_id": "9999"})
        self.assertRaises(NotFound, deck_delete, request)

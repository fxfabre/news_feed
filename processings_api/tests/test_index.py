from unittest import TestCase

from starlette.testclient import TestClient

from src.fastapi_app import app


class TestIndex(TestCase):
    def test_docs_redirect(self) -> None:
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.history[0].status_code, 302)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.url, "http://testserver/docs")

from __future__ import annotations

from unittest import TestCase

from starlette.testclient import TestClient

from src.fastapi_app import app


class TestHealthcheck(TestCase):
    def test_status_healthy(self) -> None:
        client = TestClient(app)
        response = client.get("/healthcheck")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Healthy")

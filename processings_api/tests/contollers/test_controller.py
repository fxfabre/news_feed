from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock, patch

from starlette.testclient import TestClient

from src.fastapi_app import app


class TestController(TestCase):
    @patch(
        "src.models.custom_model.{function_name}",
        MagicMock(return_value="function response data"),
    )
    def test_good_data(self) -> None:
        client = TestClient(app)
        response = client.get("/api/v1/endpoint")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "expected result")

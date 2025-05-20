from typing import Any

from pythonjsonlogger.json import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, rename_fields=self._rename_fields, **kwargs)

    @property
    def _rename_fields(self) -> dict[str, str]:
        return {
            "name": "source",
            "levelname": "severity",
        }

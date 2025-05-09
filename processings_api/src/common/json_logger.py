from typing import Any
from typing import Dict

from pythonjsonlogger.json import JsonFormatter


class CustomJsonFormatter(JsonFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, rename_fields=self._rename_fields, **kwargs)

    @property
    def _rename_fields(self) -> Dict[str, str]:
        return {
            # "asctime": "Date",
            # "thread": "Thread",
            # "module": "Logger",
            "name": "source",
            "levelname": "severity",
            # "message": "message",
        }

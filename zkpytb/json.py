"""
Helper functions related to json

Author: Marc Gallet
"""


import datetime
import decimal
import json
import uuid
import pathlib


class JSONEncoder(json.JSONEncoder):
    """
    A custom JSONEncoder that can handle a bit more data types than the one from stdlib.
    """
    def default(self, o):
        # early passthrough if it works by default
        try:
            return json.JSONEncoder.default(self, o)
        except Exception:
            pass
        # handle Path objects
        if isinstance(o, pathlib.Path):
            return str(o).replace('\\', '/')
        # handle UUID objects
        if isinstance(o, uuid.UUID):
            return str(o)
        if isinstance(o, (datetime.datetime, datetime.time, datetime.date)):
            return o.isoformat()
        if isinstance(o, datetime.timedelta):
            return o.total_seconds()
        if isinstance(o, (complex, decimal.Decimal)):
            return str(o)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, o)

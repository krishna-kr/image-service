from decimal import Decimal
from typing import Any


def json_safe(value: Any):
    """
    Recursively converts Decimal values to int or float
    so the object becomes JSON serializable.
    """
    if isinstance(value, Decimal):
        # Convert to int if possible, else float
        if value % 1 == 0:
            return int(value)
        return float(value)

    if isinstance(value, list):
        return [json_safe(v) for v in value]

    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}

    return value

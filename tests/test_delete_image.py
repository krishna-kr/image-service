import json
from src.handlers.delete_image import lambda_handler


def test_delete_image_idempotent():
    event = {
        "pathParameters": {
            "user_id": "unknown",
            "image_id": "already-deleted",
        }
    }

    response = lambda_handler(event, None)
    assert response["statusCode"] in (200, 404)

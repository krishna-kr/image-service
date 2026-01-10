import json
from src.handlers.download_image import lambda_handler


def test_download_image_not_found():
    event = {
        "pathParameters": {
            "user_id": "unknown",
            "image_id": "invalid-id",
        }
    }

    response = lambda_handler(event, None)
    assert response["statusCode"] == 404

import json
import base64
from src.handlers.upload_image import lambda_handler


def test_upload_image_success():
    payload = {
        "user_id": "test-user",
        "file_name": "hello.txt",
        "content_type": "text/plain",
        "image_base64": base64.b64encode(b"hello world").decode(),
    }

    event = {"body": json.dumps(payload)}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert "image_id" in body


def test_upload_image_missing_field():
    event = {"body": json.dumps({"user_id": "test-user"})}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 400

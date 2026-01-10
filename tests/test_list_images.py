import json
from src.handlers.list_images import lambda_handler


def test_list_images_missing_user():
    event = {"queryStringParameters": {}}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 400


def test_list_images_empty():
    event = {"queryStringParameters": {"user_id": "non-existing"}}
    response = lambda_handler(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["count"] == 0

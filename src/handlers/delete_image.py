import json

from src.services.dynamodb_service import (
    get_image_metadata,
    delete_image_metadata,
)
from src.services.s3_service import delete_object


def lambda_handler(event, context):
    path_params = event.get("pathParameters") or {}

    user_id = path_params.get("user_id")
    image_id = path_params.get("image_id")

    if not user_id or not image_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing path parameters: user_id or image_id"
            })
        }

    item = get_image_metadata(user_id, image_id)

    # Idempotency: if not found, return success or 404 (design choice)
    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "message": "Image already deleted or does not exist"
            })
        }

    # Delete from S3
    delete_object(item["s3_key"])

    # Delete metadata from DynamoDB
    delete_image_metadata(user_id, image_id)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Image deleted successfully",
            "image_id": image_id
        })
    }

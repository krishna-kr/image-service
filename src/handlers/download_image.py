import json
from src.services.dynamodb_service import get_image_metadata
from src.services.s3_service import generate_download_url
from src.utils.json_utils import json_safe


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

    if not item:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Image not found"
            })
        }

    download_url = generate_download_url(item["s3_key"])

    return {
        "statusCode": 200,
        "body": json.dumps(json_safe({
            "image_id": image_id,
            "download_url": download_url
        }))
    }

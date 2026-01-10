import json
from src.services.dynamodb_service import query_images_by_user
from src.utils.json_utils import json_safe


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters") or {}
    user_id = query_params.get("user_id")

    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required query parameter: user_id"
            })
        }

    items = query_images_by_user(user_id)

    items.sort(
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "count": len(items),
            "items": json_safe(items)
        })
    }

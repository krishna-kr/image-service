import json
from src.services.dynamodb_service import query_images_by_user_paginated
from src.utils.json_utils import json_safe


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters") or {}

    user_id = query_params.get("user_id")
    limit = int(query_params.get("limit", 10))
    cursor = query_params.get("cursor")
    from_date = query_params.get("from_date")
    to_date = query_params.get("to_date")

    if not user_id:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required query parameter: user_id"
            })
        }

    last_evaluated_key = json.loads(cursor) if cursor else None

    result = query_images_by_user_paginated(
        user_id=user_id,
        limit=limit,
        last_evaluated_key=last_evaluated_key,
        from_date=from_date,
        to_date=to_date,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(json_safe({
            "count": len(result["items"]),
            "items": result["items"],
            "next_cursor": result["last_evaluated_key"],
        }))
    }

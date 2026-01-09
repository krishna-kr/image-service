import base64
import json
import uuid
from datetime import datetime

from src.services.s3_service import upload_object
from src.services.dynamodb_service import put_item


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        user_id = body["user_id"]
        file_name = body["file_name"]
        content_type = body["content_type"]
        image_base64 = body["image_base64"]

        image_bytes = base64.b64decode(image_base64)

        image_id = str(uuid.uuid4())
        s3_key = f"{user_id}/{image_id}/{file_name}"

        # Upload to S3
        upload_object(
            key=s3_key,
            content=image_bytes,
            content_type=content_type
        )

        # Store metadata in DynamoDB
        item = {
            "PK": f"USER#{user_id}",
            "SK": f"IMAGE#{image_id}",
            "user_id": user_id,
            "image_id": image_id,
            "file_name": file_name,
            "content_type": content_type,
            "size_bytes": len(image_bytes),
            "s3_key": s3_key,
            "created_at": datetime.utcnow().isoformat()
        }

        put_item(item)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Image uploaded successfully",
                "image_id": image_id
            })
        }

    except KeyError as exc:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Missing field: {str(exc)}"
            })
        }

    except Exception as exc:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(exc)
            })
        }

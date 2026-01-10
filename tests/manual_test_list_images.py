import json
from src.handlers.list_images import lambda_handler

event = {
    "queryStringParameters": {
        "user_id": "user-1"
    }
}

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))

import json
from src.handlers.download_image import lambda_handler

# Replace with actual IDs from list API output
event = {
    "pathParameters": {
        "user_id": "user-1",
        "image_id": "5b04bfbe-7270-4893-b504-59b1d06983a5"
    }
}

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))

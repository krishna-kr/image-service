import json
import base64

from src.handlers.upload_image import lambda_handler

image_content = b"hello image service"

event = {
    "body": json.dumps({
        "user_id": "user-1",
        "file_name": "test.txt",
        "content_type": "text/plain",
        "image_base64": base64.b64encode(image_content).decode()
    })
}

response = lambda_handler(event, None)
print(response)

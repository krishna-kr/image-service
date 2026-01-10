import os
import boto3
from typing import Dict, Any

DYNAMODB_ENDPOINT = os.getenv(
    "DYNAMODB_ENDPOINT",
    "http://localhost:4566"
)

TABLE_NAME = os.getenv(
    "IMAGES_TABLE_NAME",
    "images_metadata"
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=DYNAMODB_ENDPOINT,
    region_name="us-east-1"
)

table = dynamodb.Table(TABLE_NAME)


def put_item(item: Dict[str, Any]) -> None:
    table.put_item(Item=item)


def get_item(pk: str, sk: str) -> Dict[str, Any] | None:
    response = table.get_item(
        Key={
            "PK": pk,
            "SK": sk
        }
    )
    return response.get("Item")


def query_images_by_user(user_id: str):
    response = table.query(
        KeyConditionExpression="PK = :pk AND begins_with(SK, :sk)",
        ExpressionAttributeValues={
            ":pk": f"USER#{user_id}",
            ":sk": "IMAGE#"
        }
    )
    return response.get("Items", [])

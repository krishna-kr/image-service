import os
import boto3
from typing import Dict, Any, Optional

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


def get_image_metadata(user_id: str, image_id: str):
    return get_item(
        pk=f"USER#{user_id}",
        sk=f"IMAGE#{image_id}"
    )


def delete_image_metadata(user_id: str, image_id: str) -> None:
    table.delete_item(
        Key={
            "PK": f"USER#{user_id}",
            "SK": f"IMAGE#{image_id}"
        }
    )


def query_images_by_user_paginated(
    user_id: str,
    limit: int = 10,
    last_evaluated_key: Optional[Dict[str, Any]] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
):
    key_condition = "PK = :pk AND begins_with(SK, :sk)"

    expression_values = {
        ":pk": f"USER#{user_id}",
        ":sk": "IMAGE#",
    }

    filter_expression = []
    if from_date:
        filter_expression.append("created_at >= :from_date")
        expression_values[":from_date"] = from_date

    if to_date:
        filter_expression.append("created_at <= :to_date")
        expression_values[":to_date"] = to_date

    query_kwargs = {
        "KeyConditionExpression": key_condition,
        "ExpressionAttributeValues": expression_values,
        "Limit": limit,
    }

    if filter_expression:
        query_kwargs["FilterExpression"] = " AND ".join(filter_expression)

    if last_evaluated_key:
        query_kwargs["ExclusiveStartKey"] = last_evaluated_key

    response = table.query(**query_kwargs)

    return {
        "items": response.get("Items", []),
        "last_evaluated_key": response.get("LastEvaluatedKey"),
    }
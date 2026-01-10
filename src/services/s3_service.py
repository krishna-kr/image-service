import os
import boto3

S3_ENDPOINT = os.getenv(
    "S3_ENDPOINT",
    "http://localhost:4566"
)

S3_BUCKET_NAME = os.getenv(
    "IMAGES_BUCKET_NAME",
    "image-bucket"
)

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    region_name="us-east-1"
)


def upload_object(
    key: str,
    content: bytes,
    content_type: str
) -> None:
    """
    Uploads an object to S3.
    """
    s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=content,
        ContentType=content_type
    )


def generate_download_url(key: str, expires_in: int = 3600) -> str:
    """
    Generates a presigned URL for downloading an object.
    """
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": S3_BUCKET_NAME,
            "Key": key
        },
        ExpiresIn=expires_in
    )


def delete_object(key: str) -> None:
    """
    Deletes an object from S3.
    """
    s3_client.delete_object(
        Bucket=S3_BUCKET_NAME,
        Key=key
    )

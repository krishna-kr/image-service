from src.services.s3_service import upload_object

upload_object(
    key="test/hello.txt",
    content=b"hello localstack",
    content_type="text/plain"
)

print("Upload successful")

# Image Service (Serverless)

A serverless backend service for uploading, listing, downloading, and deleting images.
Built using AWS serverless architecture and fully runnable locally using LocalStack.

---

## 🚀 Features

- Upload image with metadata
- List images with pagination & filters
- Download images using presigned URLs
- Delete images (idempotent)
- Local AWS emulation using Docker + LocalStack
- Unit tests using pytest

---

## 🏗️ Architecture

Client
|
API Gateway
|
AWS Lambda (Python)
|
├── S3 (image storage)
└── DynamoDB (image metadata)



### Request Flow
1. Client sends HTTP request
2. API Gateway routes request to Lambda
3. Lambda performs business logic
4. Metadata stored in DynamoDB
5. Image stored in S3
6. Responses returned via API Gateway


## 📈 Scaling to Millions of Users

### Horizontal Scalability
- **API Gateway** auto-scales with traffic
- **Lambda** scales automatically with concurrency
- **DynamoDB** partitions data by user (PK)
- **S3** scales infinitely

### Performance Optimizations
- Cursor-based pagination (`LastEvaluatedKey`)
- No DynamoDB scans
- Stateless Lambda functions
- Idempotent delete operations


## 🧪 Local Development Setup

### Prerequisites
- Python 3.11
- Docker
- AWS CLI

### Start Local AWS Services
```bash
docker compose up -d

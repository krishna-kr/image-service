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

---

## 🧠 Why This Architecture?

### AWS Lambda
- Stateless compute
- Auto-scaling
- Pay-per-use
- Ideal for event-driven APIs

### Amazon S3
- Designed for large binary objects
- Virtually unlimited storage
- Highly durable and cost-effective

### Amazon DynamoDB
- Key-value access pattern
- Single-digit millisecond latency
- Horizontally scalable
- No schema migrations

### API Gateway
- HTTP interface
- Built-in throttling
- Easy Lambda integration

---

## 🗂️ Project Structure

image-service/
├── src/
│ ├── handlers/ # Lambda entry points (API logic)
│ ├── services/ # AWS integrations (S3, DynamoDB)
│ ├── models/ # Data validation & schemas
│ ├── utils/ # Shared utilities (JSON helpers, etc.)
│
├── tests/ # Unit tests (pytest)
│
├── docker-compose.yml
├── requirements.txt
├── README.md


### Why this structure?
- Clear separation of concerns
- Easy testing
- Easy to extend
- Matches real-world backend projects

---

## 🧠 Design Decisions & Trade-offs

### Why DynamoDB instead of SQL?
- Access pattern is key-based (by user)
- No complex joins required
- Scales horizontally without sharding
- Lower operational overhead

**Trade-off:**  
No joins or complex queries — but acceptable for this use case.

---

### Why store images in S3 instead of a database?
- Databases are inefficient for large blobs
- S3 is cheaper, faster, and purpose-built
- Independent scaling of metadata vs binary data

---

### Why presigned URLs for downloads?
- Avoids streaming binary data through Lambda
- Reduces Lambda execution time and cost
- Improves performance and scalability

---

### Why base64 uploads?
- API Gateway encodes binary payloads as base64
- Matches real AWS behavior
- Keeps Lambda logic realistic

---

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

### Future Enhancements
- Global Secondary Indexes (GSI) for advanced filtering
- CloudFront CDN for image delivery
- S3 lifecycle policies for cost optimization

---

## 🔐 Security Considerations

- Private S3 bucket (no public access)
- Presigned URLs with expiration
- Input validation in handlers
- IAM least-privilege principle (in real AWS)
- No secrets committed to GitHub

---

## 🧪 Local Development Setup

### Prerequisites
- Python 3.11
- Docker
- AWS CLI

### Start Local AWS Services
```bash
docker compose up -d

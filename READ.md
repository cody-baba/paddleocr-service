# PaddleOCR FastAPI Service

This repo wraps PaddleOCR in a FastAPI server for easy integration with n8n.

## Run locally
```bash
docker build -t paddleocr-service .
docker run -p 8000:8000 paddleocr-service

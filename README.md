# ACME Product Importer

A scalable web application for importing large CSV files (up to 500,000 products) into a SQL database with real-time progress tracking and product management.

## Features

- CSV Upload with real-time progress tracking
- Product Management with CRUD operations, filtering and pagination
- Bulk delete operations with confirmation dialogs
- Webhook configuration and testing
- Async processing with Celery for large files
- SKU-based upsert (automatic overwrite of duplicates)
- Handles 500K records in ~60-120 seconds with batch processing

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Async Processing: Celery with Redis
- Frontend: HTML/CSS/JavaScript
- Database: PostgreSQL

## Quick Start

### 1. Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create `.env` file in project root:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/acme_products
CELERY_BROKER_URL=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0
```

### 3. Setup Database
```bash
# Create tables
python backend/app/create_tables.py
```

### 4. Start Services
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A backend.app.celery_app worker --loglevel=info

# Terminal 3: Start FastAPI Server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access Application
- Main App: Open `frontend/app.html` in browser
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## CSV Format

```csv
sku,name,description,price
ABC123,Widget Pro,High-quality widget,29.99
XYZ789,Gadget Plus,Premium gadget,49.99
```

## API Endpoints

### Products
- `GET /products/` - List products with filtering and pagination
- `POST /products/` - Create new product (rejects duplicates)
- `POST /products/upsert` - Create or update product based on SKU
- `GET /products/{id}` - Get single product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product
- `DELETE /products/all?confirm=true` - Bulk delete all products

### File Upload
- `POST /upload/` - Upload CSV file for processing
- `GET /tasks/{task_id}` - Get upload progress status

## Performance

- Throughput: ~4,000-8,000 products/second
- Memory optimized with 1000-record batches
- Real-time progress updates every 300ms

## Architecture

### Backend Structure
```
backend/app/
├── main.py              # FastAPI application
├── models.py            # SQLAlchemy models 
├── schemas.py           # Pydantic schemas
├── routes_products.py   # Product CRUD endpoints
├── routes_upload.py     # File upload endpoint
├── routes_task.py       # Task status endpoint
├── tasks.py             # Celery tasks
├── db.py                # Database connection
├── utils.py             # Utility functions
└── celery_app.py        # Celery configuration
```

### Frontend Structure
```
frontend/
├── app.html             # Complete web application

```

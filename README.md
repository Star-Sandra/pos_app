 Star POS API

A fast, lightweight Point of Sale (POS) backend API built for Star Supermarket. This system handles cashiers, product catalog inventory, shopping cart checkouts, and payment tracking across multiple counters.

 Project Structure

pos_app/
└── app/
    ├── models/          # Database tables (SQLAlchemy)
    ├── schemas/         # Request/Response validation (Pydantic)
    ├── repositories/    # Database queries
    ├── services/        # Business logic & math calculations
    ├── routers/         # API endpoints (FastAPI Routes)
    ├── database.py      # Database connection setup
    └── main.py          # App entry point & automatic table creator
```

 How to Setup & Run Locally

1. Install Dependencies
Make sure your python environment is active, then run:
```bash
pip install -r requirements.txt
```

2. Configure Environment Variables
Create a file named `.env` in the root folder and add your PostgreSQL connection string 

 3. Start the Server
Run this command from your root directory. The application will automatically create all 9 required database tables in PostgreSQL on startup:
```bash
python -m uvicorn app.main:app --reload
```

Testing the API
Open your browser and navigate to the interactive Swagger UI playground to test all endpoints:
Interactive API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Available Modules:
Employee Management (`/users`) - Register staff and open counter shifts.
Catalog Lookups (`/catalog`) - Setup lookup categories and suppliers.
Inventory Control (`/products`)  - Add products, restock inventory, and scan barcodes.
Sales Checkout (`/sales`) - Submit shopping carts and compute totals safely.
Payments & Receipts (`/payments`) - Process customer payments and print unique receipts.

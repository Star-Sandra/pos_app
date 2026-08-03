from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, create_tables, engine
from app.routers import user_router, product_router, sales_router, payment_router


# 1. Define the lifespan event manager (handles startup and shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
       create_tables()  
       yield  
      

# 2. Initialize the FastAPI app instance ONCE, passing the lifespan manager
app = FastAPI(title="Star POS System", version="1.0.0", lifespan=lifespan)

# 3. Core API Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Star POS API!"}

@app.get("/db_status_check")
def test_database_connection(db: Session = Depends(get_db)):
    try:        
        db.connection() 
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database connection failed: {str(e)}"
        )

app.include_router(user_router)
app.include_router(product_router)
app.include_router(sales_router)
app.include_router(payment_router)
"""
Database configuration for PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - Update with your PostgreSQL credentials
# Format: postgresql://username:password@localhost:5432/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://elas_user:elas_password@localhost:5432/elas_erp"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    echo=False,  # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

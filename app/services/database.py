# blog_app/services/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")

# --- ADD THIS FIX ---
# Render/Heroku provide URLs starting with "postgresql://", but async SQLAlchemy needs "postgresql+asyncpg://"
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
# --------------------

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

from sqlalchemy.orm import declarative_base
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
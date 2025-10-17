
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Database engine

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base

Base = declarative_base()

# Initialize DB

async def init_db():
    async with engine.begin() as conn:
        # Run synchronous DDL inside async context
        await conn.run_sync(Base.metadata.create_all)

# Dependency for FastAPI

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

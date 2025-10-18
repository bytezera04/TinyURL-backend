
from fastapi import FastAPI, Request, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal, engine, Base, init_db, get_db
from app.schemas import URLCreateDto, URLResponseDto
from sqlalchemy.future import select
from sqlalchemy import desc
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from app.models.url import URL
from datetime import datetime
from typing import List
from nanoid import generate

app = FastAPI()

##
##  CORS
##

CORS_ORIGIN = [
    "http://127.0.0.1:3000", "http://localhost:3000", # dev
    "https://tinyurldemo.dev" # prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN,              # Whitelist NextJS
    allow_credentials=True,                 # Allow cookies/auth headers
    allow_methods=["*"],                    # Allow all HTTP methods
    allow_headers=["*"],                    # Allow all headers
)

##
##  ID Generation
##

async def generate_unique_short(db: AsyncSessionLocal, length: int = 6) -> str:
    """Generate a unique short ID that does not collide in the database."""

    for _ in range(10):  # try max 10 times
        short_id = generate("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", length)
        # Check if it exists
        result = await db.execute(select(URL).filter(URL.short == short_id))
        existing = result.scalars().first()
        if not existing:
            return short_id
    
    raise HTTPException(status_code=500, detail="Failed to generate unique short URL")

##
##  Rate Limiting
##

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )

##
##  Application
##

@app.on_event("startup")
async def startup():
    # Initialize database

    await init_db()

@app.post("/urls/", response_model=URLResponseDto)
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def create_url(
    request: Request,
    payload: URLCreateDto,
    db: AsyncSessionLocal = Depends(get_db)
):
    # Generate the URL ID

    short_id = await generate_unique_short(db)

    # Add URL to the database

    db_url = URL(
        id=short_id,
        original=payload.original,
        short=short_id,
        clicks=0,
    )

    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)

    # Respond with URL dto

    return db_url

@app.get("/urls/top", response_model=List[URLResponseDto])
@limiter.limit("30/minute")
async def get_top_urls(
    request: Request,
    limit: int = Query(5, ge=1, le=100),
    db: AsyncSessionLocal = Depends(get_db)
):
    result = await db.execute(select(URL).order_by(desc(URL.clicks)).limit(limit))

    urls = result.scalars().all()

    return urls

@app.get("/urls/{short_id}", response_model=URLResponseDto)
@limiter.limit("60/minute")  # 60 requests per minute per IP
async def get_url(
    request: Request,
    short_id: str,
    db: AsyncSessionLocal = Depends(get_db)
):
    # Fetch the URL

    result = await db.execute(select(URL).filter(URL.short == short_id))

    db_url = result.scalars().first()

    # Handle not found

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Increment clicks

    db_url.clicks += 1
    db_url.last_clicked_at = datetime.now()

    await db.commit()
    await db.refresh(db_url)

    # Respond with URL dto

    return db_url

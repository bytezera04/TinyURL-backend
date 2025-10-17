
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal, engine, Base, init_db, get_db
from app.schemas import URLCreateDto, URLResponseDto
from sqlalchemy.future import select
from app.models.url import URL
from nanoid import generate

app = FastAPI()

##
##  CORS
##

CORS_ORIGIN = ["http://127.0.0.1:3000", "http://localhost:3000"]

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
##  Application
##

@app.on_event("startup")
async def startup():
    # Initialize database

    await init_db()

@app.post("/urls/", response_model=URLResponseDto)
async def create_url(payload: URLCreateDto, db: AsyncSessionLocal = Depends(get_db)):
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

@app.get("/urls/{short_id}", response_model=URLResponseDto)
async def get_url(short_id: str, db: AsyncSessionLocal = Depends(get_db)):
    # Fetch the URL

    result = await db.execute(select(URL).filter(URL.short == short_id))

    db_url = result.scalars().first()

    # Handle not found

    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Increment clicks

    db_url.clicks += 1

    await db.commit()
    await db.refresh(db_url)

    # Respond with URL dto

    return db_url

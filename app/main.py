
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import AsyncSessionLocal, engine, Base, init_db, get_db
from app.schemas import URLCreateDto, URLResponseDto
from app.models.url import URL
from uuid import uuid4
import uuid

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
##  Application
##

@app.on_event("startup")
async def startup():
    # Initialize database

    await init_db()

@app.post("/urls/", response_model=URLResponseDto)
async def create_url(payload: URLCreateDto, db: AsyncSessionLocal = Depends(get_db)):
    # Generate the URL ID

    short_id = str(uuid.uuid4())[:6]

    # Add URL to the database

    db_url = URL(
        id=str(uuid4()),
        original=payload.original,
        short=short_id,
        clicks=0,
    )

    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)

    # Respond with URL dto

    return db_url

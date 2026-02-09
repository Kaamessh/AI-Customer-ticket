from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

Base = declarative_base()

load_dotenv()

def get_db_url():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL is not set. Ensure .env is present and includes DATABASE_URL, or set the environment variable."
        )
    return url

engine = create_async_engine(get_db_url(), echo=True)

SessionLocal = async_sessionmaker(autoflush=False, class_=AsyncSession, bind=engine, expire_on_commit=False) 

async def get_db():
    async with SessionLocal() as db:
        yield db

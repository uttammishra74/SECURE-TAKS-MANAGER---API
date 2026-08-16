from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from app.config import user, password, port, host, name

load_dotenv()


DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"

# Create database if it doesn't exist
try:
    engine_root = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}")
    with engine_root.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {name}"))
        connection.commit()
    print(f"✅ Database '{name}' created or already exists")
except Exception as e:
    print(f"❌ Error creating database: {e}")
    

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

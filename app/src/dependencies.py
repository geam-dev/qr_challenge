from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
import os

url = URL.create(
    drivername="postgresql",
    username=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT')),
)

engine = create_engine(url)
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = Session()
    try:
        yield db 
    finally:
        db.close()

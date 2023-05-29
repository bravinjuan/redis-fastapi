# IMPORTS -------------------------------------------------------------
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from dotenv import load_dotenv
# IMPORTS -------------------------------------------------------------

load_dotenv()

DB_SERVER = os.getenv('DB_SERVER')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_UID = os.getenv('DB_UID')
DB_PASS = os.getenv('DB_PASS')
DATABASE_URL = urllib.parse.quote_plus(f'Driver={{ODBC Driver 17 for SQL Server}};Server={DB_SERVER},{DB_PORT};Database={DB_NAME};Uid={DB_UID};Pwd={DB_PASS};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
CONNECTION_STR = 'mssql+pyodbc:///?odbc_connect={}'.format(DATABASE_URL)

engine = create_engine(CONNECTION_STR, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

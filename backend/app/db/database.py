# data/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib
from dotenv import load_dotenv
import os

load_dotenv()

# Datos de conexión a Azure SQL
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER") 
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE") 
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

# Driver ODBC
driver = '{ODBC Driver 17 for SQL Server}'

# Cadena de conexión codificada
params = urllib.parse.quote_plus(
    f"DRIVER={driver};"
    f"SERVER={AZURE_SQL_SERVER};"
    f"DATABASE={AZURE_SQL_DATABASE};"
    f"UID={AZURE_SQL_USERNAME};"
    f"PWD={AZURE_SQL_PASSWORD};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Crear engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    use_scope_identity=False
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# from app.core.config import settings

# engine = create_engine(
#     settings.DATABASE_URL,
#     connect_args={"check_same_thread": False}
#     if settings.DATABASE_URL.startswith("sqlite")
#     else {},
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

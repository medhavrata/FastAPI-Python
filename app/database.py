from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Connection to database via SQLALCHEMY and we can use the Python methods to interact with
# database which under the hood will interact with psycopg2 to convert the python functions
# into the SQL Queries as the Postgres database only understands the SQL Queries

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#Connection to the Database via psycopg2, it will use the SQL to interact with database
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'database-name', user = 'sample-user', password = 'sample-password', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection has been successful !!")
#         break
#     except Exception as error:
#         print("Database connection has been failed")
#         print("Error was: ", error)
#         time.sleep(2)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

port = 5432
password = "admin"
username = "postgres"
db_url = f"postgresql://{username}:{password}@localhost:{port}/"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

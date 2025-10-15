from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

port = 5432
password = "admin"
username = "postgres"
db_url = f"postgresql://{username}:{password}@localhost:{port}/"
# Create the engine. `echo=True` is great for development as it logs all SQL commands.
engine = create_engine(db_url, echo=True)
# Create a configured "SessionLocal" class. This is not a session yet, but a factory.
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Question: What is the purpose of this file and what is a "database engine"?
# Answer: This file is the foundation of our database interaction. It creates a "factory" for database
# sessions and defines the connection string. The engine is SQLAlchemy's starting point. '
# 'It's a home for the connection pool, which manages database connections efficiently.
# The SessionLocal is a factory for creating individual database sessions,
# which represent a "conversation" with the database. Each request will get its own session.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

# Create a Base class. Our model classes (in models.py) will inherit from this.
# This Base class will later be used to create all the database tables.
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)


# # Question: What is an ORM Model and how is it different from a Pydantic model?
# Answer: An ORM Model (here, BookDB) is a Python class that represents a table in your database.
# Each instance of this class represents a row in that table.
# SQLAlchemy uses this to generate the SQL CREATE TABLE statements and to map Python objects to database rows.
# A Pydantic Model (next step) defines the schema or shape of the data for API requests and responses.
# It's about data validation and serialization, not database structure.

# Now we define the columns. These are the attributes of our table.
#    id = Column(Integer, primary_key=True, index=True)
# Column(Integer, primary_key=True, index=True): -
#   - `Integer` is the data type.
#   - `primary_key=True` marks this as the unique identifier for each row.
#   - `index=True` creates a database index for faster lookups on this column.

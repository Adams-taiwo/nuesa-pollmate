from sqlmodel import SQLModel
from sqlalchemy.ext.declarative import declarative_base

# The base for all models
Base = SQLModel

# Alternative declarative base for compatibility if needed
DeclarativeBase = declarative_base()

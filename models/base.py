from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    JSON,
)
Base = declarative_base()

metadata = MetaData()
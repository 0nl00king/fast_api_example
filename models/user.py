from base import (
    datetime,
    Base,
    metadata,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    JSON,
)


class Role(Base):
    __tablename__ = "role"

    metadata = metadata
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permission = Column(JSON)


class User(Base):
    __tablename__ = "user"

    metadata = metadata
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("role.id"))

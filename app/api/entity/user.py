from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "analytics"}
    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=True)

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ChatBotActivity(Base):
    __tablename__ = "chat-bot-activity"
    __table_args__ = {"schema": "chat-bot"}
    uuid = Column(UUID(as_uuid=True), nullable=False, primary_key=True)
    task_code = Column(String, nullable=False)
    name = Column(String, nullable=True)

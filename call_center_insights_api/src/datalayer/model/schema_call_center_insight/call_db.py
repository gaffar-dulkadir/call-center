from datetime import datetime
from uuid import UUID
import uuid
from sqlmodel import Field, SQLModel


class CallDB(SQLModel, table=True):
    __tablename__ = "call"
    __table_args__ = {"schema": "public"}

    call_id: UUID = Field(primary_key=True, default=uuid.uuid4())
    call_agent_name: str = Field(nullable=False)
    call_phone_number: str = Field(nullable=False)
    call_duration: float = Field(nullable=False)
    call_agent_speech_rate: float = Field(nullable=False)
    call_customer_speech_rate: float = Field(nullable=False)
    call_silence_rate: float = Field(nullable=False)
    call_cross_talk_rate: float = Field(nullable=False)
    call_agent_interrupt_count: int = Field(nullable=False)
    call_created_at: datetime = Field(nullable=False)

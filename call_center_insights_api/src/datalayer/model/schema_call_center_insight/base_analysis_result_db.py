from uuid import UUID
import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class BaseAnalysisResultDB(SQLModel, table=True):
    __tablename__ = "base_analysis_result"
    __table_args__ = {"schema": "public"}

    base_analysis_call_id: UUID = Field(primary_key=True, foreign_key="call_center_insight.call.call_id")
    base_analysis_reason: str = Field(nullable=False)
    base_analysis_reason_detail: str = Field(nullable=False)
    base_analysis_call_requires_followup: bool = Field(nullable=False)


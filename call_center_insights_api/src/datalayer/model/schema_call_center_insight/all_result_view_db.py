from datetime import datetime
from uuid import UUID
from typing import Optional
from sqlmodel import Field, SQLModel

class AllResultViewDB(SQLModel, table=True):
    __tablename__ = "mvw_analysis_result"
    __table_args__ = {"schema": "public"}

    # Primary key - using call_id as primary key since it's the main identifier
    call_id: UUID = Field(primary_key=True, description="Call ID from call table")
    
    # Call related fields (from call table)
    call_agent_name: str = Field(nullable=False, description="Agent name")
    call_phone_number: str = Field(nullable=False, description="Customer phone number")
    call_duration: float = Field(nullable=False, description="Call duration in seconds")
    call_agent_speech_rate: float = Field(nullable=False, description="Agent speech rate percentage")
    call_customer_speech_rate: float = Field(nullable=False, description="Customer speech rate percentage")
    call_silence_rate: float = Field(nullable=False, description="Silence rate percentage")
    call_cross_talk_rate: float = Field(nullable=False, description="Cross talk rate percentage")
    call_agent_interrupt_count: int = Field(nullable=False, description="Agent interrupt count")
    call_created_at: datetime = Field(nullable=False, description="Call creation timestamp")
    
    # Base analysis related fields (from base_analysis_result table)
    base_analysis_call_id: UUID = Field(nullable=True, description="Base analysis call ID")
    base_analysis_reason: str = Field(nullable=True, description="Call reason")
    base_analysis_reason_detail: str = Field(nullable=True, description="Call reason detail")
    base_analysis_call_requires_followup: bool = Field(nullable=True, description="Follow-up required flag")
    base_analysis_organization_metadata: Optional[str] = Field(default=None, description="Organization metadata as JSON string")
    
    # Issue analysis related fields (from issue_analysis_result table)
    issue_analysis_id: Optional[UUID] = Field(default=None, description="Issue analysis ID")
    issue_analysis_sub_category: Optional[str] = Field(default=None, description="Issue sub category")
    issue_analysis_sub_issue_type: Optional[str] = Field(default=None, description="Sub issue type")
    issue_analysis_churn_risk: Optional[int] = Field(default=None, description="Churn risk level")
    issue_analysis_urgency_level: Optional[str] = Field(default=None, description="Urgency level")
    issue_analysis_related_with_previous_call: Optional[bool] = Field(default=None, description="Related with previous call")
    issue_analysis_related_with_previous_call_detail: Optional[str] = Field(default=None, description="Previous call relation detail")
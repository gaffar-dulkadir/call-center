from sqlmodel import SQLModel, Field
from uuid import UUID

class IssueAnalysisResultDB(SQLModel, table=True):
    __tablename__ = "issue_analysis_result"
    __table_args__ = {"schema": "public"}

    issue_analysis_id: UUID = Field(primary_key=True)
    issue_analysis_sub_category: str = Field(nullable=False)
    issue_analysis_sub_issue_type: str = Field(nullable=False)
    issue_analysis_churn_risk: int = Field(nullable=False)
    issue_analysis_urgency_level: str = Field(nullable=False)
    issue_analysis_related_with_previous_call: bool = Field(nullable=False)
    issue_analysis_related_with_previous_call_detail: str = Field(nullable=False)


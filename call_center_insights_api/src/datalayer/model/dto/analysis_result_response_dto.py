from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

from datalayer.model.dto.base_dto import BaseDto
from datalayer.model.dto.all_result_view_dto import AllResultViewDto

T = TypeVar('T')

class AnalysisResultResponseDto(BaseDto):
    """Analysis result response model with count"""
    is_success: bool = Field(..., description="Success status")
    count: int = Field(..., description="Total count of records")
    message: Optional[str] = Field(None, description="Response message")
    data: List[AllResultViewDto] = Field(..., description="Analysis result data")
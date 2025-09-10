from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

from datalayer.model.dto.base_dto import BaseDto

T = TypeVar('T')

class BusinessLogicDto(BaseDto):
    """Business logic yanıt modeli"""
    is_success: bool = Field(..., description="Success status")
    message: Optional[str] = Field(None, description="Response message")

class BusinessLogicDtoGeneric(BusinessLogicDto, Generic[T]):
    """Generic başarılı yanıt modeli - tip güvenli"""
    data: T = Field(..., description="Response data")
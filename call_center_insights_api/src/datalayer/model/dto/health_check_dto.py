from datetime import datetime

from pydantic import BaseModel, Field

from datalayer.model.dto.base_dto import BaseDto


class HealthCheckDto(BaseDto):
    """Sağlık kontrolü yanıt modeli"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="API version")
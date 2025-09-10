from pydantic import Field
from .base_dto import BaseDto


class MerchantContactCreateDto(BaseDto):
    """
    Yeni bir MerchantContact kaydı oluşturmak için kullanılan DTO.
    """
    
    merchant_id: int = Field(..., description="Merchant ID'si", alias="merchantId")


class MerchantContactDto(BaseDto):
    """
    API'den bir MerchantContact kaydı döndürmek için kullanılan DTO.
    """
    
    id: int = Field(..., description="Contact benzersiz ID'si")
    merchant_id: int = Field(..., description="Merchant ID'si", alias="merchantId")
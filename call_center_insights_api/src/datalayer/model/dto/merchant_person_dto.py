from pydantic import Field
from typing import Optional
from .base_dto import BaseDto


# --- CREATE DTO ---
class MerchantPersonCreateDto(BaseDto):
    """
    Yeni bir MerchantPerson kaydı oluşturmak için kullanılan DTO.
    """
    
    merchant_id: int = Field(..., description="Merchant ID'si", alias="merchantId")
    merchant_person_state: Optional[str] = Field(None, description="Merchant kişi durumu", alias="merchantPersonState")
    merchant_person_name: Optional[str] = Field(None, description="Merchant kişi adı", alias="merchantPersonName")
    merchant_person_phone: Optional[str] = Field(None, description="Merchant kişi telefonu", alias="merchantPersonPhone")


# --- RESPONSE DTO ---
class MerchantPersonDto(BaseDto):
    """
    API'den bir MerchantPerson kaydı döndürmek için kullanılan DTO.
    """
    
    merchant_id: int = Field(..., description="Merchant ID'si", alias="merchantId")
    merchant_person_state: Optional[str] = Field(None, description="Merchant kişi durumu", alias="merchantPersonState")
    merchant_person_name: Optional[str] = Field(None, description="Merchant kişi adı", alias="merchantPersonName")
    merchant_person_phone: Optional[str] = Field(None, description="Merchant kişi telefonu", alias="merchantPersonPhone")
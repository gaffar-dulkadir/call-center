from pydantic import Field
from datetime import datetime
from typing import Optional
from .base_dto import BaseDto


# --- CREATE DTO ---
class MerchantCreateDto(BaseDto):
    """
    Yeni bir Merchant kaydı oluşturmak için kullanılan DTO.
    """
    
    merchant_name: str = Field(..., description="Merchant adı", alias="merchantName")
    merchant_brand: Optional[str] = Field(None, description="Merchant markası", alias="merchantBrand")
    merchant_status: Optional[str] = Field(None, description="Merchant durumu", alias="merchantStatus")
    merchant_city: Optional[str] = Field(None, description="Merchant şehri", alias="merchantCity")
    merchant_district: Optional[str] = Field(None, description="Merchant ilçesi", alias="merchantDistrict")
    merchant_address: Optional[str] = Field(None, description="Merchant adresi", alias="merchantAddress")
    merchant_tax_no: Optional[str] = Field(None, description="Merchant vergi numarası", alias="merchantTaxNo")
    merchant_tax_office: Optional[str] = Field(None, description="Merchant vergi dairesi", alias="merchantTaxOffice")
    merchant_sector: Optional[str] = Field(None, description="Merchant sektörü", alias="merchantSector")
    merchant_people: Optional[int] = Field(None, description="Merchant çalışan sayısı", alias="merchantPeople")
    merchant_hardware: Optional[str] = Field(None, description="Merchant donanımı", alias="merchantHardware")
    merchant_fiscal_no: Optional[str] = Field(None, description="Merchant mali sicil numarası", alias="merchantFiscalNo")
    merchant_service: Optional[str] = Field(None, description="Merchant hizmeti", alias="merchantService")
    merchant_ticket: Optional[str] = Field(None, description="Merchant ticket bilgisi", alias="merchantTicket")


# --- RESPONSE DTO ---
class MerchantDto(BaseDto):
    """
    API'den bir Merchant kaydı döndürmek için kullanılan DTO.
    """
    
    id: int = Field(..., description="Merchant benzersiz ID'si")
    merchant_name: str = Field(..., description="Merchant adı", alias="merchantName")
    merchant_brand: Optional[str] = Field(None, description="Merchant markası", alias="merchantBrand")
    merchant_status: Optional[str] = Field(None, description="Merchant durumu", alias="merchantStatus")
    merchant_city: Optional[str] = Field(None, description="Merchant şehri", alias="merchantCity")
    merchant_district: Optional[str] = Field(None, description="Merchant ilçesi", alias="merchantDistrict")
    merchant_address: Optional[str] = Field(None, description="Merchant adresi", alias="merchantAddress")
    merchant_tax_no: Optional[str] = Field(None, description="Merchant vergi numarası", alias="merchantTaxNo")
    merchant_tax_office: Optional[str] = Field(None, description="Merchant vergi dairesi", alias="merchantTaxOffice")
    merchant_sector: Optional[str] = Field(None, description="Merchant sektörü", alias="merchantSector")
    merchant_people: Optional[int] = Field(None, description="Merchant çalışan sayısı", alias="merchantPeople")
    merchant_hardware: Optional[str] = Field(None, description="Merchant donanımı", alias="merchantHardware")
    merchant_fiscal_no: Optional[str] = Field(None, description="Merchant mali sicil numarası", alias="merchantFiscalNo")
    merchant_service: Optional[str] = Field(None, description="Merchant hizmeti", alias="merchantService")
    merchant_ticket: Optional[str] = Field(None, description="Merchant ticket bilgisi", alias="merchantTicket")
    inserted_at: datetime = Field(..., description="Kaydın oluşturulma zamanı", alias="insertedAt")
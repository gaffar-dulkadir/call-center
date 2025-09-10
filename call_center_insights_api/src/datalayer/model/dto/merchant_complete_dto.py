from pydantic import Field
from datetime import datetime
from typing import Optional, List
from .base_dto import BaseDto


# --- Consolidated response DTO for all merchant data ---
class MerchantCompleteDto(BaseDto):
    """
    Bir merchant_id için beş tablodan gelen tüm veriyi içeren konsolide DTO.
    """
    
    # Merchant basic info
    merchant_id: int = Field(..., description="Merchant benzersiz ID'si", alias="merchantId")
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
    merchant_inserted_at: datetime = Field(..., description="Merchant kaydının oluşturulma zamanı", alias="merchantInsertedAt")
    
    # Merchant person info
    merchant_person_state: Optional[str] = Field(None, description="Merchant kişi durumu", alias="merchantPersonState")
    merchant_person_name: Optional[str] = Field(None, description="Merchant kişi adı", alias="merchantPersonName")
    merchant_person_phone: Optional[str] = Field(None, description="Merchant kişi telefonu", alias="merchantPersonPhone")
    
    # Merchant contacts
    contact_ids: Optional[List[int]] = Field(None, description="Merchant ile ilişkili contact ID'leri", alias="contactIds")
    
    # Merchant tickets with details
    tickets: Optional[List["MerchantTicketWithDetailsDto"]] = Field(None, description="Merchant ile ilişkili ticket ve detayları", alias="tickets")


class MerchantTicketWithDetailsDto(BaseDto):
    """
    Merchant ticket ve onun detaylarını içeren DTO.
    """
    
    # Ticket info
    ticket_id: int = Field(..., description="Merchant ticket benzersiz ID'si", alias="ticketId")
    merchant_ticket_order_no: Optional[int] = Field(None, description="Merchant ticket sipariş numarası", alias="merchantTicketOrderNo")
    merchant_ticket_type_id: Optional[int] = Field(None, description="Merchant ticket tip ID'si", alias="merchantTicketTypeId")
    merchant_ticket_time: Optional[datetime] = Field(None, description="Merchant ticket zamanı", alias="merchantTicketTime")
    merchant_ticket_kind_id: Optional[int] = Field(None, description="Merchant ticket türü ID'si", alias="merchantTicketKindId")
    merchant_ticket_sub_type_id: Optional[int] = Field(None, description="Merchant ticket alt tip ID'si", alias="merchantTicketSubTypeId")
    merchant_ticket_explanation: Optional[str] = Field(None, description="Merchant ticket açıklaması", alias="merchantTicketExplanation")
    merchant_ticket_first_explanation: Optional[str] = Field(None, description="Merchant ticket ilk açıklaması", alias="merchantTicketFirstExplanation")
    
    # Ticket details
    ticket_detail: Optional[str] = Field(None, description="Ticket detayı", alias="ticketDetail")


class MerchantBatchRequestDto(BaseDto):
    """
    Batch request için kullanılan DTO - tek veya birden fazla merchant_id.
    """
    
    merchant_ids: List[int] = Field(..., description="Sorgulanacak merchant ID'lerin listesi", alias="merchantIds")


class MerchantBatchResponseDto(BaseDto):
    """
    Batch response için kullanılan DTO - birden fazla merchant verisi.
    """
    
    merchants: List[MerchantCompleteDto] = Field(..., description="Merchant verileri listesi", alias="merchants")
    total_count: int = Field(..., description="Toplam bulunan merchant sayısı", alias="totalCount")
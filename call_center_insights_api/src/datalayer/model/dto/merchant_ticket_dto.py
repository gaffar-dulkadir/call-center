from pydantic import Field
from datetime import datetime
from typing import Optional
from .base_dto import BaseDto


# --- CREATE DTO ---
class MerchantTicketCreateDto(BaseDto):
    """
    Yeni bir MerchantTicket kaydı oluşturmak için kullanılan DTO.
    """
    
    merchant_id: int = Field(..., description="Merchant ID'si", alias="merchantId")
    merchant_ticket_order_no: Optional[int] = Field(None, description="Merchant ticket sipariş numarası", alias="merchantTicketOrderNo")
    merchant_ticket_type_id: Optional[int] = Field(None, description="Merchant ticket tip ID'si", alias="merchantTicketTypeId")
    merchant_ticket_time: Optional[datetime] = Field(None, description="Merchant ticket zamanı", alias="merchantTicketTime")
    merchant_ticket_kind_id: Optional[int] = Field(None, description="Merchant ticket türü ID'si", alias="merchantTicketKindId")
    merchant_ticket_sub_type_id: Optional[int] = Field(None, description="Merchant ticket alt tip ID'si", alias="merchantTicketSubTypeId")
    merchant_ticket_explanation: Optional[str] = Field(None, description="Merchant ticket açıklaması", alias="merchantTicketExplanation")
    merchant_ticket_first_explanation: Optional[str] = Field(None, description="Merchant ticket ilk açıklaması", alias="merchantTicketFirstExplanation")


# --- RESPONSE DTO ---
class MerchantTicketDto(BaseDto):
    """
    API'den bir MerchantTicket kaydı döndürmek için kullanılan DTO.
    """
    
    id: int = Field(..., description="Merchant ticket benzersiz ID'si")
    merchant_id: int = Field(..., description="Merchant ID'si", alias="merchantId")
    merchant_ticket_order_no: Optional[int] = Field(None, description="Merchant ticket sipariş numarası", alias="merchantTicketOrderNo")
    merchant_ticket_type_id: Optional[int] = Field(None, description="Merchant ticket tip ID'si", alias="merchantTicketTypeId")
    merchant_ticket_time: Optional[datetime] = Field(None, description="Merchant ticket zamanı", alias="merchantTicketTime")
    merchant_ticket_kind_id: Optional[int] = Field(None, description="Merchant ticket türü ID'si", alias="merchantTicketKindId")
    merchant_ticket_sub_type_id: Optional[int] = Field(None, description="Merchant ticket alt tip ID'si", alias="merchantTicketSubTypeId")
    merchant_ticket_explanation: Optional[str] = Field(None, description="Merchant ticket açıklaması", alias="merchantTicketExplanation")
    merchant_ticket_first_explanation: Optional[str] = Field(None, description="Merchant ticket ilk açıklaması", alias="merchantTicketFirstExplanation")
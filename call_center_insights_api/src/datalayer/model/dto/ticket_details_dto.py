from pydantic import Field
from typing import Optional
from .base_dto import BaseDto


# --- CREATE DTO ---
class TicketDetailsCreateDto(BaseDto):
    """
    Yeni bir TicketDetails kaydı oluşturmak için kullanılan DTO.
    """
    
    ticket_id: int = Field(..., description="Ticket ID'si", alias="ticketId")
    ticket_detail: Optional[str] = Field(None, description="Ticket detayı", alias="ticketDetail")


# --- RESPONSE DTO ---
class TicketDetailsDto(BaseDto):
    """
    API'den bir TicketDetails kaydı döndürmek için kullanılan DTO.
    """
    
    ticket_id: int = Field(..., description="Ticket ID'si", alias="ticketId")
    ticket_detail: Optional[str] = Field(None, description="Ticket detayı", alias="ticketDetail")
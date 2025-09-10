# datalayer/model/dto/call_dto.py - Sadeleştirilmiş Versiyon

from pydantic import Field
from uuid import UUID
from datetime import datetime
from .base_dto import BaseDto  # Ana BaseDto'yu import ediyoruz

# --- CREATE DTO ---
# API'ye yeni bir Call kaydı oluşturmak için gönderilen veri modeli
class CallCreateDto(BaseDto):
    """
    Yeni bir Call kaydı oluşturmak için kullanılan DTO.
    BaseDto'dan 'to_camel' ve diğer konfigürasyonları miras alır.
    """
    
    agent_name: str = Field(..., description="Görüşmeyi yapan ajanın adı", alias="agentName")
    phone_number: str = Field(..., description="Müşterinin telefon numarası", alias="phoneNumber")
    duration: float = Field(..., description="Görüşmenin saniye cinsinden süresi", ge=0)
    agent_speech_rate: float = Field(..., description="Ajanın konuşma oranı (%)", ge=0, le=100, alias="agentSpeechRate")
    customer_speech_rate: float = Field(..., description="Müşterinin konuşma oranı (%)", ge=0, le=100, alias="customerSpeechRate")
    silence_rate: float = Field(..., description="Görüşmedeki sessizlik oranı (%)", ge=0, le=100, alias="silenceRate")
    cross_talk_rate: float = Field(..., description="Karşılıklı konuşma oranı (%)", ge=0, le=100, alias="crossTalkRate")
    agent_interrupt_count: int = Field(..., description="Ajanın müşterinin sözünü kesme sayısı", ge=0, alias="agentInterruptCount")

    # `to_db_model` yöntemi burada olmamalı. Bu işi Mapper yapar.


# --- RESPONSE DTO ---
# API'den cevap olarak dönen veri modeli
class CallDto(BaseDto):
    """
    API'den bir Call kaydı döndürmek için kullanılan DTO.
    """
    
    id: UUID = Field(..., description="Arama kaydının benzersiz ID'si")
    agent_name: str = Field(..., description="Görüşmeyi yapan ajanın adı", alias="agentName")
    phone_number: str = Field(..., description="Müşterinin telefon numarası", alias="phoneNumber")
    duration: float = Field(..., description="Görüşmenin saniye cinsinden süresi")
    agent_speech_rate: float = Field(..., description="Ajanın konuşma oranı (%)", alias="agentSpeechRate")
    customer_speech_rate: float = Field(..., description="Müşterinin konuşma oranı (%)", alias="customerSpeechRate")
    silence_rate: float = Field(..., description="Görüşmedeki sessizlik oranı (%)", alias="silenceRate")
    cross_talk_rate: float = Field(..., description="Karşılıklı konuşma oranı (%)", alias="crossTalkRate")
    agent_interrupt_count: int = Field(..., description="Ajanın müşterinin sözünü kesme sayısı", alias="agentInterruptCount")
    created_at: datetime = Field(..., description="Kaydın oluşturulma zamanı", alias="createdAt")

    # `from_db_model` yöntemi burada olmamalı. Bu işi Mapper yapar.
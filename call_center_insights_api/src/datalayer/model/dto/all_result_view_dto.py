# datalayer/model/dto/all_result_view_dto.py

from pydantic import Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Union, Any
from .base_dto import BaseDto

# --- CREATE DTO ---
# API'ye yeni kayıt oluşturmak için gönderilen veri modeli (eğer view insert destekliyorsa)
class AllResultViewCreateDto(BaseDto):
    """
    Yeni bir AnalysisResultView kaydı oluşturmak için kullanılan DTO.
    BaseDto'dan 'to_camel' ve diğer konfigürasyonları miras alır.
    Note: Views genellikle INSERT desteklemez, bu DTO sadece completeness için.
    """
    
    # Call bilgileri
    agent_name: str = Field(..., description="Görüşmeyi yapan ajanın adı", alias="agentName")
    phone_number: str = Field(..., description="Müşterinin telefon numarası", alias="phoneNumber")
    duration: float = Field(..., description="Görüşmenin saniye cinsinden süresi", ge=0)
    agent_speech_rate: float = Field(..., description="Ajanın konuşma oranı (%)", ge=0, le=100, alias="agentSpeechRate")
    customer_speech_rate: float = Field(..., description="Müşterinin konuşma oranı (%)", ge=0, le=100, alias="customerSpeechRate")
    silence_rate: float = Field(..., description="Görüşmedeki sessizlik oranı (%)", ge=0, le=100, alias="silenceRate")
    cross_talk_rate: float = Field(..., description="Karşılıklı konuşma oranı (%)", ge=0, le=100, alias="crossTalkRate")
    agent_interrupt_count: int = Field(..., description="Ajanın müşterinin sözünü kesme sayısı", ge=0, alias="agentInterruptCount")
    
    # Base Analysis bilgileri
    call_reason: str = Field(..., description="Aramanın ana nedeni", alias="callReason")
    call_reason_detail: str = Field(..., description="Arama nedeninin detaylı açıklaması", alias="callReasonDetail")
    is_follow_up_required: bool = Field(..., description="Aramanın takip gerektirip gerektirmediği", alias="isFollowUpRequired")


# --- RESPONSE DTO ---
# API'den cevap olarak dönen veri modeli
class AllResultViewDto(BaseDto):
    """
    API'den bir AnalysisResultView kaydı döndürmek için kullanılan DTO.
    Bu DTO call, base analysis result ve issue analysis result verilerini birleştirir.
    """
    
    # Primary ID (call_id)
    call_id: UUID = Field(..., description="Call kaydının benzersiz ID'si", alias="callId")
    
    # Call bilgileri
    agent_name: str = Field(..., description="Görüşmeyi yapan ajanın adı", alias="agentName")
    phone_number: str = Field(..., description="Müşterinin telefon numarası", alias="phoneNumber")
    duration: float = Field(..., description="Görüşmenin saniye cinsinden süresi")
    agent_speech_rate: float = Field(..., description="Ajanın konuşma oranı (%)", alias="agentSpeechRate")
    customer_speech_rate: float = Field(..., description="Müşterinin konuşma oranı (%)", alias="customerSpeechRate")
    silence_rate: float = Field(..., description="Görüşmedeki sessizlik oranı (%)", alias="silenceRate")
    cross_talk_rate: float = Field(..., description="Karşılıklı konuşma oranı (%)", alias="crossTalkRate")
    agent_interrupt_count: int = Field(..., description="Ajanın müşterinin sözünü kesme sayısı", alias="agentInterruptCount")
    created_at: datetime = Field(..., description="Kaydın oluşturulma zamanı", alias="createdAt")
    
    # Base Analysis bilgileri (nullable due to LEFT JOIN)
    base_analysis_call_id: Optional[UUID] = Field(None, description="Base analysis call ID", alias="baseAnalysisCallId")
    call_reason: Optional[str] = Field(None, description="Aramanın ana nedeni", alias="callReason")
    call_reason_detail: Optional[str] = Field(None, description="Arama nedeninin detaylı açıklaması", alias="callReasonDetail")
    is_follow_up_required: Optional[bool] = Field(None, description="Aramanın takip gerektirip gerektirmediği", alias="isFollowUpRequired")
    organization_metadata: Optional[Union[str, dict, Any]] = Field(None, description="Organizasyon metadata'sı", alias="organizationMetadata")
    
    # Issue Analysis bilgileri (nullable due to LEFT JOIN)
    issue_analysis_id: Optional[UUID] = Field(None, description="Issue analysis ID", alias="issueAnalysisId")
    issue_sub_category: Optional[str] = Field(None, description="Issue alt kategorisi", alias="issueSubCategory")
    sub_issue_type: Optional[str] = Field(None, description="Alt issue tipi", alias="subIssueType")
    churn_risk: Optional[Union[str, int]] = Field(None, description="Churn risk seviyesi", alias="churnRisk")
    urgency_level: Optional[str] = Field(None, description="Aciliyet seviyesi", alias="urgencyLevel")
    related_with_previous_call: Optional[bool] = Field(None, description="Önceki çağrı ile ilişkili mi", alias="relatedWithPreviousCall")
    previous_call_relation_detail: Optional[str] = Field(None, description="Önceki çağrı ilişki detayı", alias="previousCallRelationDetail")
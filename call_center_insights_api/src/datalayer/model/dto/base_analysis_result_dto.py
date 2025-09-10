# datalayer/model/dto/base_analysis_result_dto.py - Sadeleştirilmiş Versiyon

from pydantic import Field
from uuid import UUID
from .base_dto import BaseDto  # Ana BaseDto'yu import ediyoruz

# --- CREATE DTO ---
# API'ye yeni kayıt oluşturmak için gönderilen veri modeli
class BaseAnalysisResultCreateDto(BaseDto):
    """
    Yeni bir BaseAnalysisResult kaydı oluşturmak için kullanılan DTO.
    BaseDto'dan 'to_camel' ve diğer konfigürasyonları miras alır.
    """
    
    call_reason: str = Field(..., description="Aramanın ana nedeni (soru, talep, vb.)", alias="callReason")
    call_reason_detail: str = Field(..., description="Arama nedeninin detaylı açıklaması", alias="callReasonDetail")
    is_follow_up_required: bool = Field(..., description="Aramanın takip gerektirip gerektirmediği", alias="isFollowUpRequired")

    # `to_db_model` gibi yöntemler burada olmamalı, bu işi Mapper yapmalı.


# --- RESPONSE DTO ---
# API'den cevap olarak dönen veri modeli  
class BaseAnalysisResultDto(BaseDto):
    """
    API'den bir BaseAnalysisResult kaydı döndürmek için kullanılan DTO.
    """
    
    id: UUID = Field(..., description="Base Analysis kaydının benzersiz ID'si")
    call_reason: str = Field(..., description="Aramanın ana nedeni", alias="callReason")
    call_reason_detail: str = Field(..., description="Arama nedeninin detaylı açıklaması", alias="callReasonDetail")
    is_follow_up_required: bool = Field(..., description="Aramanın takip gerektirip gerektirmediği", alias="isFollowUpRequired")

    # `from_db_model` gibi yöntemler burada olmamalı, bu işi Mapper yapmalı.
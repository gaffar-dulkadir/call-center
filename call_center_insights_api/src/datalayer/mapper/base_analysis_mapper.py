from datalayer import BaseAnalysisResultDB
from datalayer import BaseAnalysisResultDto, BaseAnalysisResultCreateDto

class BaseAnalysisMapper:
    """
    Base Analysis Result için DB modeli ile DTO arasında dönüşüm yapar.
    """
    
    @staticmethod
    def to_dto(base_analysis_data: BaseAnalysisResultDB) -> BaseAnalysisResultDto:
        """
        BaseAnalysisResultDB modelini BaseAnalysisResultDto'ya dönüştürür.
        """
        if base_analysis_data is None:
            return None
            
        return BaseAnalysisResultDto(
            id=base_analysis_data.base_analysis_call_id,  # Veritabanı modelindeki ID alanı
            call_reason=base_analysis_data.base_analysis_reason,
            call_reason_detail=base_analysis_data.base_analysis_reason_detail,
            is_follow_up_required=base_analysis_data.base_analysis_call_requires_followup
        )

    @staticmethod
    def to_db(base_analysis_data: BaseAnalysisResultCreateDto) -> BaseAnalysisResultDB:
        """
        BaseAnalysisResultCreateDto'yu BaseAnalysisResultDB modeline dönüştürür.
        """
        if base_analysis_data is None:
            return None
            
        return BaseAnalysisResultDB(
            base_analysis_reason=base_analysis_data.call_reason,
            base_analysis_reason_detail=base_analysis_data.call_reason_detail,
            base_analysis_call_requires_followup=base_analysis_data.is_follow_up_required
        )
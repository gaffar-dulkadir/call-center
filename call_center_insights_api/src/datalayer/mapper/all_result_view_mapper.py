from datalayer.model.schema_call_center_insight.all_result_view_db import AllResultViewDB
from datalayer.model.dto.all_result_view_dto import AllResultViewDto
from typing import List
import logging
import json

logger = logging.getLogger(__name__)

class AllResultViewMapper:
    """
    All Result View için DB modeli ile DTO arasında dönüşüm yapar.
    Not: Bu bir view olduğu için sadece READ işlemleri desteklenir.
    """
    
    @staticmethod
    def _convert_organization_metadata(metadata) -> str:
        """
        Handle organization_metadata conversion from dict/object to string.
        This fixes the validation error when SQLAlchemy returns JSON as dict.
        """
        if metadata is None:
            return None
        
        # If it's already a string, return as-is
        if isinstance(metadata, str):
            return metadata
            
        # If it's a dict/object, convert to JSON string
        if isinstance(metadata, (dict, list)):
            try:
                result = json.dumps(metadata)
                logger.debug(f"🔄 Converted organization_metadata from {type(metadata)} to string: {result[:100]}...")
                return result
            except Exception as e:
                logger.warning(f"⚠️ Failed to convert organization_metadata to JSON: {e}, returning str()")
                return str(metadata)
        
        # For any other type, convert to string
        logger.debug(f"🔄 Converting organization_metadata from {type(metadata)} to string")
        return str(metadata)

    @staticmethod
    def _convert_churn_risk(churn_risk) -> str:
        """
        Handle churn_risk conversion from int to string.
        Database stores it as smallint, but API expects string.
        """
        if churn_risk is None:
            return None
        
        # If it's already a string, return as-is
        if isinstance(churn_risk, str):
            return churn_risk
            
        # Convert int to string
        if isinstance(churn_risk, int):
            result = str(churn_risk)
            logger.debug(f"🔄 Converted churn_risk from int {churn_risk} to string '{result}'")
            return result
        
        # For any other type, convert to string
        logger.debug(f"🔄 Converting churn_risk from {type(churn_risk)} to string")
        return str(churn_risk)

    @staticmethod
    def to_dto(db_model: AllResultViewDB) -> AllResultViewDto:
        """
        AllResultViewDB modelini AllResultViewDto'ya dönüştürür.
        """
        if db_model is None:
            return None

        # Log the organization_metadata type and value for debugging
        if db_model.base_analysis_organization_metadata is not None:
            logger.debug(f"🔍 organization_metadata type: {type(db_model.base_analysis_organization_metadata)}, "
                        f"value: {str(db_model.base_analysis_organization_metadata)[:100]}...")
            
        return AllResultViewDto(
            # Primary ID
            call_id=db_model.call_id,
            
            # Call bilgileri
            agent_name=db_model.call_agent_name,
            phone_number=db_model.call_phone_number,
            duration=db_model.call_duration,
            agent_speech_rate=db_model.call_agent_speech_rate,
            customer_speech_rate=db_model.call_customer_speech_rate,
            silence_rate=db_model.call_silence_rate,
            cross_talk_rate=db_model.call_cross_talk_rate,
            agent_interrupt_count=db_model.call_agent_interrupt_count,
            created_at=db_model.call_created_at,
            
            # Base Analysis bilgileri (nullable due to LEFT JOIN)
            base_analysis_call_id=db_model.base_analysis_call_id,
            call_reason=db_model.base_analysis_reason,
            call_reason_detail=db_model.base_analysis_reason_detail,
            is_follow_up_required=db_model.base_analysis_call_requires_followup,
            organization_metadata=AllResultViewMapper._convert_organization_metadata(
                db_model.base_analysis_organization_metadata
            ),
            
            # Issue Analysis bilgileri (nullable due to LEFT JOIN)
            issue_analysis_id=db_model.issue_analysis_id,
            issue_sub_category=db_model.issue_analysis_sub_category,
            sub_issue_type=db_model.issue_analysis_sub_issue_type,
            churn_risk=AllResultViewMapper._convert_churn_risk(db_model.issue_analysis_churn_risk),
            urgency_level=db_model.issue_analysis_urgency_level,
            related_with_previous_call=db_model.issue_analysis_related_with_previous_call,
            previous_call_relation_detail=db_model.issue_analysis_related_with_previous_call_detail
        )

    @staticmethod
    def to_dto_list(db_models: List[AllResultViewDB]) -> List[AllResultViewDto]:
        """
        DB modeli listesini DTO listesine dönüştürür.
        Bulk conversion helper method.
        """
        if not db_models:
            return []
        
        return [AllResultViewMapper.to_dto(db_model) for db_model in db_models]
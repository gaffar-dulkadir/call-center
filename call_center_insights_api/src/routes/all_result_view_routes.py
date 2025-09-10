from typing import List, Optional
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer import BusinessLogicDtoGeneric
from datalayer import get_db_session
from datalayer.model.dto.all_result_view_dto import AllResultViewDto
from datalayer.model.dto.analysis_result_response_dto import AnalysisResultResponseDto
from services.all_result_view_service import AllResultViewService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analysis-result", tags=["ANALYSIS_RESULT"])

@router.get(
    "",
    response_model=AnalysisResultResponseDto,
    summary="Retrieve all analysis results",
    description="Fetches a list of all analysis results from the view with optional pagination and filtering. Includes total count."
)
async def get_analysis_results(
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Maximum number of results to return"),
    offset: Optional[int] = Query(None, ge=0, description="Number of results to skip"),
    agent_name: Optional[str] = Query(None, description="Filter by agent name (partial match)"),
    phone_number: Optional[str] = Query(None, description="Filter by phone number (exact match)"),
    follow_up_required: Optional[bool] = Query(None, description="Filter by follow-up requirement"),
    reason_contains: Optional[str] = Query(None, description="Filter by call reason (partial match)"),
    # Date range filters
    created_at_from: Optional[str] = Query(None, description="Filter calls created from this date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    created_at_to: Optional[str] = Query(None, description="Filter calls created until this date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)"),
    # Numeric range filters
    duration_min: Optional[float] = Query(None, description="Minimum call duration in seconds"),
    duration_max: Optional[float] = Query(None, description="Maximum call duration in seconds"),
    agent_speech_rate_min: Optional[float] = Query(None, description="Minimum agent speech rate percentage"),
    agent_speech_rate_max: Optional[float] = Query(None, description="Maximum agent speech rate percentage"),
    customer_speech_rate_min: Optional[float] = Query(None, description="Minimum customer speech rate percentage"),
    customer_speech_rate_max: Optional[float] = Query(None, description="Maximum customer speech rate percentage"),
    silence_rate_min: Optional[float] = Query(None, description="Minimum silence rate percentage"),
    silence_rate_max: Optional[float] = Query(None, description="Maximum silence rate percentage"),
    cross_talk_rate_min: Optional[float] = Query(None, description="Minimum cross talk rate percentage"),
    cross_talk_rate_max: Optional[float] = Query(None, description="Maximum cross talk rate percentage"),
    agent_interrupt_count_min: Optional[int] = Query(None, description="Minimum agent interrupt count"),
    agent_interrupt_count_max: Optional[int] = Query(None, description="Maximum agent interrupt count"),
    churn_risk_min: Optional[int] = Query(None, description="Minimum churn risk level"),
    churn_risk_max: Optional[int] = Query(None, description="Maximum churn risk level"),
    db: AsyncSession = Depends(get_db_session),
) -> AnalysisResultResponseDto:
    """
    Retrieve all analysis results with optional filtering and pagination. Includes total count.
    Args:
        limit (int, optional): Maximum number of results to return (1-1000).
        offset (int, optional): Number of results to skip for pagination.
        agent_name (str, optional): Filter by agent name (partial match).
        phone_number (str, optional): Filter by phone number (exact match).
        follow_up_required (bool, optional): Filter by follow-up requirement.
        reason_contains (str, optional): Filter by call reason (partial match).
        created_at_from/to (str, optional): Filter by creation date range.
        duration_min/max (float, optional): Filter by call duration range.
        Various min/max range filters for numeric fields.
        db (AsyncSession): Database session dependency.
    Returns:
        AnalysisResultResponseDto: A response containing filtered analysis results with count.
    """
    logger.info("🚀 Route: Getting analysis results with filters and count")
    
    try:
        analysis_service = AllResultViewService(db)
        
        # Apply filters if provided
        filters = {}
        if agent_name:
            filters['agent_name'] = agent_name
        if phone_number:
            filters['phone_number'] = phone_number
        if follow_up_required is not None:
            filters['follow_up_required'] = follow_up_required
        if reason_contains:
            filters['reason_contains'] = reason_contains
        
        # Date range filters
        if created_at_from:
            filters['created_at_from'] = created_at_from
        if created_at_to:
            filters['created_at_to'] = created_at_to
        
        # Numeric range filters
        if duration_min is not None:
            filters['duration_min'] = duration_min
        if duration_max is not None:
            filters['duration_max'] = duration_max
        if agent_speech_rate_min is not None:
            filters['agent_speech_rate_min'] = agent_speech_rate_min
        if agent_speech_rate_max is not None:
            filters['agent_speech_rate_max'] = agent_speech_rate_max
        if customer_speech_rate_min is not None:
            filters['customer_speech_rate_min'] = customer_speech_rate_min
        if customer_speech_rate_max is not None:
            filters['customer_speech_rate_max'] = customer_speech_rate_max
        if silence_rate_min is not None:
            filters['silence_rate_min'] = silence_rate_min
        if silence_rate_max is not None:
            filters['silence_rate_max'] = silence_rate_max
        if cross_talk_rate_min is not None:
            filters['cross_talk_rate_min'] = cross_talk_rate_min
        if cross_talk_rate_max is not None:
            filters['cross_talk_rate_max'] = cross_talk_rate_max
        if agent_interrupt_count_min is not None:
            filters['agent_interrupt_count_min'] = agent_interrupt_count_min
        if agent_interrupt_count_max is not None:
            filters['agent_interrupt_count_max'] = agent_interrupt_count_max
        if churn_risk_min is not None:
            filters['churn_risk_min'] = churn_risk_min
        if churn_risk_max is not None:
            filters['churn_risk_max'] = churn_risk_max
        
        # Use the new service method that returns data with count
        result = await analysis_service.get_analysis_results_with_count(
            limit=limit,
            offset=offset,
            **filters
        )
        
        logger.info(f"✅ Route: Returning {len(result.data)} analysis result records with total count: {result.count}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Route: Error getting analysis results: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching analysis results")

@router.get(
    "/{call_id}",
    response_model=BusinessLogicDtoGeneric[AllResultViewDto],
    summary="Retrieve an analysis result by Call ID",
    description="Fetches a single analysis result from the view using the call ID (primary key)."
)
async def get_analysis_result_by_call_id(
    call_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[AllResultViewDto]:
    """
    Retrieve an analysis result by its call ID (primary key).
    Args:
        call_id (UUID): The unique identifier of the call.
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[AnalysisResultViewDto]: A response containing the analysis result.
    """
    logger.info(f"🚀 Route: Getting analysis result by call ID: {call_id}")
    
    try:
        analysis_service = AllResultViewService(db)
        analysis_result = await analysis_service.get_analysis_result_by_call_id(call_id)
        
        if not analysis_result:
            logger.warning(f"❌ Route: No analysis result found for call ID: {call_id}")
            raise HTTPException(status_code=404, detail="Analysis result not found for the specified call")
        
        logger.info(f"✅ Route: Returning analysis result for call ID: {call_id}")
        return BusinessLogicDtoGeneric(
            data=analysis_result,
            is_success=True,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Route: Error getting analysis result by call ID {call_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while fetching analysis result")
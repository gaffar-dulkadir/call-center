from typing import List
import logging
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer import BusinessLogicDtoGeneric
from datalayer import get_db_session, BaseAnalysisResultDB
from datalayer import BaseAnalysisResultCreateDto, BaseAnalysisResultDto
from services import BaseResultService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/base-result", tags=["BASE_RESULT"])

@router.get(
    "/",
    response_model=BusinessLogicDtoGeneric[List[BaseAnalysisResultDto]],
    summary="Retrieve all base analysis results",
    description="Fetches a list of all base analysis results from the database."
)
async def get_base_analysis_results(
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[List[BaseAnalysisResultDto]]:
    """
    Retrieve all base analysis results.
    Args:
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[List[BaseAnalysisResultDto]]: A response containing a list of base analysis results.
    """
    logger.info("🚀 Route: Getting all base analysis results")
    
    base_result_service = BaseResultService(db)
    base_results = await base_result_service.get_all_base_analysis_results()
    
    logger.info(f"✅ Route: Returning {len(base_results)} base analysis results")
    return BusinessLogicDtoGeneric(
        data=base_results,
        is_success=True,
    )

@router.get(
    "/{result_id}",
    response_model=BusinessLogicDtoGeneric[BaseAnalysisResultDto],
    summary="Retrieve a base analysis result by ID",
    description="Fetches a single base analysis result from the database using its unique ID (primary key)."
)
async def get_base_analysis_result_by_id(
    result_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[BaseAnalysisResultDto]:
    """
    Retrieve a base analysis result by its primary key ID.
    Args:
        result_id (UUID): The unique identifier of the base analysis result.
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[BaseAnalysisResultDto]: A response containing the base analysis result.
    """
    logger.info(f"🚀 Route: Getting base analysis result by ID: {result_id}")
    
    base_result_service = BaseResultService(db)
    base_result = await base_result_service.get_base_analysis_result_by_id(result_id)
    
    if not base_result:
        logger.warning(f"❌ Route: No base analysis result found for ID: {result_id}")
        raise HTTPException(status_code=404, detail="Base analysis result not found")
    
    logger.info(f"✅ Route: Returning base analysis result for ID: {result_id}")
    return BusinessLogicDtoGeneric(
        data=base_result,
        is_success=True,
    )

@router.post(
    "/",
    response_model=BusinessLogicDtoGeneric[BaseAnalysisResultDto],
    summary="Create a new base analysis result",
    description="Creates a new base analysis result in the database based on the provided data."
)
async def create_base_analysis_result(
    base_analysis_result: BaseAnalysisResultCreateDto = Body(...),
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[BaseAnalysisResultDto]:
    """
    Create a new base analysis result.
    Args:
        base_analysis_result (BaseAnalysisResultCreateDto): The data for creating a new base analysis result.
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[BaseAnalysisResultDto]: A response containing the created base analysis result.
    """
    logger.info("🚀 Route: Creating new base analysis result")
    
    base_result_service = BaseResultService(db)
    base_result = await base_result_service.create_base_analysis_result(base_analysis_result)
    
    logger.info(f"✅ Route: Created base analysis result with ID: {base_result.id}")
    return BusinessLogicDtoGeneric(
        data=base_result,
        is_success=True,
    )
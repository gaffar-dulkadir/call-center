from typing import List
import logging
from uuid import UUID
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer import BusinessLogicDtoGeneric
from datalayer import get_db_session, CallDB
from datalayer import CallCreateDto, CallDto
from services import CallService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/call", tags=["CALL"])

@router.get(
    "/",
    response_model=BusinessLogicDtoGeneric[List[CallDto]],
    summary="Retrieve all calls",
    description="Fetches a list of all call records from the database."
)
async def get_calls(
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[List[CallDto]]:
    """
    Retrieve all call records.
    Args:
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[List[CallDto]]: A response containing a list of call records.
    """
    logger.info("🚀 Route: Getting all calls")
    
    call_service = CallService(db)
    calls = await call_service.get_all_calls()
    
    logger.info(f"✅ Route: Returning {len(calls)} call records")
    return BusinessLogicDtoGeneric(
        data=calls,
        is_success=True,
    )

@router.get(
    "/{call_id}",
    response_model=BusinessLogicDtoGeneric[CallDto],
    summary="Retrieve a call by ID",
    description="Fetches a single call record from the database using its unique ID (primary key)."
)
async def get_call_by_id(
    call_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[CallDto]:
    """
    Retrieve a call record by its primary key ID.
    Args:
        call_id (UUID): The unique identifier of the call record.
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[CallDto]: A response containing the call record.
    """
    logger.info(f"🚀 Route: Getting call by ID: {call_id}")
    
    call_service = CallService(db)
    call = await call_service.get_call_by_id(call_id)
    
    if not call:
        logger.warning(f"❌ Route: No call found for ID: {call_id}")
        raise HTTPException(status_code=404, detail="Call not found")
    
    logger.info(f"✅ Route: Returning call for ID: {call_id}")
    return BusinessLogicDtoGeneric(
        data=call,
        is_success=True,
    )

@router.post(
    "/",
    response_model=BusinessLogicDtoGeneric[CallDto],
    summary="Create a new call record",
    description="Creates a new call record in the database based on the provided data."
)
async def create_call(
    call: CallCreateDto = Body(...),
    db: AsyncSession = Depends(get_db_session),
) -> BusinessLogicDtoGeneric[CallDto]:
    """
    Create a new call record.
    Args:
        call (CallCreateDto): The data for creating a new call record.
        db (AsyncSession): Database session dependency.
    Returns:
        BusinessLogicDtoGeneric[CallDto]: A response containing the created call record.
    """
    logger.info("🚀 Route: Creating new call record")
    
    call_service = CallService(db)
    created_call = await call_service.create_call(call)
    
    logger.info(f"✅ Route: Created call record with ID: {created_call.id}")
    return BusinessLogicDtoGeneric(
        data=created_call,
        is_success=True,
    )
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from datalayer import CallDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class CallRepository(AsyncBaseRepository[CallDB]):
    """Repository for Call model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, CallDB)
    
    async def get_by_id(self, call_id: UUID) -> Optional[CallDB]:
        """Primary key (call_id) ile call getirir"""
        logger.info(f"Veritabanında call_id ile sorgu: {call_id}, tip: {type(call_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.call_id == call_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan call kayıt call_id: {db_model.call_id}")
        else:
            logger.warning(f"Call kayıt bulunamadı call_id: {call_id}")
            
        return db_model

    async def exists(self, call_id: UUID) -> bool:
        """Check if entity exists by call_id"""
        logger.info(f"Checking existence for call_id: {call_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.call_id == call_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using call_id"""
        from sqlalchemy import func
        
        logger.info(f"Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.call_id))
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                stmt = stmt.where(getattr(self.model_class, key) == value)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"Entity count: {count}")
        return count

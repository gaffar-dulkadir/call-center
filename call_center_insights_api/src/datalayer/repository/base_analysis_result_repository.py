from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from datalayer import BaseAnalysisResultDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class BaseAnalysisResultRepository(AsyncBaseRepository[BaseAnalysisResultDB]):
    """Repository for BaseAnalysisResult model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, BaseAnalysisResultDB)
    
    async def get_by_id(self, result_id: UUID) -> Optional[BaseAnalysisResultDB]:
        """Primary key (base_analysis_call_id) ile base analysis result getirir"""
        logger.info(f"Veritabanında result_id ile sorgu: {result_id}, tip: {type(result_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.base_analysis_call_id == result_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan result kayıt base_analysis_call_id: {db_model.base_analysis_call_id}")
        else:
            logger.warning(f"Result kayıt bulunamadı base_analysis_call_id: {result_id}")
            
        return db_model
    
    async def get_by_base_analysis_call_id(self, base_analysis_call_id: UUID) -> Optional[BaseAnalysisResultDB]:
        """Base analysis call ID ile result getirir"""
        logger.info(f"Veritabanında base_analysis_call_id ile sorgu: {base_analysis_call_id}, tip: {type(base_analysis_call_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.base_analysis_call_id == base_analysis_call_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan result kayıt base_analysis_call_id: {db_model.base_analysis_call_id}")
        else:
            logger.warning(f"Result kayıt bulunamadı base_analysis_call_id: {base_analysis_call_id}")
            
        return db_model

    async def exists(self, result_id: UUID) -> bool:
        """Check if entity exists by base_analysis_call_id"""
        logger.info(f"Checking existence for base_analysis_call_id: {result_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.base_analysis_call_id == result_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using base_analysis_call_id"""
        from sqlalchemy import func
        
        logger.info(f"Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.base_analysis_call_id))
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                stmt = stmt.where(getattr(self.model_class, key) == value)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"Entity count: {count}")
        return count
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from datalayer.model.schema_call_center_insight import TicketDetailsDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class TicketDetailsRepository(AsyncBaseRepository[TicketDetailsDB]):
    """Repository for TicketDetails model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, TicketDetailsDB)
    
    async def get_by_ticket_id(self, ticket_id: int) -> Optional[TicketDetailsDB]:
        """Primary key (ticket_id) ile ticket details getirir"""
        logger.info(f"Veritabanında ticket_id ile sorgu: {ticket_id}, tip: {type(ticket_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.ticket_id == ticket_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan ticket details kayıt ticket_id: {db_model.ticket_id}")
        else:
            logger.warning(f"Ticket details kayıt bulunamadı ticket_id: {ticket_id}")
            
        return db_model

    async def exists(self, ticket_id: int) -> bool:
        """Check if entity exists by ticket_id"""
        logger.info(f"Checking existence for ticket_id: {ticket_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.ticket_id == ticket_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using ticket_id"""
        from sqlalchemy import func
        
        logger.info(f"Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.ticket_id))
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                stmt = stmt.where(getattr(self.model_class, key) == value)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"Entity count: {count}")
        return count

    async def search_by_detail(self, search_term: str) -> list[TicketDetailsDB]:
        """Ticket detayı içinde arama yapar"""
        logger.info(f"Veritabanında detail ile sorgu: {search_term}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.ticket_detail.like(f"%{search_term}%"))
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan ticket details sayısı: {len(db_models)}")
        return db_models
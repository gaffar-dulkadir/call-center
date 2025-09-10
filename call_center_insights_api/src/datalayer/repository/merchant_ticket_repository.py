from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from datalayer.model.schema_call_center_insight import MerchantTicketDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class MerchantTicketRepository(AsyncBaseRepository[MerchantTicketDB]):
    """Repository for MerchantTicket model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, MerchantTicketDB)
    
    async def get_by_id(self, merchant_ticket_id: UUID) -> Optional[MerchantTicketDB]:
        """Primary key (merchant_ticket_id) ile merchant ticket getirir"""
        logger.info(f"Veritabanında merchant_ticket_id ile sorgu: {merchant_ticket_id}, tip: {type(merchant_ticket_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_ticket_id == merchant_ticket_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan merchant ticket kayıt merchant_ticket_id: {db_model.merchant_ticket_id}")
        else:
            logger.warning(f"Merchant ticket kayıt bulunamadı merchant_ticket_id: {merchant_ticket_id}")
            
        return db_model

    async def exists(self, merchant_ticket_id: UUID) -> bool:
        """Check if entity exists by merchant_ticket_id"""
        logger.info(f"Checking existence for merchant_ticket_id: {merchant_ticket_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.merchant_ticket_id == merchant_ticket_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using merchant_ticket_id"""
        from sqlalchemy import func
        
        logger.info(f"Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.merchant_ticket_id))
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                stmt = stmt.where(getattr(self.model_class, key) == value)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"Entity count: {count}")
        return count

    async def get_by_merchant_id(self, merchant_id: UUID) -> list[MerchantTicketDB]:
        """Merchant ID ile ticket listesi getirir"""
        logger.info(f"Veritabanında merchant_id ile sorgu: {merchant_id}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_id == merchant_id)
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan merchant ticket sayısı: {len(db_models)}")
        return db_models

    async def get_by_order_no(self, order_no: str) -> Optional[MerchantTicketDB]:
        """Sipariş numarası ile merchant ticket getirir"""
        logger.info(f"Veritabanında order_no ile sorgu: {order_no}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_ticket_order_no == order_no)
        )
        db_model = result.scalar_one_or_none()
        
        if db_model:
            logger.info(f"Bulunan merchant ticket kayıt: {db_model.merchant_ticket_order_no}")
        else:
            logger.warning(f"Merchant ticket kayıt bulunamadı: {order_no}")
            
        return db_model

    async def get_by_type_id(self, type_id: str) -> list[MerchantTicketDB]:
        """Ticket tip ID ile merchant ticket listesi getirir"""
        logger.info(f"Veritabanında type_id ile sorgu: {type_id}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_ticket_type_id == type_id)
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan merchant ticket sayısı: {len(db_models)}")
        return db_models
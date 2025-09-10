from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from datalayer.model.schema_call_center_insight import MerchantContactDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class MerchantContactRepository(AsyncBaseRepository[MerchantContactDB]):
    """Repository for MerchantContact model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, MerchantContactDB)
    
    async def get_by_contact_id(self, contact_id: int) -> Optional[MerchantContactDB]:
        """Primary key (contact_id) ile merchant contact getirir"""
        logger.info(f"Veritabanında contact_id ile sorgu: {contact_id}, tip: {type(contact_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.contact_id == contact_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan merchant contact kayıt contact_id: {db_model.contact_id}")
        else:
            logger.warning(f"Merchant contact kayıt bulunamadı contact_id: {contact_id}")
            
        return db_model

    async def exists(self, contact_id: int) -> bool:
        """Check if entity exists by contact_id"""
        logger.info(f"Checking existence for contact_id: {contact_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.contact_id == contact_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using contact_id"""
        from sqlalchemy import func
        
        logger.info(f"Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.contact_id))
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                stmt = stmt.where(getattr(self.model_class, key) == value)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"Entity count: {count}")
        return count

    async def get_by_merchant_id(self, merchant_id: int) -> list[MerchantContactDB]:
        """Merchant ID ile contact listesi getirir"""
        logger.info(f"Veritabanında merchant_id ile sorgu: {merchant_id}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_id == merchant_id)
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan merchant contact sayısı: {len(db_models)}")
        return db_models
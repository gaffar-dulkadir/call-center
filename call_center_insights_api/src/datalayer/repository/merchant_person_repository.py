from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from datalayer.model.schema_call_center_insight import MerchantPersonDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class MerchantPersonRepository(AsyncBaseRepository[MerchantPersonDB]):
    """Repository for MerchantPerson model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, MerchantPersonDB)
    
    async def get_by_merchant_id(self, merchant_id: UUID) -> Optional[MerchantPersonDB]:
        """Primary key (merchant_id) ile merchant person getirir"""
        logger.info(f"Veritabanında merchant_id ile sorgu: {merchant_id}, tip: {type(merchant_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_id == merchant_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan merchant person kayıt merchant_id: {db_model.merchant_id}")
        else:
            logger.warning(f"Merchant person kayıt bulunamadı merchant_id: {merchant_id}")
            
        return db_model

    async def exists(self, merchant_id: UUID) -> bool:
        """Check if entity exists by merchant_id"""
        logger.info(f"Checking existence for merchant_id: {merchant_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.merchant_id == merchant_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using merchant_id"""
        from sqlalchemy import func
        
        logger.info(f"Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.merchant_id))
        for key, value in filters.items():
            if hasattr(self.model_class, key):
                stmt = stmt.where(getattr(self.model_class, key) == value)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"Entity count: {count}")
        return count

    async def get_by_phone(self, phone: str) -> list[MerchantPersonDB]:
        """Telefon numarası ile merchant person listesi getirir"""
        logger.info(f"Veritabanında phone ile sorgu: {phone}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_person_phone == phone)
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan merchant person sayısı: {len(db_models)}")
        return db_models

    async def get_by_name(self, name: str) -> list[MerchantPersonDB]:
        """İsim ile merchant person listesi getirir"""
        logger.info(f"Veritabanında name ile sorgu: {name}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_person_name.like(f"%{name}%"))
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan merchant person sayısı: {len(db_models)}")
        return db_models
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from datalayer.model.schema_call_center_insight import MerchantDB
from datalayer.repository._base_repository import AsyncBaseRepository

import logging
logger = logging.getLogger(__name__)

class MerchantRepository(AsyncBaseRepository[MerchantDB]):
    """Repository for Merchant model"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(session, MerchantDB)
    
    async def get_all(self, limit=None, offset=None):
        """Override get_all to add debugging for NULL merchant_name values"""
        logger.info("🔍 Repository: Executing get_all query for merchant table")
        
        # Call parent get_all method
        results = await super().get_all(limit, offset)
        
        logger.info(f"🔍 Repository: Retrieved {len(results)} records from merchant table")
        
        # Debug each record for NULL values
        for i, record in enumerate(results):
            logger.debug(f"🔍 Repository Record {i+1}:")
            logger.debug(f"   merchant_id: {getattr(record, 'merchant_id', 'MISSING')}")
            logger.debug(f"   merchant_name: {repr(getattr(record, 'merchant_name', 'MISSING'))}")
            logger.debug(f"   merchant_inserted_at: {getattr(record, 'merchant_inserted_at', 'MISSING')}")
            
            # Alert on NULL merchant_name
            if getattr(record, 'merchant_name', None) is None:
                logger.error(f"❌ Repository: NULL merchant_name found in record {i+1} (ID: {getattr(record, 'merchant_id', 'UNKNOWN')})")
        
        return results
    
    async def get_by_id(self, merchant_id: UUID) -> Optional[MerchantDB]:
        """Primary key (merchant_id) ile merchant getirir"""
        logger.info(f"Veritabanında merchant_id ile sorgu: {merchant_id}, tip: {type(merchant_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_id == merchant_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"Bulunan merchant kayıt merchant_id: {db_model.merchant_id}")
        else:
            logger.warning(f"Merchant kayıt bulunamadı merchant_id: {merchant_id}")
            
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

    async def get_by_name(self, merchant_name: str) -> Optional[MerchantDB]:
        """Merchant name ile merchant getirir"""
        logger.info(f"Veritabanında merchant_name ile sorgu: {merchant_name}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_name == merchant_name)
        )
        db_model = result.scalar_one_or_none()
        
        if db_model:
            logger.info(f"Bulunan merchant kayıt: {db_model.merchant_name}")
        else:
            logger.warning(f"Merchant kayıt bulunamadı: {merchant_name}")
            
        return db_model

    async def get_by_city(self, city: str) -> list[MerchantDB]:
        """Şehir bazında merchant listesi getirir"""
        logger.info(f"Veritabanında city ile sorgu: {city}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.merchant_city == city)
        )
        db_models = result.scalars().all()
        
        logger.info(f"Bulunan merchant sayısı: {len(db_models)}")
        return db_models
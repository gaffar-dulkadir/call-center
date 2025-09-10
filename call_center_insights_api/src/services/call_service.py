import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer import CallMapper, CallDB
from datalayer.repository import CallRepository
from datalayer.model.dto import CallDto, CallCreateDto

logger = logging.getLogger(__name__)

class CallService:
    def __init__(self, db: AsyncSession):
        self.repository = CallRepository(db)
        self.mapper = CallMapper()
    
    async def get_all_calls(self) -> List[CallDto]:
        """
        Tüm call kayıtlarını alır ve DTO listesine dönüştürür.
        """
        logger.info("🚀 Service: getting all calls")
        
        # Repository'den DB modellerini çek ve DTO'lara dönüştürerek döndür
        db_models = await self.repository.get_all()
        return [self.mapper.to_dto(db_model) for db_model in db_models]
    
    async def list_calls(self) -> List[CallDto]:
        """Legacy method for backward compatibility"""
        return await self.get_all_calls()
    
    async def create_call(self, dto: CallCreateDto) -> CallDto:
        """
        Yeni bir call kaydı oluşturur.
        """
        logger.info(f"🚀 Service: creating new call")
        
        # DTO'yu DB modeline dönüştür, kaydet ve DTO olarak döndür
        db_model = self.mapper.to_db(dto)
        saved_db_model = await self.repository.save(db_model)
        return self.mapper.to_dto(saved_db_model)
    
    async def get_call_by_id(self, call_id: UUID) -> Optional[CallDto]:
        """
        Primary key (call_id) ile call getirir.
        """
        logger.info(f"🚀 Service: getting call by ID: {call_id}")
        
        db_model = await self.repository.get_by_id(call_id)
        
        if not db_model:
            logger.warning(f"Call bulunamadı ID: {call_id}")
            return None
            
        logger.info(f"✅ Call bulundu ID: {call_id}")
        return self.mapper.to_dto(db_model)
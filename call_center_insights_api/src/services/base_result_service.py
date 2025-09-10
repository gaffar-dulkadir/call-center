# services/base_result_service.py
import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer import BaseAnalysisResultDto, BaseAnalysisMapper, BaseAnalysisResultDB
from datalayer.repository import BaseAnalysisResultRepository
from datalayer.model.dto import BaseAnalysisResultDto, BaseAnalysisResultCreateDto

logger = logging.getLogger(__name__)

class BaseResultService:
    def __init__(self, db: AsyncSession):
        self.repository = BaseAnalysisResultRepository(db)
        self.mapper = BaseAnalysisMapper()
    
    async def get_all_base_analysis_results(self) -> List[BaseAnalysisResultDto]:
        """
        Tüm base analysis sonuçlarını alır ve DTO listesine dönüştürür.
        """
        logger.info("🚀 Service: getting all base analysis results")
        
        # Repository'den DB modellerini çek ve DTO'lara dönüştürerek döndür
        db_models = await self.repository.get_all()
        return [self.mapper.to_dto(db_model) for db_model in db_models]
    
    async def create_base_analysis_result(
        self, dto: BaseAnalysisResultCreateDto
    ) -> BaseAnalysisResultDto:
        """
        Yeni bir base analysis sonucu oluşturur.
        """
        logger.info(f"🚀 Service: creating new base analysis result")
        
        # DTO'yu DB modeline dönüştür, kaydet ve DTO olarak döndür
        db_model = self.mapper.to_db(dto)
        saved_db_model = await self.repository.save(db_model)
        return self.mapper.to_dto(saved_db_model)
    
    async def get_base_analysis_result_by_id(self, result_id: UUID) -> Optional[BaseAnalysisResultDto]:
        """
        Primary key (id) ile base analysis result getirir.
        """
        logger.info(f"🚀 Service: getting base analysis result by ID: {result_id}")
        
        db_model = await self.repository.get_by_id(result_id)
        
        if not db_model:
            logger.warning(f"Result bulunamadı ID: {result_id}")
            return None
            
        logger.info(f"✅ Result bulundu ID: {result_id}")
        return self.mapper.to_dto(db_model)
    
    async def get_base_analysis_result_by_call_id(self, call_id: UUID) -> Optional[BaseAnalysisResultDto]:
        """
        Base analysis call ID ile result getirir.
        """
        logger.info(f"🚀 Service: getting base analysis result by call ID: {call_id}")
        
        db_model = await self.repository.get_by_base_analysis_call_id(call_id)
        
        if not db_model:
            logger.warning(f"Result bulunamadı call ID: {call_id}")
            return None
            
        logger.info(f"✅ Result bulundu call ID: {call_id}")
        return self.mapper.to_dto(db_model)
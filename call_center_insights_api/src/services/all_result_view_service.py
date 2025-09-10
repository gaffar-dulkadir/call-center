# services/all_result_view_service.py
import logging
from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer.model.dto.all_result_view_dto import AllResultViewDto
from datalayer.model.dto.analysis_result_response_dto import AnalysisResultResponseDto
from datalayer.mapper.all_result_view_mapper import AllResultViewMapper
from datalayer.repository.all_result_view_repository import AllResultViewRepository

logger = logging.getLogger(__name__)

class AllResultViewService:
    """
    Read-only service for AnalysisResultView.
    Bu bir view olduğu için sadece SELECT işlemleri desteklenir.
    """
    
    def __init__(self, db: AsyncSession):
        self.repository = AllResultViewRepository(db)
        self.mapper = AllResultViewMapper()
    
    async def get_all_analysis_results(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[AllResultViewDto]:
        """
        Tüm analysis result view kayıtlarını alır ve DTO listesine dönüştürür.
        """
        logger.info("🚀 Service: getting all analysis result views")
        
        try:
            # Repository'den DB modellerini çek ve DTO'lara dönüştürerek döndür
            db_models = await self.repository.get_all(limit=limit, offset=offset)
            results = self.mapper.to_dto_list(db_models)
            
            logger.info(f"✅ Service: Retrieved {len(results)} analysis result view records")
            return results
            
        except Exception as e:
            logger.error(f"❌ Service: Error getting all analysis result views: {e}")
            raise

    async def get_analysis_result_by_call_id(self, call_id: UUID) -> Optional[AllResultViewDto]:
        """
        Call ID (primary key) ile analysis result view getirir.
        """
        logger.info(f"🚀 Service: getting analysis result view by call ID: {call_id}")
        
        try:
            db_model = await self.repository.get_by_call_id(call_id)
            
            if not db_model:
                logger.warning(f"❌ Analysis result view bulunamadı call ID: {call_id}")
                return None
                
            logger.info(f"✅ Analysis result view bulundu call ID: {call_id}")
            return self.mapper.to_dto(db_model)
            
        except Exception as e:
            logger.error(f"❌ Service: Error getting analysis result view by call ID {call_id}: {e}")
            raise

    async def get_filtered_analysis_results(self, **filters) -> List[AllResultViewDto]:
        """
        Filtreleme kriterlerine göre analysis result view kayıtlarını getirir.
        """
        logger.info(f"🚀 Service: getting filtered analysis result views with filters: {filters}")
        
        try:
            db_models = await self.repository.get_by_filter(**filters)
            results = self.mapper.to_dto_list(db_models)
            
            logger.info(f"✅ Service: Retrieved {len(results)} filtered analysis result view records")
            return results
            
        except Exception as e:
            logger.error(f"❌ Service: Error getting filtered analysis result views: {e}")
            raise

    async def count_analysis_results(self, **filters) -> int:
        """
        Filtreleme kriterlerine göre analysis result view kayıt sayısını döndürür.
        """
        logger.info(f"🚀 Service: counting analysis result views with filters: {filters}")
        
        try:
            count = await self.repository.count(**filters)
            
            logger.info(f"✅ Service: Analysis result view count: {count}")
            return count
            
        except Exception as e:
            logger.error(f"❌ Service: Error counting analysis result views: {e}")
            raise

    async def get_analysis_results_with_count(self, limit: Optional[int] = None, offset: Optional[int] = None, **filters) -> AnalysisResultResponseDto:
        """
        Tüm analysis result view kayıtlarını count ile birlikte döndürür.
        """
        logger.info(f"🚀 Service: getting analysis result views with count, filters: {filters}")
        
        try:
            # Filters varsa filtered query kullan, yoksa get_all kullan
            if filters:
                # Filtered query for data
                db_models = await self.repository.get_by_filter(**filters)
                # Apply pagination manually if needed
                if offset or limit:
                    start = offset or 0
                    end = start + limit if limit else None
                    paginated_models = db_models[start:end]
                else:
                    paginated_models = db_models
                
                # Count with same filters
                total_count = await self.repository.count(**filters)
            else:
                # No filters, use get_all with pagination
                db_models = await self.repository.get_all(limit=limit, offset=offset)
                paginated_models = db_models
                # Count all records
                total_count = await self.repository.count()
            
            # Convert to DTOs
            results = self.mapper.to_dto_list(paginated_models)
            
            logger.info(f"✅ Service: Retrieved {len(results)} analysis result records with total count: {total_count}")
            
            return AnalysisResultResponseDto(
                is_success=True,
                count=total_count,
                message=None,
                data=results
            )
            
        except Exception as e:
            logger.error(f"❌ Service: Error getting analysis result views with count: {e}")
            raise
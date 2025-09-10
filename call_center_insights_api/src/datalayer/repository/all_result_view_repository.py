from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, List
from datalayer.model.schema_call_center_insight.all_result_view_db import AllResultViewDB

import logging
logger = logging.getLogger(__name__)

class AllResultViewRepository:
    """
    Read-only repository for AnalysisResultView model.
    Bu bir view olduğu için sadece SELECT işlemleri desteklenir.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model_class = AllResultViewDB
    
    async def get_by_call_id(self, call_id: UUID) -> Optional[AllResultViewDB]:
        """Primary key (call_id) ile analysis result view getirir"""
        logger.info(f"🚀 Veritabanında call_id ile sorgu: {call_id}, tip: {type(call_id)}")
        
        result = await self.session.execute(
            select(self.model_class).where(self.model_class.call_id == call_id)
        )
        db_model = result.scalar_one_or_none()
        
        logger.debug(f"Sorgu sonucu: {db_model}")
        
        if db_model:
            logger.info(f"✅ Bulunan analysis result view kayıt call_id: {db_model.call_id}")
        else:
            logger.warning(f"❌ Analysis result view kayıt bulunamadı call_id: {call_id}")
            
        return db_model

    async def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[AllResultViewDB]:
        """Tüm analysis result view kayıtlarını getirir"""
        logger.info(f"🚀 Getting all analysis result view records with limit: {limit}, offset: {offset}")
        
        stmt = select(self.model_class)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)
            
        result = await self.session.execute(stmt)
        results = result.scalars().all()
        
        logger.info(f"✅ Found {len(results)} analysis result view records")
        return results

    async def get_by_filter(self, **filters) -> List[AllResultViewDB]:
        """Custom filtering methods for analysis results"""
        logger.info(f"🚀 Filtering analysis results with filters: {filters}")
        
        stmt = select(self.model_class)
        stmt = self._apply_filters(stmt, filters)
        
        result = await self.session.execute(stmt)
        results = result.scalars().all()
        
        logger.info(f"✅ Found {len(results)} analysis result view records matching filters")
        return results

    def _apply_filters(self, stmt, filters):
        """Apply all filter conditions to the statement"""
        from datetime import datetime
        
        for key, value in filters.items():
            if value is not None:
                if key == 'agent_name':
                    stmt = stmt.where(self.model_class.call_agent_name.ilike(f"%{value}%"))
                elif key == 'phone_number':
                    stmt = stmt.where(self.model_class.call_phone_number == value)
                elif key == 'follow_up_required':
                    stmt = stmt.where(self.model_class.base_analysis_call_requires_followup == value)
                elif key == 'reason_contains':
                    stmt = stmt.where(self.model_class.base_analysis_reason.ilike(f"%{value}%"))
                
                # Date range filters
                elif key == 'created_at_from':
                    try:
                        if 'T' not in value and ' ' not in value:
                            # If only date provided, add start of day
                            value += ' 00:00:00'
                        date_from = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        stmt = stmt.where(self.model_class.call_created_at >= date_from)
                    except ValueError as e:
                        logger.warning(f"⚠️ Invalid created_at_from date format: {value}, error: {e}")
                elif key == 'created_at_to':
                    try:
                        if 'T' not in value and ' ' not in value:
                            # If only date provided, add end of day
                            value += ' 23:59:59'
                        date_to = datetime.fromisoformat(value.replace('Z', '+00:00'))
                        stmt = stmt.where(self.model_class.call_created_at <= date_to)
                    except ValueError as e:
                        logger.warning(f"⚠️ Invalid created_at_to date format: {value}, error: {e}")
                
                # Numeric range filters
                elif key == 'duration_min':
                    stmt = stmt.where(self.model_class.call_duration >= value)
                elif key == 'duration_max':
                    stmt = stmt.where(self.model_class.call_duration <= value)
                elif key == 'agent_speech_rate_min':
                    stmt = stmt.where(self.model_class.call_agent_speech_rate >= value)
                elif key == 'agent_speech_rate_max':
                    stmt = stmt.where(self.model_class.call_agent_speech_rate <= value)
                elif key == 'customer_speech_rate_min':
                    stmt = stmt.where(self.model_class.call_customer_speech_rate >= value)
                elif key == 'customer_speech_rate_max':
                    stmt = stmt.where(self.model_class.call_customer_speech_rate <= value)
                elif key == 'silence_rate_min':
                    stmt = stmt.where(self.model_class.call_silence_rate >= value)
                elif key == 'silence_rate_max':
                    stmt = stmt.where(self.model_class.call_silence_rate <= value)
                elif key == 'cross_talk_rate_min':
                    stmt = stmt.where(self.model_class.call_cross_talk_rate >= value)
                elif key == 'cross_talk_rate_max':
                    stmt = stmt.where(self.model_class.call_cross_talk_rate <= value)
                elif key == 'agent_interrupt_count_min':
                    stmt = stmt.where(self.model_class.call_agent_interrupt_count >= value)
                elif key == 'agent_interrupt_count_max':
                    stmt = stmt.where(self.model_class.call_agent_interrupt_count <= value)
                elif key == 'churn_risk_min':
                    stmt = stmt.where(self.model_class.issue_analysis_churn_risk >= value)
                elif key == 'churn_risk_max':
                    stmt = stmt.where(self.model_class.issue_analysis_churn_risk <= value)
                
                else:
                    # Only use hasattr for unknown fields
                    if hasattr(self.model_class, key):
                        stmt = stmt.where(getattr(self.model_class, key) == value)
                    else:
                        logger.warning(f"⚠️ Unknown filter field: {key}")
        
        return stmt

    async def exists(self, call_id: UUID) -> bool:
        """Check if entity exists by call_id"""
        logger.info(f"🚀 Checking existence for call_id: {call_id}")
        
        result = await self.session.execute(
            select(1).where(self.model_class.call_id == call_id)
        )
        exists = result.scalar() is not None
        
        logger.debug(f"Entity exists: {exists}")
        return exists

    async def count(self, **filters) -> int:
        """Count entities with optional filters using call_id"""
        from sqlalchemy import func
        
        logger.info(f"🚀 Counting entities with filters: {filters}")
        
        stmt = select(func.count(self.model_class.call_id))
        stmt = self._apply_filters(stmt, filters)
        
        result = await self.session.execute(stmt)
        count = result.scalar()
        
        logger.debug(f"✅ Entity count: {count}")
        return count
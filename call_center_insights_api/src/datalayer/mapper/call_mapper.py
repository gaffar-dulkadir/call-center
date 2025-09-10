from datalayer import CallDB
from datalayer import CallDto, CallCreateDto

class CallMapper:
    
    @staticmethod
    def to_dto(db_model: CallDB) -> CallDto:
        return CallDto(
            id=db_model.call_id,
            agent_name=db_model.call_agent_name,
            phone_number=db_model.call_phone_number,
            duration=db_model.call_duration,
            agent_speech_rate=db_model.call_agent_speech_rate,
            customer_speech_rate=db_model.call_customer_speech_rate,
            silence_rate=db_model.call_silence_rate,
            cross_talk_rate=db_model.call_cross_talk_rate,
            agent_interrupt_count=db_model.call_agent_interrupt_count,
            created_at=db_model.call_created_at
        )

    @staticmethod
    def to_db(dto: CallCreateDto) -> CallDB:
        from datetime import datetime
        return CallDB(
            call_agent_name=dto.agent_name,
            call_phone_number=dto.phone_number,
            call_duration=dto.duration,
            call_agent_speech_rate=dto.agent_speech_rate,
            call_customer_speech_rate=dto.customer_speech_rate,
            call_silence_rate=dto.silence_rate,
            call_cross_talk_rate=dto.cross_talk_rate,
            call_agent_interrupt_count=dto.agent_interrupt_count,
            call_created_at=datetime.now()
        )
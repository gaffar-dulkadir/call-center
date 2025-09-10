from datalayer.model.schema_call_center_insight import TicketDetailsDB
from datalayer.model.dto import TicketDetailsDto, TicketDetailsCreateDto

class TicketDetailsMapper:
    
    @staticmethod
    def to_dto(db_model: TicketDetailsDB) -> TicketDetailsDto:
        return TicketDetailsDto(
            ticket_id=db_model.ticket_id,
            ticket_detail=db_model.ticket_detail
        )

    @staticmethod
    def to_db(dto: TicketDetailsCreateDto) -> TicketDetailsDB:
        return TicketDetailsDB(
            ticket_id=dto.ticket_id,
            ticket_detail=dto.ticket_detail
        )
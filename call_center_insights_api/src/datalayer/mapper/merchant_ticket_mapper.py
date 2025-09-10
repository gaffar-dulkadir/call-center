from datalayer.model.schema_call_center_insight import MerchantTicketDB
from datalayer.model.dto import MerchantTicketDto, MerchantTicketCreateDto

class MerchantTicketMapper:
    
    @staticmethod
    def to_dto(db_model: MerchantTicketDB) -> MerchantTicketDto:
        return MerchantTicketDto(
            id=db_model.merchant_ticket_id,
            merchant_id=db_model.merchant_id,
            merchant_ticket_order_no=db_model.merchant_ticket_order_no,
            merchant_ticket_type_id=db_model.merchant_ticket_type_id,
            merchant_ticket_time=db_model.merchant_ticket_time,
            merchant_ticket_kind_id=db_model.merchant_ticket_kind_id,
            merchant_ticket_sub_type_id=db_model.merchant_ticket_sub_type_id,
            merchant_ticket_explanation=db_model.merchant_ticket_explanation,
            merchant_ticket_first_explanation=db_model.merchant_ticket_first_explanation
        )

    @staticmethod
    def to_db(dto: MerchantTicketCreateDto) -> MerchantTicketDB:
        return MerchantTicketDB(
            merchant_id=dto.merchant_id,
            merchant_ticket_order_no=dto.merchant_ticket_order_no,
            merchant_ticket_type_id=dto.merchant_ticket_type_id,
            merchant_ticket_time=dto.merchant_ticket_time,
            merchant_ticket_kind_id=dto.merchant_ticket_kind_id,
            merchant_ticket_sub_type_id=dto.merchant_ticket_sub_type_id,
            merchant_ticket_explanation=dto.merchant_ticket_explanation,
            merchant_ticket_first_explanation=dto.merchant_ticket_first_explanation
        )
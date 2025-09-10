from datalayer.model.schema_call_center_insight import MerchantContactDB
from datalayer.model.dto import MerchantContactDto, MerchantContactCreateDto

class MerchantContactMapper:
    
    @staticmethod
    def to_dto(db_model: MerchantContactDB) -> MerchantContactDto:
        return MerchantContactDto(
            id=db_model.contact_id,
            merchant_id=db_model.merchant_id
        )

    @staticmethod
    def to_db(dto: MerchantContactCreateDto) -> MerchantContactDB:
        return MerchantContactDB(
            merchant_id=dto.merchant_id
        )
from datalayer.model.schema_call_center_insight import MerchantPersonDB
from datalayer.model.dto import MerchantPersonDto, MerchantPersonCreateDto

class MerchantPersonMapper:
    
    @staticmethod
    def to_dto(db_model: MerchantPersonDB) -> MerchantPersonDto:
        return MerchantPersonDto(
            merchant_id=db_model.merchant_id,
            merchant_person_state=str(db_model.merchant_person_state) if db_model.merchant_person_state is not None else None,
            merchant_person_name=db_model.merchant_person_name,
            merchant_person_phone=db_model.merchant_person_phone
        )

    @staticmethod
    def to_db(dto: MerchantPersonCreateDto) -> MerchantPersonDB:
        return MerchantPersonDB(
            merchant_id=dto.merchant_id,
            merchant_person_state=dto.merchant_person_state,
            merchant_person_name=dto.merchant_person_name,
            merchant_person_phone=dto.merchant_person_phone
        )
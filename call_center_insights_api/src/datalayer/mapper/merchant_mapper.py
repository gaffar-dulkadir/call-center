from datalayer.model.schema_call_center_insight import MerchantDB
from datalayer.model.dto import MerchantDto, MerchantCreateDto

class MerchantMapper:
    
    @staticmethod
    def to_dto(db_model: MerchantDB) -> MerchantDto:
        import logging
        logger = logging.getLogger(__name__)
        
        # Handle NULL merchant_name gracefully with default value
        merchant_name = db_model.merchant_name
        if merchant_name is None:
            merchant_name = "Unknown Merchant"
            logger.warning(f"⚠️  NULL merchant_name found for ID {db_model.merchant_id}, using default: '{merchant_name}'")
        
        # Handle invalid merchant_people data gracefully
        merchant_people = db_model.merchant_people
        if not isinstance(merchant_people, (int, type(None))):
            logger.warning(f"⚠️  Invalid merchant_people data type for ID {db_model.merchant_id}: {type(merchant_people)}, value: {repr(merchant_people)}")
            # If it's a list, try to get the count
            if isinstance(merchant_people, list):
                merchant_people = len(merchant_people)
                logger.info(f"🔧 Converted merchant_people list to count: {merchant_people}")
            else:
                merchant_people = None
        
        # Handle invalid merchant_ticket data gracefully (also receiving lists)
        merchant_ticket = db_model.merchant_ticket
        if not isinstance(merchant_ticket, (str, type(None))):
            logger.warning(f"⚠️  Invalid merchant_ticket data type for ID {db_model.merchant_id}: {type(merchant_ticket)}")
            if isinstance(merchant_ticket, list):
                merchant_ticket = f"[{len(merchant_ticket)} tickets]" if merchant_ticket else None
                logger.info(f"🔧 Converted merchant_ticket list to summary: {merchant_ticket}")
            else:
                merchant_ticket = str(merchant_ticket) if merchant_ticket is not None else None
        
        # Handle other potentially problematic string fields
        def safe_string_field(field_value, field_name):
            if field_value is None:
                return None
            elif isinstance(field_value, str):
                return field_value
            elif isinstance(field_value, list):
                logger.warning(f"⚠️  {field_name} contains list data for ID {db_model.merchant_id}")
                return f"[{len(field_value)} items]" if field_value else None
            else:
                return str(field_value)
        
        return MerchantDto(
            id=db_model.merchant_id,
            merchant_name=merchant_name,
            merchant_brand=safe_string_field(db_model.merchant_brand, "merchant_brand"),
            merchant_status=safe_string_field(db_model.merchant_status, "merchant_status"),
            merchant_city=safe_string_field(db_model.merchant_city, "merchant_city"),
            merchant_district=safe_string_field(db_model.merchant_district, "merchant_district"),
            merchant_address=safe_string_field(db_model.merchant_address, "merchant_address"),
            merchant_tax_no=safe_string_field(db_model.merchant_tax_no, "merchant_tax_no"),
            merchant_tax_office=safe_string_field(db_model.merchant_tax_office, "merchant_tax_office"),
            merchant_sector=safe_string_field(db_model.merchant_sector, "merchant_sector"),
            merchant_people=merchant_people,
            merchant_hardware=safe_string_field(db_model.merchant_hardware, "merchant_hardware"),
            merchant_fiscal_no=safe_string_field(db_model.merchant_fiscal_no, "merchant_fiscal_no"),
            merchant_service=safe_string_field(db_model.merchant_service, "merchant_service"),
            merchant_ticket=merchant_ticket,
            inserted_at=db_model.merchant_inserted_at
        )

    @staticmethod
    def to_db(dto: MerchantCreateDto) -> MerchantDB:
        from datetime import datetime
        return MerchantDB(
            merchant_name=dto.merchant_name,
            merchant_brand=dto.merchant_brand,
            merchant_status=dto.merchant_status,
            merchant_city=dto.merchant_city,
            merchant_district=dto.merchant_district,
            merchant_address=dto.merchant_address,
            merchant_tax_no=dto.merchant_tax_no,
            merchant_tax_office=dto.merchant_tax_office,
            merchant_sector=dto.merchant_sector,
            merchant_people=dto.merchant_people,
            merchant_hardware=dto.merchant_hardware,
            merchant_fiscal_no=dto.merchant_fiscal_no,
            merchant_service=dto.merchant_service,
            merchant_ticket=dto.merchant_ticket,
            merchant_inserted_at=datetime.now()
        )
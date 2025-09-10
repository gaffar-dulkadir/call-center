import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from datalayer.repository import (
    MerchantRepository, 
    MerchantPersonRepository, 
    MerchantContactRepository,
    MerchantTicketRepository,
    TicketDetailsRepository
)
from datalayer.mapper import (
    MerchantMapper,
    MerchantPersonMapper,
    MerchantContactMapper,
    MerchantTicketMapper,
    TicketDetailsMapper
)
from datalayer.model.dto.merchant_complete_dto import (
    MerchantCompleteDto,
    MerchantTicketWithDetailsDto,
    MerchantBatchRequestDto,
    MerchantBatchResponseDto
)

logger = logging.getLogger(__name__)

class MerchantUnifiedService:
    def __init__(self, db: AsyncSession):
        # Initialize all repositories
        self.merchant_repo = MerchantRepository(db)
        self.merchant_person_repo = MerchantPersonRepository(db)
        self.merchant_contact_repo = MerchantContactRepository(db)
        self.merchant_ticket_repo = MerchantTicketRepository(db)
        self.ticket_details_repo = TicketDetailsRepository(db)
        
        # Initialize all mappers
        self.merchant_mapper = MerchantMapper()
        self.merchant_person_mapper = MerchantPersonMapper()
        self.merchant_contact_mapper = MerchantContactMapper()
        self.merchant_ticket_mapper = MerchantTicketMapper()
        self.ticket_details_mapper = TicketDetailsMapper()
    
    async def get_merchant_complete_data(self, merchant_id: int) -> Optional[MerchantCompleteDto]:
        """
        Tek bir merchant_id için beş tablodan tüm veriyi getirir.
        """
        logger.info(f"🚀 Service: getting complete merchant data for ID: {merchant_id}")
        
        # 1. Merchant basic data
        merchant_db = await self.merchant_repo.get_by_id(merchant_id)
        if not merchant_db:
            logger.warning(f"Merchant bulunamadı ID: {merchant_id}")
            return None
        
        merchant_dto = self.merchant_mapper.to_dto(merchant_db)
        
        # 2. Merchant person data
        merchant_person_db = await self.merchant_person_repo.get_by_merchant_id(merchant_id)
        merchant_person_dto = None
        if merchant_person_db:
            merchant_person_dto = self.merchant_person_mapper.to_dto(merchant_person_db)
        
        # 3. Merchant contacts
        merchant_contacts_db = await self.merchant_contact_repo.get_by_merchant_id(merchant_id)
        contact_ids = [contact.contact_id for contact in merchant_contacts_db] if merchant_contacts_db else []
        
        # 4. Merchant tickets with details
        merchant_tickets_db = await self.merchant_ticket_repo.get_by_merchant_id(merchant_id)
        tickets_with_details = []
        
        for ticket_db in merchant_tickets_db:
            ticket_dto = self.merchant_ticket_mapper.to_dto(ticket_db)
            
            # Get ticket details
            ticket_details_db = await self.ticket_details_repo.get_by_ticket_id(ticket_db.merchant_ticket_id)
            ticket_detail = None
            if ticket_details_db:
                ticket_detail = ticket_details_db.ticket_detail
            
            # Create combined ticket with details DTO
            ticket_with_details = MerchantTicketWithDetailsDto(
                ticketId=ticket_dto.id,
                merchantTicketOrderNo=ticket_dto.merchant_ticket_order_no,
                merchantTicketTypeId=ticket_dto.merchant_ticket_type_id,
                merchantTicketTime=ticket_dto.merchant_ticket_time,
                merchantTicketKindId=ticket_dto.merchant_ticket_kind_id,
                merchantTicketSubTypeId=ticket_dto.merchant_ticket_sub_type_id,
                merchantTicketExplanation=ticket_dto.merchant_ticket_explanation,
                merchantTicketFirstExplanation=ticket_dto.merchant_ticket_first_explanation,
                ticketDetail=ticket_detail
            )
            tickets_with_details.append(ticket_with_details)
        
        # 5. Create complete DTO
        complete_dto = MerchantCompleteDto(
            merchantId=merchant_dto.id,
            merchantName=merchant_dto.merchant_name,
            merchantBrand=merchant_dto.merchant_brand,
            merchantStatus=merchant_dto.merchant_status,
            merchantCity=merchant_dto.merchant_city,
            merchantDistrict=merchant_dto.merchant_district,
            merchantAddress=merchant_dto.merchant_address,
            merchantTaxNo=merchant_dto.merchant_tax_no,
            merchantTaxOffice=merchant_dto.merchant_tax_office,
            merchantSector=merchant_dto.merchant_sector,
            merchantPeople=merchant_dto.merchant_people,
            merchantHardware=merchant_dto.merchant_hardware,
            merchantFiscalNo=merchant_dto.merchant_fiscal_no,
            merchantService=merchant_dto.merchant_service,
            merchantTicket=merchant_dto.merchant_ticket,
            merchantInsertedAt=merchant_dto.inserted_at,
            merchantPersonState=merchant_person_dto.merchant_person_state if merchant_person_dto else None,
            merchantPersonName=merchant_person_dto.merchant_person_name if merchant_person_dto else None,
            merchantPersonPhone=merchant_person_dto.merchant_person_phone if merchant_person_dto else None,
            contactIds=contact_ids if contact_ids else None,
            tickets=tickets_with_details if tickets_with_details else None
        )
        
        logger.info(f"✅ Complete merchant data assembled for ID: {merchant_id}")
        return complete_dto
    
    async def get_merchants_batch_data(self, request: MerchantBatchRequestDto) -> MerchantBatchResponseDto:
        """
        Birden fazla merchant_id için beş tablodan tüm veriyi getirir (batch işlem).
        """
        logger.info(f"🚀 Service: getting batch merchant data for {len(request.merchant_ids)} merchants")
        
        merchants = []
        for merchant_id in request.merchant_ids:
            merchant_data = await self.get_merchant_complete_data(merchant_id)
            if merchant_data:
                merchants.append(merchant_data)
        
        response = MerchantBatchResponseDto(
            merchants=merchants,
            totalCount=len(merchants)
        )
        
        logger.info(f"✅ Batch merchant data assembled for {len(merchants)} merchants")
        return response
    
    async def get_merchants_by_ids(self, merchant_ids: List[int]) -> List[MerchantCompleteDto]:
        """
        Birden fazla merchant_id için complete data listesi döner.
        """
        logger.info(f"🚀 Service: getting merchants by IDs: {merchant_ids}")
        
        merchants = []
        for merchant_id in merchant_ids:
            merchant_data = await self.get_merchant_complete_data(merchant_id)
            if merchant_data:
                merchants.append(merchant_data)
        
        return merchants
    
    async def get_merchant_by_phone(self, phone: str) -> Optional[MerchantCompleteDto]:
        """
        Telefon numarası ile merchant person tablosunu arar ve merchant_id'yi bularak
        tüm merchant verilerini getirir.
        """
        logger.info(f"🚀 Service: searching merchant by phone: {phone}")
        
        # 1. Telefon numarası ile merchant person ara
        merchant_persons = await self.merchant_person_repo.get_by_phone(phone)
        if not merchant_persons:
            logger.warning(f"Telefon numarası için merchant person bulunamadı: {phone}")
            return None
        
        # İlk bulunan merchant person'ı kullan (birden fazla olabilir)
        merchant_person = merchant_persons[0]
        merchant_id = merchant_person.merchant_id
        
        logger.info(f"📞 Phone {phone} için bulunan merchant_id: {merchant_id}")
        
        # 2. Merchant ID ile tüm verileri getir
        complete_data = await self.get_merchant_complete_data(merchant_id)
        
        if complete_data:
            logger.info(f"✅ Complete merchant data found for phone: {phone}")
        else:
            logger.warning(f"Merchant data bulunamadı phone: {phone}, merchant_id: {merchant_id}")
        
        return complete_data
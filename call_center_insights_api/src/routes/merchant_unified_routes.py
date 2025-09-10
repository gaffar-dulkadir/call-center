import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from services import MerchantUnifiedService
from datalayer.model.dto.merchant_complete_dto import (
    MerchantCompleteDto,
    MerchantBatchRequestDto,
    MerchantBatchResponseDto
)
from datalayer import get_db_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/merchants", tags=["Unified Merchants"])

@router.get("/complete/{merchant_id}", response_model=MerchantCompleteDto)
async def get_merchant_complete_data(
    merchant_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Tek bir merchant_id için beş tablodan (merchant, merchant_person, merchant_contact, 
    merchant_ticket, ticket_details) tüm veriyi getirir.
    
    Args:
        merchant_id: Merchant benzersiz ID'si
        
    Returns:
        MerchantCompleteDto: Konsolide merchant verisi
    """
    logger.info(f"🌐 Route: GET /merchants/complete/{merchant_id}")
    
    try:
        service = MerchantUnifiedService(db)
        result = await service.get_merchant_complete_data(merchant_id)
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"Merchant bulunamadı ID: {merchant_id}"
            )
        
        logger.info(f"✅ Route: Complete merchant data returned for ID: {merchant_id}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Route: Error getting complete merchant data for ID {merchant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/complete/batch", response_model=MerchantBatchResponseDto)
async def get_merchants_batch_data(
    request: MerchantBatchRequestDto,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Birden fazla merchant_id için beş tablodan tüm veriyi getirir (batch işlem).
    
    Args:
        request: Merchant ID'lerin listesini içeren request DTO
        
    Returns:
        MerchantBatchResponseDto: Birden fazla merchant verisi
    """
    logger.info(f"🌐 Route: POST /merchants/complete/batch with {len(request.merchant_ids)} IDs")
    
    try:
        if not request.merchant_ids:
            raise HTTPException(
                status_code=400, 
                detail="Merchant ID listesi boş olamaz"
            )
        
        if len(request.merchant_ids) > 100:  # Limit for performance
            raise HTTPException(
                status_code=400, 
                detail="Tek seferde maksimum 100 merchant sorgulanabilir"
            )
        
        service = MerchantUnifiedService(db)
        result = await service.get_merchants_batch_data(request)
        
        logger.info(f"✅ Route: Batch merchant data returned for {result.total_count} merchants")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Route: Error getting batch merchant data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/complete", response_model=List[MerchantCompleteDto])
async def get_merchants_by_ids(
    merchant_ids: List[int] = Query(..., description="Sorgulanacak merchant ID'lerin listesi"),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Query parameter olarak verilen birden fazla merchant_id için 
    beş tablodan tüm veriyi getirir.
    
    Args:
        merchant_ids: Query parameter olarak verilen merchant ID'lerin listesi
        
    Returns:
        List[MerchantCompleteDto]: Merchant verilerinin listesi
        
    Example:
        GET /merchants/complete?merchant_ids=1&merchant_ids=2&merchant_ids=3
    """
    logger.info(f"🌐 Route: GET /merchants/complete with IDs: {merchant_ids}")
    
    try:
        if not merchant_ids:
            raise HTTPException(
                status_code=400, 
                detail="En az bir merchant ID gereklidir"
            )
        
        if len(merchant_ids) > 100:  # Limit for performance
            raise HTTPException(
                status_code=400, 
                detail="Tek seferde maksimum 100 merchant sorgulanabilir"
            )
        
        service = MerchantUnifiedService(db)
        result = await service.get_merchants_by_ids(merchant_ids)
        
        logger.info(f"✅ Route: Complete merchant data returned for {len(result)} merchants")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Route: Error getting merchants by IDs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/search/phone/{phone}", response_model=MerchantCompleteDto)
async def get_merchant_by_phone(
    phone: str,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Telefon numarası ile merchant person tablosunu arar ve bulunan merchant_id için
    beş tablodan (merchant, merchant_person, merchant_contact, merchant_ticket, ticket_details)
    tüm veriyi getirir.
    
    Args:
        phone: Aranacak telefon numarası
        
    Returns:
        MerchantCompleteDto: Konsolide merchant verisi
        
    Example:
        GET /merchants/search/phone/5422147888
    """
    logger.info(f"🌐 Route: GET /merchants/search/phone/{phone}")
    
    try:
        if not phone or len(phone.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="Telefon numarası boş olamaz"
            )
        
        # Telefon numarasını temizle (sadece rakamlar)
        clean_phone = ''.join(filter(str.isdigit, phone))
        if len(clean_phone) < 10:
            raise HTTPException(
                status_code=400,
                detail="Geçerli bir telefon numarası giriniz"
            )
        
        # Türkiye telefon numarası formatını normalize et
        # +90 ile başlıyorsa veya 90 ile başlıyorsa, onu kaldır
        if clean_phone.startswith('90') and len(clean_phone) == 12:
            clean_phone = clean_phone[2:]  # 90 prefikisini kaldır
        elif clean_phone.startswith('0') and len(clean_phone) == 11:
            clean_phone = clean_phone[1:]  # 0 prefikisini kaldır
        
        service = MerchantUnifiedService(db)
        result = await service.get_merchant_by_phone(clean_phone)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Telefon numarası için merchant bulunamadı: {phone}"
            )
        
        logger.info(f"✅ Route: Merchant data found for phone: {phone}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Route: Error getting merchant by phone {phone}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
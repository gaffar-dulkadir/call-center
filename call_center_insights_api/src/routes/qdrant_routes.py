from typing import List
import logging
from fastapi import APIRouter, Body, HTTPException, Path
from datalayer import BusinessLogicDtoGeneric
from datalayer.model.dto import (
    QdrantSearchRequestDto,
    QdrantSearchResponseDto,
    QdrantTextSearchRequestDto,
    QdrantRecommendRequestDto,
    QdrantRecommendResponseDto,
    QdrantBatchSearchRequestDto,
    QdrantBatchSearchResponseDto,
    QdrantCollectionInfoDto,
    QdrantErrorDto,
)
from services import SearchApiService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/qdrant", tags=["QDRANT"])


@router.get(
    "/health",
    summary="Check Qdrant service health",
    description="Verify that Qdrant service is available and responding"
)
async def qdrant_health_check():
    """
    Check Qdrant service health status
    
    Returns:
        dict: Health status information
    """
    logger.info("🏥 Route: Checking Qdrant health")
    
    search_api_service = SearchApiService()
    
    try:
        health_data = await search_api_service.health_check()
        
        logger.info("✅ Route: Qdrant health check completed")
        return BusinessLogicDtoGeneric(
            data=health_data,
            is_success=True,
        )
            
    except Exception as e:
        logger.error(f"❌ Route: Qdrant health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Search API service unavailable: {e}")


@router.get(
    "/collections",
    response_model=BusinessLogicDtoGeneric[List[str]],
    summary="List all collections",
    description="Retrieve a list of all available collections in Qdrant"
)
async def list_collections():
    """
    List all available Qdrant collections
    
    Returns:
        BusinessLogicDtoGeneric[List[str]]: List of collection names
    """
    logger.info("📋 Route: Listing all Search API collections")
    
    search_api_service = SearchApiService()
    
    try:
        collections = await search_api_service.list_collections()
        
        logger.info(f"✅ Route: Found {len(collections)} collections")
        return BusinessLogicDtoGeneric(
            data=collections,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Failed to list collections: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list collections: {e}")


@router.get(
    "/collections/{collection_name}",
    response_model=BusinessLogicDtoGeneric[QdrantCollectionInfoDto],
    summary="Get collection information",
    description="Retrieve detailed information about a specific collection"
)
async def get_collection_info(
    collection_name: str = Path(..., description="Name of the collection")
):
    """
    Get information about a specific collection
    
    Args:
        collection_name: Name of the collection to get info for
        
    Returns:
        BusinessLogicDtoGeneric[QdrantCollectionInfoDto]: Collection information
    """
    logger.info(f"ℹ️ Route: Getting info for collection: {collection_name}")
    
    search_api_service = SearchApiService()
    
    try:
        collection_info = await search_api_service.get_collection_info(collection_name)
        
        logger.info(f"✅ Route: Retrieved info for collection: {collection_name}")
        return BusinessLogicDtoGeneric(
            data=collection_info,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Failed to get collection info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get collection info: {e}")


@router.post(
    "/collections/{collection_name}/search",
    response_model=BusinessLogicDtoGeneric[QdrantSearchResponseDto],
    summary="Search documents",
    description="Perform vector similarity search in the specified collection"
)
async def search_documents(
    collection_name: str = Path(..., description="Name of the collection to search"),
    search_request: QdrantSearchRequestDto = Body(..., description="Search parameters")
):
    """
    Perform vector similarity search in a collection
    
    Args:
        collection_name: Name of the collection to search
        search_request: Search parameters including vector, filters, etc.
        
    Returns:
        BusinessLogicDtoGeneric[QdrantSearchResponseDto]: Search results
    """
    logger.info(f"🔍 Route: Searching in collection: {collection_name}")
    
    search_api_service = SearchApiService()
    
    try:
        search_response = await search_api_service.search_documents(collection_name, search_request)
        
        logger.info(f"✅ Route: Search completed for collection: {collection_name}, found {len(search_response.results)} results")
        return BusinessLogicDtoGeneric(
            data=search_response,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Search failed in collection {collection_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {e}")


@router.post(
    "/collections/{collection_name}/search/recommend",
    response_model=BusinessLogicDtoGeneric[QdrantRecommendResponseDto],
    summary="Get document recommendations",
    description="Get document recommendations based on positive and negative examples"
)
async def recommend_documents(
    collection_name: str = Path(..., description="Name of the collection to search"),
    recommend_request: QdrantRecommendRequestDto = Body(..., description="Recommendation parameters")
):
    """
    Get document recommendations based on positive/negative examples
    
    Args:
        collection_name: Name of the collection to search
        recommend_request: Recommendation parameters including positive/negative examples
        
    Returns:
        BusinessLogicDtoGeneric[QdrantRecommendResponseDto]: Recommendation results
    """
    logger.info(f"🎯 Route: Getting recommendations from collection: {collection_name}")
    
    search_api_service = SearchApiService()
    
    try:
        recommend_response = await search_api_service.recommend_documents(collection_name, recommend_request)
        
        logger.info(f"✅ Route: Recommendations completed for collection: {collection_name}, found {len(recommend_response.results)} results")
        return BusinessLogicDtoGeneric(
            data=recommend_response,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Recommendation failed in collection {collection_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {e}")


@router.post(
    "/collections/{collection_name}/search/batch",
    response_model=BusinessLogicDtoGeneric[QdrantBatchSearchResponseDto],
    summary="Batch search documents",
    description="Perform multiple searches in a single request for better efficiency"
)
async def batch_search_documents(
    collection_name: str = Path(..., description="Name of the collection to search"),
    batch_request: QdrantBatchSearchRequestDto = Body(..., description="Batch search parameters")
):
    """
    Perform multiple searches in a single request
    
    Args:
        collection_name: Name of the collection to search
        batch_request: Batch search parameters containing multiple queries
        
    Returns:
        BusinessLogicDtoGeneric[QdrantBatchSearchResponseDto]: Batch search results
    """
    logger.info(f"📦 Route: Batch searching in collection: {collection_name} with {len(batch_request.queries)} queries")
    
    search_api_service = SearchApiService()
    
    try:
        batch_response = await search_api_service.batch_search_documents(collection_name, batch_request)
        
        logger.info(f"✅ Route: Batch search completed for collection: {collection_name}, found {batch_response.total} total results")
        
        return BusinessLogicDtoGeneric(
            data=batch_response,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Batch search failed in collection {collection_name}: {e}")
        raise HTTPException(status_code=500, detail=f"Batch search failed: {e}")


# Additional endpoints from schema

@router.post(
    "/collections/{collection_name}/search/text",
    response_model=BusinessLogicDtoGeneric[QdrantSearchResponseDto],
    summary="Text search",
    description="Perform text search in the specified collection"
)
async def text_search(
    collection_name: str = Path(..., description="Name of the collection to search"),
    search_request: QdrantTextSearchRequestDto = Body(..., description="Text search parameters")
):
    """
    Perform text search in a collection
    
    Args:
        collection_name: Name of the collection to search
        search_request: Text search parameters with required 'query' field
        
    Returns:
        BusinessLogicDtoGeneric[QdrantSearchResponseDto]: Search results
    """
    logger.info(f"🔍 Route: Text search in collection: {collection_name}")
    logger.info(f"🔍 DEBUG: Received text search request with query: '{search_request.query}'")
    logger.info(f"🔍 DEBUG: Request parameters: limit={search_request.limit}, score_threshold={search_request.score_threshold}")
    logger.info(f"🔍 DEBUG: Request payload will be: {search_request.model_dump(by_alias=True, exclude_none=True)}")
    
    search_api_service = SearchApiService()
    
    try:
        # Use the proper service method for text search
        search_response = await search_api_service.text_search_documents(collection_name, search_request)
        
        logger.info(f"✅ Route: Text search completed for collection: {collection_name}, found {len(search_response.results)} results")
        return BusinessLogicDtoGeneric(
            data=search_response,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Text search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Text search failed: {e}")


@router.post(
    "/search",
    response_model=BusinessLogicDtoGeneric[QdrantSearchResponseDto],
    summary="Simple search with collection name in body",
    description="Alternative search endpoint with collection name in request body"
)
async def simple_search(
    collection_name: str = Body(..., description="Collection name", embed=True),
    search_request: QdrantSearchRequestDto = Body(..., description="Search parameters")
):
    """
    Simple search endpoint with collection name in body
    
    Args:
        collection_name: Name of the collection to search (in body)
        search_request: Search parameters
        
    Returns:
        BusinessLogicDtoGeneric[QdrantSearchResponseDto]: Search results
    """
    logger.info(f"🔍 Route: Simple search in collection: {collection_name}")
    
    search_api_service = SearchApiService()
    
    try:
        search_response = await search_api_service.search_documents(collection_name, search_request)
        
        logger.info(f"✅ Route: Simple search completed for collection: {collection_name}")
        return BusinessLogicDtoGeneric(
            data=search_response,
            is_success=True,
        )
        
    except Exception as e:
        logger.error(f"❌ Route: Simple search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Simple search failed: {e}")
import logging
from typing import List, Optional, Union, Dict, Any
import aiohttp
import json
from config import Config
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
    QdrantPoint,
)

logger = logging.getLogger(__name__)


class SearchApiService:
    """Service class for interacting with Search API service on localhost:8083"""
    
    def __init__(self):
        self.config = Config()
        self.base_url = self.config.search_api_host
        # self.base_url = f"http://{self.config.search_api_host}:{self.config.search_api_port}" local için kullanım.

        self.timeout = 30.0
        
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Search API service
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request payload
            
        Returns:
            Dict: Response data
            
        Raises:
            Exception: On HTTP or connection errors
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Prepare headers
            headers = {
                "Content-Type": "application/json"
            }
            
            # Configure timeout
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                logger.info(f"🚀 Search API Request: {method} {url}")
                
                if method.upper() == "GET":
                    async with session.get(url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                elif method.upper() == "POST":
                    async with session.post(url, json=data, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                elif method.upper() == "PUT":
                    async with session.put(url, json=data, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                elif method.upper() == "DELETE":
                    async with session.delete(url, headers=headers) as response:
                        response.raise_for_status()
                        result = await response.json()
                elif method.upper() == "HEAD":
                    async with session.head(url, headers=headers) as response:
                        response.raise_for_status()
                        result = {}  # HEAD requests don't have response body
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                logger.info(f"✅ Search API Response: Status {response.status}")
                return result
                
        except aiohttp.ClientError as e:
            logger.error(f"❌ Search API connection error: {e}")
            raise Exception(f"Failed to connect to Search API: {e}")
        except aiohttp.ClientResponseError as e:
            error_text = ""
            try:
                error_text = await e.response.text() if hasattr(e, 'response') else str(e)
            except:
                error_text = str(e)
            logger.error(f"❌ Search API HTTP error: {e.status} - {error_text}")
            raise Exception(f"Search API error: {e.status} - {error_text}")
        except Exception as e:
            logger.error(f"❌ Unexpected Search API error: {e}")
            raise Exception(f"Unexpected error: {e}")

    async def search_documents(
        self, 
        collection_name: str, 
        search_request: QdrantSearchRequestDto
    ) -> QdrantSearchResponseDto:
        """
        Perform basic vector search via Search API service
        
        Args:
            collection_name: Name of the collection to search
            search_request: Search parameters
            
        Returns:
            QdrantSearchResponseDto: Search results
        """
        logger.info(f"🔍 Searching in collection: {collection_name}")
        
        endpoint = f"/collections/{collection_name}/search"
        
        # Convert DTO to snake_case format expected by external Search API
        payload = {
            "vector": search_request.vector,
            "limit": search_request.limit,
            "with_payload": search_request.with_payload,
            "with_vector": search_request.with_vector
        }
        
        # Only include score_threshold if it's set
        if search_request.score_threshold is not None:
            payload["score_threshold"] = search_request.score_threshold
            
        # Only include filters if they exist
        if search_request.filters is not None:
            payload["filters"] = search_request.filters
            
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            response_data = await self._make_request("POST", endpoint, payload)
            
            # Convert response to DTO - match schema format
            points = [QdrantPoint(**point) for point in response_data.get("results", [])]
            
            return QdrantSearchResponseDto(
                results=points,
                total=response_data.get("total", len(points)),
                executionTimeMs=response_data.get("executionTimeMs", 0.0),
                queryInfo=response_data.get("queryInfo", {})
            )
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise

    async def text_search_documents(
        self,
        collection_name: str,
        search_request: QdrantTextSearchRequestDto
    ) -> QdrantSearchResponseDto:
        """
        Perform text search via Search API service
        
        Args:
            collection_name: Name of the collection to search
            search_request: Text search parameters
            
        Returns:
            QdrantSearchResponseDto: Search results
        """
        logger.info(f"🔍 Text searching in collection: {collection_name} with query: '{search_request.query}'")
        logger.info(f"🔍 Parameters: limit={search_request.limit}, score_threshold={search_request.score_threshold}")
        
        endpoint = f"/collections/{collection_name}/search/text"
        
        # CRITICAL FIX: The external Search API expects snake_case field names according to schema
        # Convert from camelCase DTO to snake_case format expected by external API
        payload = {
            "query": search_request.query,
            "limit": search_request.limit,
            "with_payload": search_request.with_payload,
            "with_vector": search_request.with_vector
        }
        
        # Only include score_threshold if it's set
        if search_request.score_threshold is not None:
            payload["score_threshold"] = search_request.score_threshold
            
        # Only include filters if they exist
        if search_request.filters is not None:
            payload["filters"] = search_request.filters
            
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        logger.info(f"🚀 Text search payload (snake_case format) being sent to external API: {payload}")
        
        # DEBUG: Let's see what the external API is actually receiving
        logger.info(f"🔍 DEBUG Original request values:")
        logger.info(f"  - limit: {search_request.limit}")
        logger.info(f"  - score_threshold: {search_request.score_threshold}")
        logger.info(f"  - with_payload: {search_request.with_payload}")
        logger.info(f"  - with_vector: {search_request.with_vector}")
        
        # Validate critical parameters are present
        if search_request.limit is not None and search_request.limit <= 0:
            raise ValueError(f"Invalid limit value: {search_request.limit}. Must be > 0")
        if search_request.score_threshold is not None and (search_request.score_threshold < 0 or search_request.score_threshold > 1):
            raise ValueError(f"Invalid score_threshold value: {search_request.score_threshold}. Must be between 0 and 1")
        
        try:
            response_data = await self._make_request("POST", endpoint, payload)
            logger.info(f"✅ Text search API response: {response_data}")
            
            # Convert response to DTO - match schema format
            points = [QdrantPoint(**point) for point in response_data.get("results", [])]
            
            return QdrantSearchResponseDto(
                results=points,
                total=response_data.get("total", len(points)),
                executionTimeMs=response_data.get("executionTimeMs", 0.0),
                queryInfo=response_data.get("queryInfo", {})
            )
            
        except Exception as e:
            logger.error(f"❌ Text search failed: {e}")
            raise

    async def recommend_documents(
        self, 
        collection_name: str, 
        recommend_request: QdrantRecommendRequestDto
    ) -> QdrantRecommendResponseDto:
        """
        Get document recommendations based on positive/negative examples via Search API service
        
        Args:
            collection_name: Name of the collection to search
            recommend_request: Recommendation parameters
            
        Returns:
            QdrantRecommendResponseDto: Recommendation results
        """
        logger.info(f"🎯 Getting recommendations from collection: {collection_name}")
        
        endpoint = f"/collections/{collection_name}/search/recommend"
        
        # Convert DTO to snake_case format expected by external Search API
        payload = {
            "positive_ids": recommend_request.positive_ids,
            "limit": recommend_request.limit,
            "with_payload": recommend_request.with_payload,
            "with_vector": recommend_request.with_vector
        }
        
        # Only include optional fields if they're set
        if recommend_request.negative_ids is not None:
            payload["negative_ids"] = recommend_request.negative_ids
            
        if recommend_request.score_threshold is not None:
            payload["score_threshold"] = recommend_request.score_threshold
            
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        try:
            response_data = await self._make_request("POST", endpoint, payload)
            
            # Convert response to DTO - match schema format
            points = [QdrantPoint(**point) for point in response_data.get("results", [])]
            
            return QdrantRecommendResponseDto(
                results=points,
                total=response_data.get("total", len(points)),
                executionTimeMs=response_data.get("executionTimeMs", 0.0),
                queryInfo=response_data.get("queryInfo", {})
            )
            
        except Exception as e:
            logger.error(f"❌ Recommendation failed: {e}")
            raise

    async def batch_search_documents(
        self, 
        collection_name: str, 
        batch_request: QdrantBatchSearchRequestDto
    ) -> QdrantBatchSearchResponseDto:
        """
        Perform multiple searches in a single request via Search API service
        
        Args:
            collection_name: Name of the collection to search
            batch_request: Batch search parameters
            
        Returns:
            QdrantBatchSearchResponseDto: Batch search results
        """
        logger.info(f"📦 Batch searching in collection: {collection_name} with {len(batch_request.queries)} queries")
        
        endpoint = f"/collections/{collection_name}/search/batch"
        
        # Convert DTO to request payload
        payload = batch_request.model_dump(by_alias=True, exclude_none=True)
        
        try:
            response_data = await self._make_request("POST", endpoint, payload)
            
            # Convert response to DTO - match schema format
            batch_results = []
            for search_result in response_data.get("results", []):
                points = [QdrantPoint(**point) for point in search_result.get("results", [])]
                result_dto = QdrantSearchResponseDto(
                    results=points,
                    total=search_result.get("total", len(points)),
                    executionTimeMs=search_result.get("executionTimeMs", 0.0),
                    queryInfo=search_result.get("queryInfo", {})
                )
                batch_results.append(result_dto)
            
            return QdrantBatchSearchResponseDto(
                results=batch_results,
                total=sum(r.total for r in batch_results),
                executionTimeMs=response_data.get("executionTimeMs", 0.0)
            )
            
        except Exception as e:
            logger.error(f"❌ Batch search failed: {e}")
            raise

    async def get_collection_info(self, collection_name: str) -> QdrantCollectionInfoDto:
        """
        Get information about a collection via Search API service
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            QdrantCollectionInfoDto: Collection information
        """
        logger.info(f"ℹ️ Getting info for collection: {collection_name}")
        
        endpoint = f"/collections/{collection_name}"
        
        try:
            response_data = await self._make_request("GET", endpoint)
            
            # Match schema CollectionDto format
            return QdrantCollectionInfoDto(
                name=response_data.get("name", collection_name),
                vectorSize=response_data.get("vectorSize", 0),
                vectorsCount=response_data.get("vectorsCount", 0),
                distance=response_data.get("distance", "Cosine"),
                status=response_data.get("status", "unknown"),
                createdAt=response_data.get("createdAt"),
                description=response_data.get("description"),
                metadata=response_data.get("metadata")
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to get collection info: {e}")
            raise

    async def list_collections(self) -> List[str]:
        """
        List all available collections via Search API service
        
        Returns:
            List[str]: List of collection names
        """
        logger.info("📋 Listing all collections")
        
        endpoint = "/collections"
        
        try:
            response_data = await self._make_request("GET", endpoint)
            
            # Match schema - collections should be a list of collection names
            if isinstance(response_data, list):
                collection_names = [col.get("name", "") if isinstance(col, dict) else str(col) for col in response_data]
            else:
                collections = response_data.get("collections", response_data.get("result", []))
                collection_names = [col.get("name", "") if isinstance(col, dict) else str(col) for col in collections]
            
            logger.info(f"✅ Found {len(collection_names)} collections")
            return collection_names
            
        except Exception as e:
            logger.error(f"❌ Failed to list collections: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Check Qdrant service health - returns HealthStatusDto format
        
        Returns:
            Dict: Health status information matching schema
        """
        logger.info("🏥 Checking Qdrant service health")
        
        try:
            response_data = await self._make_request("GET", "/health")
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Qdrant health check failed: {e}")
            raise

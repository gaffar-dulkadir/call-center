from typing import List, Dict, Any, Optional, Union
from pydantic import Field
from .base_dto import BaseDto


# === COMMON MODELS ===

class QdrantFilter(BaseDto):
    """Qdrant filter model for query filtering"""
    must: Optional[List[Dict[str, Any]]] = Field(None, description="Must conditions")
    must_not: Optional[List[Dict[str, Any]]] = Field(None, description="Must not conditions", alias="mustNot")
    should: Optional[List[Dict[str, Any]]] = Field(None, description="Should conditions")


class QdrantPoint(BaseDto):
    """Qdrant point response model - matches schema SearchResultDto"""
    id: str = Field(..., description="Document ID")
    score: float = Field(..., description="Similarity score")
    vector: Optional[List[float]] = Field(None, description="Document vector")
    payload: Optional[Dict[str, Any]] = Field(None, description="Document payload")


# === SEARCH DTOs ===

class QdrantSearchRequestDto(BaseDto):
    """Search request matching schema SearchRequestDto"""
    vector: List[float] = Field(..., description="Query vector")
    limit: Optional[int] = Field(10, description="Max results", ge=1, le=1000)
    score_threshold: Optional[float] = Field(None, description="Minimum similarity score", alias="scoreThreshold")
    with_payload: Optional[bool] = Field(True, description="Include payload", alias="withPayload")
    with_vector: Optional[bool] = Field(False, description="Include vectors", alias="withVector")
    filters: Optional[Dict[str, Any]] = Field(None, description="Payload filters")


class QdrantSearchResponseDto(BaseDto):
    """Search response matching schema SearchResponseDto"""
    results: List[QdrantPoint] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")
    executionTimeMs: float = Field(..., description="Execution time in milliseconds")
    queryInfo: Dict[str, Any] = Field(..., description="Query information")


# === RECOMMENDATION DTOs ===

class QdrantRecommendRequestDto(BaseDto):
    """Recommendation request matching schema RecommendationRequestDto"""
    positive_ids: List[str] = Field(..., description="IDs of positive examples", alias="positiveIds")
    negative_ids: Optional[List[str]] = Field(None, description="IDs of negative examples", alias="negativeIds")
    limit: Optional[int] = Field(10, description="Max results", ge=1, le=1000)
    score_threshold: Optional[float] = Field(None, description="Minimum similarity score", alias="scoreThreshold")
    with_payload: Optional[bool] = Field(True, description="Include payload", alias="withPayload")
    with_vector: Optional[bool] = Field(False, description="Include vectors", alias="withVector")


class QdrantRecommendResponseDto(BaseDto):
    """Recommendation response - reuses SearchResponseDto format"""
    results: List[QdrantPoint] = Field(..., description="Recommendation results")
    total: int = Field(..., description="Total number of results")
    executionTimeMs: float = Field(..., description="Execution time in milliseconds")
    queryInfo: Dict[str, Any] = Field(..., description="Query information")


# === BATCH SEARCH DTOs ===

class QdrantBatchQueryDto(BaseDto):
    """Single query in batch search matching schema BatchSearchQueryDto"""
    vector: Optional[List[float]] = Field(None, description="Vector search query")
    query_text: Optional[str] = Field(None, description="Text search query", alias="queryText")
    limit: Optional[int] = Field(10, description="Max results for this query")


class QdrantBatchSearchRequestDto(BaseDto):
    """Batch search request matching schema BatchSearchRequestDto"""
    queries: List[QdrantBatchQueryDto] = Field(..., description="List of search queries", max_length=10)


class QdrantBatchSearchResponseDto(BaseDto):
    """Batch search response - returns multiple SearchResponseDto results"""
    results: List[QdrantSearchResponseDto] = Field(..., description="Batch search results")
    total: int = Field(..., description="Total results across all queries")
    executionTimeMs: float = Field(..., description="Total execution time in milliseconds")


# === TEXT SEARCH DTOs ===

class QdrantTextSearchRequestDto(BaseDto):
    """Text search request DTO"""
    query: str = Field(..., description="Text query to search for", min_length=1)
    limit: Optional[int] = Field(10, description="Max results", ge=1, le=1000)
    score_threshold: Optional[float] = Field(None, description="Minimum similarity score", alias="scoreThreshold")
    with_payload: Optional[bool] = Field(True, description="Include payload", alias="withPayload")
    with_vector: Optional[bool] = Field(False, description="Include vectors", alias="withVector")
    filters: Optional[Dict[str, Any]] = Field(None, description="Payload filters")


# === COLLECTION INFO DTOs ===

class QdrantCollectionInfoDto(BaseDto):
    """Collection information matching schema CollectionDto"""
    name: str = Field(..., description="Collection name")
    vectorSize: int = Field(..., description="Vector dimensions")
    vectorsCount: int = Field(..., description="Number of vectors")
    distance: str = Field(..., description="Distance metric: Cosine|Dot|Euclid")
    status: str = Field(..., description="Collection status: green|yellow|red")
    createdAt: Optional[str] = Field(None, description="Creation timestamp")
    description: Optional[str] = Field(None, description="Collection description")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


# === ERROR DTOs ===

class QdrantErrorDto(BaseDto):
    """Qdrant error response"""
    status: str = Field("error", description="Error status")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")


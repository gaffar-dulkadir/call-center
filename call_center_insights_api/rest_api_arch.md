# Call Center Insights API - REST API Architecture

## Overview

The Call Center Insights API is a FastAPI-based microservice designed for managing call center data and performing advanced search operations using vector databases. The API provides endpoints for call management, analysis results, intelligent document search capabilities, and unified merchant management.

## API Information

- **Title**: Call Center Insight with Swagger
- **Version**: 1.0.0
- **Base URL**: `http://localhost:8002`
- **Documentation**: 
  - Swagger UI: `/docs`
  - ReDoc: `/redoc`
  - OpenAPI Schema: `/openapi.json`

## Architecture Components

### 1. Core Framework
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Database**: PostgreSQL (async with SQLAlchemy)
- **Search Engine**: Qdrant Vector Database
- **API Documentation**: OpenAPI 3.0 with Swagger UI

### 2. Middleware & Configuration
- **CORS**: Enabled for all origins (development configuration)
- **Static Files**: Served from `/static` endpoint
- **Logging**: Structured logging with file and console output
- **Error Handling**: Global exception handler

### 3. Data Transfer Objects (DTOs)
All DTOs inherit from `BaseDto` with the following features:
- **Alias Generation**: Automatic camelCase conversion
- **Population**: Support for both field names and aliases
- **Attribute Mapping**: Direct mapping from SQLAlchemy models

## API Endpoints

### Health Check

#### GET /health
Check the health status of the API service.

**Response Model**: `HealthCheckDto`

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/health" \
  -H "accept: application/json"
```

---

## Call Management (`/call`)

### GET /call/
Retrieve all call records.

**Response Model**: `BusinessLogicDtoGeneric[List[CallDto]]`

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "agentName": "John Doe",
      "phoneNumber": "+1234567890",
      "duration": 120.5,
      "agentSpeechRate": 75.2,
      "customerSpeechRate": 65.8,
      "silenceRate": 10.5,
      "crossTalkRate": 5.2,
      "agentInterruptCount": 3,
      "createdAt": "2024-01-01T10:30:00Z"
    }
  ]
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/call/" \
  -H "accept: application/json"
```

### GET /call/{call_id}
Retrieve a specific call record by ID.

**Parameters**:
- `call_id` (path, UUID): The unique identifier of the call

**Response Model**: `BusinessLogicDtoGeneric[CallDto]`

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "agentName": "John Doe",
    "phoneNumber": "+1234567890",
    "duration": 120.5,
    "agentSpeechRate": 75.2,
    "customerSpeechRate": 65.8,
    "silenceRate": 10.5,
    "crossTalkRate": 5.2,
    "agentInterruptCount": 3,
    "createdAt": "2024-01-01T10:30:00Z"
  }
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/call/550e8400-e29b-41d4-a716-446655440000" \
  -H "accept: application/json"
```

### POST /call/
Create a new call record.

**Request Model**: `CallCreateDto`

**Request Body**:
```json
{
  "agentName": "John Doe",
  "phoneNumber": "+1234567890",
  "duration": 120.5,
  "agentSpeechRate": 75.2,
  "customerSpeechRate": 65.8,
  "silenceRate": 10.5,
  "crossTalkRate": 5.2,
  "agentInterruptCount": 3
}
```

**Response Model**: `BusinessLogicDtoGeneric[CallDto]`

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/call/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "agentName": "John Doe",
    "phoneNumber": "+1234567890",
    "duration": 120.5,
    "agentSpeechRate": 75.2,
    "customerSpeechRate": 65.8,
    "silenceRate": 10.5,
    "crossTalkRate": 5.2,
    "agentInterruptCount": 3
  }'
```

---

## Base Analysis Results (`/base-result`)

### GET /base-result/
Retrieve all base analysis results.

**Response Model**: `BusinessLogicDtoGeneric[List[BaseAnalysisResultDto]]`

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "callReason": "Technical Support",
      "callReasonDetail": "Customer experiencing connectivity issues with the service",
      "isFollowUpRequired": true
    }
  ]
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/base-result/" \
  -H "accept: application/json"
```

### GET /base-result/{result_id}
Retrieve a specific base analysis result by ID.

**Parameters**:
- `result_id` (path, UUID): The unique identifier of the analysis result

**Response Model**: `BusinessLogicDtoGeneric[BaseAnalysisResultDto]`

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/base-result/550e8400-e29b-41d4-a716-446655440001" \
  -H "accept: application/json"
```

### POST /base-result/
Create a new base analysis result.

**Request Model**: `BaseAnalysisResultCreateDto`

**Request Body**:
```json
{
  "callReason": "Technical Support",
  "callReasonDetail": "Customer experiencing connectivity issues with the service",
  "isFollowUpRequired": true
}
```

**Response Model**: `BusinessLogicDtoGeneric[BaseAnalysisResultDto]`

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/base-result/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "callReason": "Technical Support",
    "callReasonDetail": "Customer experiencing connectivity issues with the service",
    "isFollowUpRequired": true
  }'
```

---

## Analysis Results View (`/analysis-result`)

### GET /analysis-result/
Retrieve analysis results with advanced filtering and pagination.

**Query Parameters**:
- `limit` (integer, 1-1000): Maximum number of results
- `offset` (integer, ≥0): Number of results to skip
- `agent_name` (string): Filter by agent name (partial match)
- `phone_number` (string): Filter by phone number (exact match)
- `follow_up_required` (boolean): Filter by follow-up requirement
- `reason_contains` (string): Filter by call reason (partial match)
- `created_at_from` (string): Filter from date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
- `created_at_to` (string): Filter to date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)
- `duration_min` (float): Minimum call duration in seconds
- `duration_max` (float): Maximum call duration in seconds
- `agent_speech_rate_min` (float): Minimum agent speech rate percentage
- `agent_speech_rate_max` (float): Maximum agent speech rate percentage
- `customer_speech_rate_min` (float): Minimum customer speech rate percentage
- `customer_speech_rate_max` (float): Maximum customer speech rate percentage
- `silence_rate_min` (float): Minimum silence rate percentage
- `silence_rate_max` (float): Maximum silence rate percentage
- `cross_talk_rate_min` (float): Minimum cross talk rate percentage
- `cross_talk_rate_max` (float): Maximum cross talk rate percentage
- `agent_interrupt_count_min` (integer): Minimum agent interrupt count
- `agent_interrupt_count_max` (integer): Maximum agent interrupt count
- `churn_risk_min` (integer): Minimum churn risk level
- `churn_risk_max` (integer): Maximum churn risk level

**Response Model**: `AnalysisResultResponseDto`

**Example Response**:
```json
{
  "isSuccess": true,
  "count": 100,
  "message": null,
  "data": [
    {
      "callId": "550e8400-e29b-41d4-a716-446655440000",
      "agentName": "John Doe",
      "phoneNumber": "+1234567890",
      "duration": 120.5,
      "agentSpeechRate": 75.2,
      "customerSpeechRate": 65.8,
      "silenceRate": 10.5,
      "crossTalkRate": 5.2,
      "agentInterruptCount": 3,
      "createdAt": "2024-01-01T10:30:00Z",
      "baseAnalysisCallId": "550e8400-e29b-41d4-a716-446655440001",
      "callReason": "Technical Support",
      "callReasonDetail": "Customer experiencing connectivity issues",
      "isFollowUpRequired": true,
      "organizationMetadata": {},
      "issueAnalysisId": "550e8400-e29b-41d4-a716-446655440002",
      "issueSubCategory": "Network Issues",
      "subIssueType": "Connectivity",
      "churnRisk": 3,
      "urgencyLevel": "High",
      "relatedWithPreviousCall": false,
      "previousCallRelationDetail": null
    }
  ]
}
```

**cURL Examples**:

Basic request:
```bash
curl -X GET "http://localhost:8002/analysis-result/" \
  -H "accept: application/json"
```

With pagination:
```bash
curl -X GET "http://localhost:8002/analysis-result/?limit=50&offset=0" \
  -H "accept: application/json"
```

With filters:
```bash
curl -X GET "http://localhost:8002/analysis-result/?agent_name=John&follow_up_required=true&duration_min=60&duration_max=300" \
  -H "accept: application/json"
```

With date range filter:
```bash
curl -X GET "http://localhost:8002/analysis-result/?created_at_from=2024-01-01&created_at_to=2024-01-31" \
  -H "accept: application/json"
```

### GET /analysis-result/{call_id}
Retrieve analysis result by call ID.

**Parameters**:
- `call_id` (path, UUID): The unique call identifier

**Response Model**: `BusinessLogicDtoGeneric[AllResultViewDto]`

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/analysis-result/550e8400-e29b-41d4-a716-446655440000" \
  -H "accept: application/json"
```

---

## Qdrant Search Services (`/qdrant`)

### GET /qdrant/health
Check Qdrant service health status.

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/qdrant/health" \
  -H "accept: application/json"
```

### GET /qdrant/collections
List all available collections in Qdrant.

**Response Model**: `BusinessLogicDtoGeneric[List[str]]`

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": ["call_conversations", "customer_feedback", "agent_notes"]
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/qdrant/collections" \
  -H "accept: application/json"
```

### GET /qdrant/collections/{collection_name}
Get detailed information about a specific collection.

**Parameters**:
- `collection_name` (path, string): Name of the collection

**Response Model**: `BusinessLogicDtoGeneric[QdrantCollectionInfoDto]`

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": {
    "name": "call_conversations",
    "vectorSize": 1024,
    "vectorsCount": 50000,
    "distance": "Cosine",
    "status": "green",
    "createdAt": "2024-01-01T00:00:00Z",
    "description": "Call conversation embeddings",
    "metadata": {
      "type": "conversations",
      "language": "en"
    }
  }
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/qdrant/collections/call_conversations" \
  -H "accept: application/json"
```

### POST /qdrant/collections/{collection_name}/search
Perform vector similarity search in a collection.

**Parameters**:
- `collection_name` (path, string): Name of the collection

**Request Model**: `QdrantSearchRequestDto`

**Request Body**:
```json
{
  "vector": [0.1, 0.2, 0.3, ...],
  "limit": 10,
  "scoreThreshold": 0.7,
  "withPayload": true,
  "withVector": false,
  "filters": {
    "must": [
      {
        "key": "category",
        "match": {
          "value": "technical_support"
        }
      }
    ]
  }
}
```

**Response Model**: `BusinessLogicDtoGeneric[QdrantSearchResponseDto]`

**Example Response**:
```json
{
  "isSuccess": true,
  "message": null,
  "data": {
    "results": [
      {
        "id": "doc_123",
        "score": 0.95,
        "vector": [0.1, 0.2, 0.3],
        "payload": {
          "text": "Customer called about network connectivity issues",
          "category": "technical_support",
          "sentiment": "negative"
        }
      }
    ],
    "total": 1,
    "executionTimeMs": 25.5,
    "queryInfo": {
      "collection": "call_conversations",
      "limit": 10
    }
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/qdrant/collections/call_conversations/search" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "vector": [0.1, 0.2, 0.3, 0.4, 0.5],
    "limit": 10,
    "scoreThreshold": 0.7,
    "withPayload": true,
    "withVector": false,
    "filters": {
      "must": [
        {
          "key": "category",
          "match": {
            "value": "technical_support"
          }
        }
      ]
    }
  }'
```

### POST /qdrant/collections/{collection_name}/search/text
Perform text search in a collection.

**Parameters**:
- `collection_name` (path, string): Name of the collection

**Request Model**: `QdrantTextSearchRequestDto`

**Request Body**:
```json
{
  "query": "network connectivity problems",
  "limit": 10,
  "scoreThreshold": 0.5,
  "withPayload": true,
  "withVector": false,
  "filters": {}
}
```

**Response Model**: `BusinessLogicDtoGeneric[QdrantSearchResponseDto]`

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/qdrant/collections/call_conversations/search/text" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "network connectivity problems",
    "limit": 10,
    "scoreThreshold": 0.5,
    "withPayload": true,
    "withVector": false
  }'
```

### POST /qdrant/collections/{collection_name}/search/recommend
Get document recommendations based on positive and negative examples.

**Parameters**:
- `collection_name` (path, string): Name of the collection

**Request Model**: `QdrantRecommendRequestDto`

**Request Body**:
```json
{
  "positiveIds": ["doc_123", "doc_456"],
  "negativeIds": ["doc_789"],
  "limit": 10,
  "scoreThreshold": 0.5,
  "withPayload": true,
  "withVector": false
}
```

**Response Model**: `BusinessLogicDtoGeneric[QdrantRecommendResponseDto]`

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/qdrant/collections/call_conversations/search/recommend" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "positiveIds": ["doc_123", "doc_456"],
    "negativeIds": ["doc_789"],
    "limit": 10,
    "scoreThreshold": 0.5,
    "withPayload": true,
    "withVector": false
  }'
```

### POST /qdrant/collections/{collection_name}/search/batch
Perform multiple searches in a single request.

**Parameters**:
- `collection_name` (path, string): Name of the collection

**Request Model**: `QdrantBatchSearchRequestDto`

**Request Body**:
```json
{
  "queries": [
    {
      "vector": [0.1, 0.2, 0.3],
      "limit": 5
    },
    {
      "queryText": "billing issues",
      "limit": 5
    }
  ]
}
```

**Response Model**: `BusinessLogicDtoGeneric[QdrantBatchSearchResponseDto]`

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/qdrant/collections/call_conversations/search/batch" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      {
        "vector": [0.1, 0.2, 0.3, 0.4, 0.5],
        "limit": 5
      },
      {
        "queryText": "billing issues",
        "limit": 5
      }
    ]
  }'
```

### POST /qdrant/search
Alternative search endpoint with collection name in request body.

**Request Body**:
```json
{
  "collectionName": "call_conversations",
  "vector": [0.1, 0.2, 0.3],
  "limit": 10,
  "scoreThreshold": 0.5,
  "withPayload": true,
  "withVector": false,
  "filters": {}
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/qdrant/search" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "collectionName": "call_conversations",
    "vector": [0.1, 0.2, 0.3, 0.4, 0.5],
    "limit": 10,
    "scoreThreshold": 0.5,
    "withPayload": true,
    "withVector": false
  }'
```

---

## Unified Merchant Management (`/api/v1/merchants`)

The API provides a unified approach to merchant data management, consolidating information from five related tables (merchant, merchant_person, merchant_contact, merchant_ticket, ticket_details) into comprehensive endpoints.

### GET /api/v1/merchants/complete/{merchant_id}
Retrieve complete merchant data for a single merchant including all related information.

**Parameters**:
- `merchant_id` (path, integer): The unique identifier of the merchant

**Response Model**: `MerchantCompleteDto`

**Example Response**:
```json
{
  "merchantId": 123,
  "merchantName": "Example Store",
  "merchantBrand": "ExampleBrand",
  "merchantStatus": "active",
  "merchantCity": "Istanbul",
  "merchantDistrict": "Kadikoy",
  "merchantAddress": "Example Street 123",
  "merchantTaxNo": "1234567890",
  "merchantTaxOffice": "Kadikoy Tax Office",
  "merchantSector": "Retail",
  "merchantPeople": 50,
  "merchantHardware": "POS Terminal",
  "merchantFiscalNo": "123456",
  "merchantService": "Payment Processing",
  "merchantTicket": "Support",
  "merchantInsertedAt": "2024-01-01T10:30:00Z",
  "merchantPersonState": "active",
  "merchantPersonName": "John Doe",
  "merchantPersonPhone": "+905551234567",
  "contactIds": [789, 790],
  "tickets": [
    {
      "ticketId": 456,
      "merchantTicketOrderNo": 789,
      "merchantTicketTypeId": 1,
      "merchantTicketTime": "2024-01-01T15:30:00Z",
      "merchantTicketKindId": 2,
      "merchantTicketSubTypeId": 3,
      "merchantTicketExplanation": "Payment processing issue",
      "merchantTicketFirstExplanation": "Customer cannot complete payment",
      "ticketDetail": "Detailed explanation of the payment issue including error codes and customer actions taken"
    }
  ]
}
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/api/v1/merchants/complete/123" \
  -H "accept: application/json"
```

### POST /api/v1/merchants/complete/batch
Retrieve complete merchant data for multiple merchants in a single request.

**Request Model**: `MerchantBatchRequestDto`

**Request Body**:
```json
{
  "merchantIds": [123, 124, 125]
}
```

**Response Model**: `MerchantBatchResponseDto`

**Example Response**:
```json
{
  "merchants": [
    {
      "merchantId": 123,
      "merchantName": "Example Store",
      "merchantBrand": "ExampleBrand",
      // ... complete merchant data
    },
    {
      "merchantId": 124,
      "merchantName": "Another Store",
      "merchantBrand": "AnotherBrand",
      // ... complete merchant data
    }
  ],
  "totalCount": 2
}
```

**Limitations**:
- Maximum 100 merchants per batch request
- Empty merchant ID list will return 400 error

**cURL Example**:
```bash
curl -X POST "http://localhost:8002/api/v1/merchants/complete/batch" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "merchantIds": [123, 124, 125]
  }'
```

### GET /api/v1/merchants/complete
Retrieve complete merchant data for multiple merchants using query parameters.

**Query Parameters**:
- `merchant_ids` (query, List[int], required): List of merchant IDs to retrieve

**Response Model**: `List[MerchantCompleteDto]`

**Example Usage**:
```
GET /api/v1/merchants/complete?merchant_ids=123&merchant_ids=124&merchant_ids=125
```

**Limitations**:
- Maximum 100 merchants per request
- At least one merchant ID is required

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/api/v1/merchants/complete?merchant_ids=123&merchant_ids=124&merchant_ids=125" \
  -H "accept: application/json"
```

### GET /api/v1/merchants/search/phone/{phone}
Search for merchant by phone number and retrieve complete merchant data.

**Parameters**:
- `phone` (path, string): Phone number to search for

**Response Model**: `MerchantCompleteDto`

**Phone Number Format**:
- Supports various Turkish phone number formats
- Automatically normalizes phone numbers:
  - Removes country code (90) if present
  - Removes leading zero if present
- Minimum 10 digits required

**Example Phone Formats**:
- `5422147888` (recommended)
- `+905422147888`
- `905422147888`
- `05422147888`

**cURL Example**:
```bash
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/5422147888" \
  -H "accept: application/json"
```

---

## Error Handling

### Standard Error Response
All endpoints return errors in a consistent format:

```json
{
  "detail": "Error message",
  "error": "Detailed error information"
}
```

### Common HTTP Status Codes
- **200**: Success
- **400**: Bad Request (validation errors, missing parameters)
- **404**: Resource not found (Call not found, Analysis result not found, Merchant not found, etc.)
- **422**: Validation error (Invalid request parameters or body)
- **500**: Internal server error
- **503**: Service unavailable (for external dependencies like Qdrant)

### Error Examples

**404 Not Found**:
```bash
curl -X GET "http://localhost:8002/call/invalid-uuid" \
  -H "accept: application/json"
```

Response:
```json
{
  "detail": "Call not found"
}
```

**422 Validation Error**:
```bash
curl -X POST "http://localhost:8002/call/" \
  -H "Content-Type: application/json" \
  -d '{
    "agentName": "",
    "duration": -10
  }'
```

Response:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "agentName"],
      "msg": "String should have at least 1 character"
    },
    {
      "type": "greater_than_equal",
      "loc": ["body", "duration"],
      "msg": "Input should be greater than or equal to 0"
    }
  ]
}
```

**Merchant Not Found**:
```bash
curl -X GET "http://localhost:8002/api/v1/merchants/complete/99999" \
  -H "accept: application/json"
```

Response:
```json
{
  "detail": "Merchant bulunamadı ID: 99999"
}
```

**Phone Number Validation Error**:
```bash
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/123" \
  -H "accept: application/json"
```

Response:
```json
{
  "detail": "Geçerli bir telefon numarası giriniz"
}
```

## Data Models

### Core Business Logic Wrapper
All successful responses are wrapped in `BusinessLogicDtoGeneric`:

```json
{
  "isSuccess": boolean,
  "message": string | null,
  "data": T
}
```

### Field Naming Convention
- **Request Bodies**: Use camelCase (e.g., `agentName`, `phoneNumber`, `merchantIds`)
- **Database Fields**: Use snake_case internally
- **API Responses**: Automatically converted to camelCase via `BaseDto`

### Data Type Specifications
- **UUIDs**: Standard UUID format (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- **Timestamps**: ISO 8601 format (e.g., `2024-01-01T10:30:00Z`)
- **Percentages**: Float values 0-100
- **Durations**: Float values in seconds
- **Merchant IDs**: Integer values
- **Phone Numbers**: String format, normalized internally

### Unified Merchant Data Model
The `MerchantCompleteDto` consolidates data from multiple tables:

- **Merchant Basic Info**: Core merchant details (name, address, tax info, etc.)
- **Merchant Person**: Contact person information (name, phone, state)
- **Merchant Contacts**: List of contact IDs associated with the merchant
- **Merchant Tickets**: List of tickets with detailed information including ticket details

## Authentication & Authorization
Currently, the API does not implement authentication. This should be added for production deployment.

## Rate Limiting
No rate limiting is currently implemented. Consider adding rate limiting for production use.

## Deployment Configuration
- **Host**: `0.0.0.0`
- **Port**: `8002`
- **Reload**: Enabled (development)
- **Log Level**: `info`
- **Access Logs**: Enabled

## Dependencies
- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM (async)
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server
- **PostgreSQL**: Primary database
- **Qdrant**: Vector search engine

## Development Tools
- **Swagger UI**: Interactive API documentation at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **OpenAPI Schema**: Machine-readable schema at `/openapi.json`
- **CORS**: Enabled for frontend development
- **Hot Reload**: Automatic server restart on code changes

## Testing Examples

### Complete Workflow Example
```bash
# 1. Check API health
curl -X GET "http://localhost:8002/health"

# 2. Create a new call
CALL_RESPONSE=$(curl -X POST "http://localhost:8002/call/" \
  -H "Content-Type: application/json" \
  -d '{
    "agentName": "Jane Smith",
    "phoneNumber": "+1234567890",
    "duration": 180.0,
    "agentSpeechRate": 80.0,
    "customerSpeechRate": 70.0,
    "silenceRate": 8.0,
    "crossTalkRate": 4.0,
    "agentInterruptCount": 2
  }')

# Extract call ID from response (requires jq)
CALL_ID=$(echo $CALL_RESPONSE | jq -r '.data.id')

# 3. Get the created call
curl -X GET "http://localhost:8002/call/$CALL_ID"

# 4. Search for analysis results
curl -X GET "http://localhost:8002/analysis-result/?agent_name=Jane&limit=10"

# 5. Get complete merchant data
curl -X GET "http://localhost:8002/api/v1/merchants/complete/123"

# 6. Search merchant by phone
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/5422147888"

# 7. Get multiple merchants
curl -X GET "http://localhost:8002/api/v1/merchants/complete?merchant_ids=123&merchant_ids=124"

# 8. Batch request for merchants
curl -X POST "http://localhost:8002/api/v1/merchants/complete/batch" \
  -H "Content-Type: application/json" \
  -d '{"merchantIds": [123, 124, 125]}'

# 9. Check Qdrant health
curl -X GET "http://localhost:8002/qdrant/health"

# 10. List available collections
curl -X GET "http://localhost:8002/qdrant/collections"
```

### Unified Merchant Management Examples
```bash
# Single merchant complete data
curl -X GET "http://localhost:8002/api/v1/merchants/complete/123"

# Multiple merchants via query parameters
curl -X GET "http://localhost:8002/api/v1/merchants/complete?merchant_ids=123&merchant_ids=124"

# Multiple merchants via batch request
curl -X POST "http://localhost:8002/api/v1/merchants/complete/batch" \
  -H "Content-Type: application/json" \
  -d '{"merchantIds": [123, 124, 125]}'

# Search by phone number
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/5422147888"

# Test phone number normalization
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/+905422147888"
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/905422147888"
curl -X GET "http://localhost:8002/api/v1/merchants/search/phone/05422147888"
```

### Performance Testing
```bash
# Test API response time
curl -X GET "http://localhost:8002/analysis-result/?limit=1000" \
  -w "Time: %{time_total}s\n" \
  -o /dev/null \
  -s

# Test batch merchant retrieval performance
curl -X POST "http://localhost:8002/api/v1/merchants/complete/batch" \
  -H "Content-Type: application/json" \
  -d '{"merchantIds": [1,2,3,4,5,6,7,8,9,10]}' \
  -w "Time: %{time_total}s\n" \
  -o /dev/null \
  -s
```

## Key Changes in v1.0.0

### Unified Merchant Management
- **Consolidated Endpoints**: Replaced separate merchant, merchant_person, merchant_contact, merchant_ticket, and ticket_details endpoints with unified merchant management
- **Complete Data Retrieval**: Single endpoints now return comprehensive merchant data from all related tables
- **Improved Performance**: Reduced API calls needed to retrieve complete merchant information
- **Phone Number Search**: Direct search capability using phone numbers with automatic normalization
- **Batch Operations**: Support for retrieving multiple merchants in single requests

### Enhanced Data Models
- **MerchantCompleteDto**: Comprehensive DTO containing all merchant-related data
- **MerchantBatchRequestDto/ResponseDto**: Specialized DTOs for batch operations
- **MerchantTicketWithDetailsDto**: Combined ticket and ticket details information

### API Route Structure
- **New Base Path**: `/api/v1/merchants` for all unified merchant operations
- **RESTful Design**: Consistent endpoint patterns for different operations
- **Query Parameter Support**: Flexible data retrieval options

This unified approach provides better developer experience, improved performance, and simplified integration for client applications.
from datetime import datetime, timezone
import logging
import os
from fastapi.responses import JSONResponse

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from datalayer import HealthCheckDto, BaseAnalysisResultDB,IssueAnalysisResultDB,CallDB
from openapi_handler import OpenAPIHandler
from routes import (
    base_analysis_result_router,
    call_router,
    all_result_view_router,
    qdrant_router,
    merchant_unified_router
)

from logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Call Center Insight with Swagger",
    description="A production-ready FastAPI application with comprehensive Swagger documentation",
    version="1.0.0",
    contact={
        "name": "API Support Team",
        "url": "https://yourcompany.com/contact",
        "email": "support@yourcompany.com",
    },
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ---! Production'da spesifik origin'ler belirtilmeli
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Static files mounting (hata kontrolü ile)
static_dir = "static" if os.path.exists("static") else "src/static"
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"Static files mounted from: {static_dir}")
else:
    logger.warning(f"Static directory not found: {static_dir}")

# OpenAPI handler
try:
    handler = OpenAPIHandler(app)
    logger.info("OpenAPI handler initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAPI handler: {e}")

# Router'ları include et
try:
    app.include_router(base_analysis_result_router)
    app.include_router(call_router)
    app.include_router(all_result_view_router)
    app.include_router(qdrant_router)
    app.include_router(merchant_unified_router)  # Unified merchant endpoint
    logger.info("Routers included successfully")
except Exception as e:
    logger.error(f"Failed to include routers: {e}")

# Exception handler ekleyin
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)})
    # Database check function
    
    
# ---! Sağlık kontrolü endpoint'i
@app.get(
    "/health",
    response_model=HealthCheckDto,
    tags=["Health"],
    summary="Health Check",
    description="Check the health status of the API service",
)
async def health_check():
    """Heltcheck endpoint'i"""
    logger.info("Health check endpoint called")  # ---! Test logging
    return HealthCheckDto(
        status="healthy", timestamp=datetime.now(timezone.utc), version="1.0.0"
    )




if __name__ == "__main__":
    print("🚀 Server başlatılıyor...")
    print("📝 Loglar hem console'da hem de app.log dosyasında görünecek")
    print("🔧 Debug: Current working directory:", __import__("os").getcwd())
    print("🔧 Debug: __file__:", __file__)
    print("=" * 50)

    import uvicorn

    uvicorn.run(
        "app:app",  # ---! Import string olarak geçir - reload için gerekli
        host="0.0.0.0",
        port=8002,
        log_level="info",
        reload=True,
        access_log=True,
    )

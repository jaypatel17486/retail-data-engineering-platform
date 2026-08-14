from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fluxguard_api.database import (
    get_connection,
    release_connection,
)

from fluxguard_api.routes.transactions import (
    router as transactions_router,
)

from fluxguard_api.routes.fraud import (
    router as fraud_router,
)

from fluxguard_api.routes.analytics import (
    router as analytics_router,
)


# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="FluxGuard API",
    description=(
        "Real-Time E-Commerce Analytics "
        "& Fraud Detection Platform"
    ),
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================
# This will allow our frontend/dashboard to communicate
# with the API during local development.
#
# We will restrict this more when we deploy FluxGuard.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    transactions_router,
    prefix="/api/v1",
)

app.include_router(
    fraud_router,
    prefix="/api/v1",
)

app.include_router(
    analytics_router,
    prefix="/api/v1",
)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    """
    FluxGuard API root endpoint.
    """

    return {
        "name": "FluxGuard",
        "description": (
            "Real-Time E-Commerce Analytics "
            "& Fraud Detection Platform"
        ),
        "version": "1.0.0",
        "status": "running",
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    """
    Check whether the FluxGuard API and PostgreSQL
    database are available.
    """

    connection = None
    cursor = None

    try:
        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1;"
        )

        cursor.fetchone()

        return {
            "status": "healthy",
            "service": "fluxguard-api",
            "database": "connected",
        }

    except Exception as error:

        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from error

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            release_connection(connection)


# =========================================================
# APPLICATION INFORMATION
# =========================================================

@app.get("/api/v1/info")
def info():
    """
    Return basic information about FluxGuard.
    """

    return {
        "project": "FluxGuard",
        "version": "1.0.0",

        "platform": (
            "Real-Time E-Commerce Analytics "
            "& Fraud Detection"
        ),

        "components": [
            "Apache Kafka",
            "Apache Spark",
            "PostgreSQL",
            "FastAPI",
            "PyTorch",
        ],

        "fraud_detection": {
            "rule_engine": True,
            "machine_learning": True,
            "model": "PyTorch",
            "hybrid_detection": True,
        },
    }


# =========================================================
# LOCAL DEVELOPMENT
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "fluxguard_api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
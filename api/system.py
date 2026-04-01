import sys
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.storage.base import StorageAdapter
from core.adapters import get_storage
from core.database import get_db
from core.config import VERSION, ENV

router = APIRouter(tags=["System"])

@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    storage: StorageAdapter = Depends(get_storage)
):
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
        
    minio_ok = await storage.check_connection()
    minio_status = "ok" if minio_ok else "error"
    
    status_code = status.HTTP_200_OK if db_status == "ok" and minio_status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return {"status": "ok" if status_code == 200 else "error", "db": db_status, "minio": minio_status}

@router.get("/info")
async def info():
    return {
        "version": VERSION,
        "environment": ENV,
        "python_version": sys.version
    }

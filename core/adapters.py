from adapters.storage.base import StorageAdapter
from adapters.storage.s3 import S3StorageAdapter

from core.config import MINIO_URL, MINIO_BUCKET_NAME, MINIO_ACCESS_KEY, MINIO_SECRET_KEY

def get_storage() -> StorageAdapter:
    return S3StorageAdapter(
        url=MINIO_URL,
        bucket=MINIO_BUCKET_NAME,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY
    )

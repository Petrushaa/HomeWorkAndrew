import aioboto3
from botocore.exceptions import ClientError
from core.config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

class StorageService:
    def __init__(self):
        self.session = aioboto3.Session()

    async def upload_file(self, content: bytes, filename: str, content_type: str) -> str:
        async with self.session.client(
            "s3",
            endpoint_url=MINIO_URL,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name="us-east-1"
        ) as client:
            try:
                # Ensure bucket exists
                try:
                    await client.head_bucket(Bucket=MINIO_BUCKET_NAME)
                except ClientError:
                    await client.create_bucket(Bucket=MINIO_BUCKET_NAME)
                    
                await client.put_object(
                    Bucket=MINIO_BUCKET_NAME,
                    Key=filename,
                    Body=content,
                    ContentType=content_type
                )
                return f"{MINIO_URL}/{MINIO_BUCKET_NAME}/{filename}"
            except Exception as e:
                print(f"Error uploading file: {e}")
                raise e

    async def check_connection(self) -> bool:
        try:
            async with self.session.client(
                "s3",
                endpoint_url=MINIO_URL,
                aws_access_key_id=MINIO_ACCESS_KEY,
                aws_secret_access_key=MINIO_SECRET_KEY,
                region_name="us-east-1"
            ) as client:
                await client.list_buckets()
                return True
        except Exception:
            return False

import aioboto3
from botocore.exceptions import ClientError
from adapters.storage.base import StorageAdapter

class S3StorageAdapter(StorageAdapter):
    def __init__(self, url: str, bucket: str, access_key: str, secret_key: str):
        self.session = aioboto3.Session()
        self.url = url
        self.bucket = bucket
        self.access_key = access_key
        self.secret_key = secret_key

    async def upload_file(self, content: bytes, key: str, content_type: str) -> str:
        async with self.session.client(
            "s3",
            endpoint_url=self.url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="us-east-1"
        ) as client:
            try:
                # Ensure bucket exists
                try:
                    await client.head_bucket(Bucket=self.bucket)
                except ClientError:
                    await client.create_bucket(Bucket=self.bucket)
                    
                await client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=content,
                    ContentType=content_type
                )
                return f"{self.url}/{self.bucket}/{key}"
            except Exception as e:
                print(f"Error uploading file: {e}")
                raise e

    async def check_connection(self) -> bool:
        try:
            async with self.session.client(
                "s3",
                endpoint_url=self.url,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name="us-east-1"
            ) as client:
                await client.list_buckets()
                return True
        except Exception:
            return False

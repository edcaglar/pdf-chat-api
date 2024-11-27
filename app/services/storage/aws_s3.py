import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime

class S3Manager:
    def __init__(self, bucket_name: str, aws_access_key: str, aws_secret_key: str, region_name: str = "us-east-1"):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_content: bytes, file_name: str) -> str:

        # Kaydedilecek klasor pathi
        current_date = datetime.now()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%m")
        s3_key = f"{year}/{month}/{file_name}"

        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content
            )
            return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
        except NoCredentialsError as e:
            raise Exception("AWS kimlik bilgileri bulunamadı.") from e

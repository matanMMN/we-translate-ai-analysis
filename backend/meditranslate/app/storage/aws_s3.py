from io import BytesIO
import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError
from fastapi import UploadFile

from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.app.loggers import logger
from meditranslate.app.configurations import AWSConfig
from meditranslate.src.files.file_constants import FileStorageProvider

class AWSStorageService(BaseStorageService):

    def __init__(self, config: AWSConfig, base_url:str, bucket_name:str, is_testing:bool = False):
        super().__init__(FileStorageProvider.AWS_S3, base_url, bucket_name, is_testing)
        self.config = config
        s3_params = {
            "aws_access_key_id": self.config.aws_access_key_id,
            "aws_secret_access_key": self.config.aws_secret_access_key,
            "region_name": self.config.region_name,
        }

        if is_testing:
            s3_params.update({
                "endpoint_url": self.config.endpoint_url,
                "config": Config(signature_version='s3v4')
            })

        self.s3_resource = boto3.resource('s3',**s3_params)
        self.test_connection()
        bucket = self.get_bucket(self.bucket_name)
        if bucket is None:
            self.create_bucket(self.bucket_name)

    def get_bucket_list(self):
        buckets = self.s3_resource.meta.client.list_buckets()
        return buckets

    def test_connection(self):
        try:
            self.get_bucket_list()
            logger.info("Connected to S3 successfully!")
        except ClientError as e:
            logger.info(f"Error connecting to S3: {e}")
            raise Exception("Connection to S3 failed")


    def create_bucket(self,bucket_name:str):
        try:
            self.s3_resource.create_bucket(
                Bucket=bucket_name,
                # ACL='private'|'public-read'|'public-read-write'|'authenticated-read',
                CreateBucketConfiguration={
                    'LocationConstraint': 'eu-west-3',
                    # 'Location': {
                    #     'Type': 'AvailabilityZone',
                    #     'Name': 'string'
                    # },
                    # 'Bucket': {
                    #     'DataRedundancy': 'SingleAvailabilityZone',
                    #     'Type': 'Directory'
                    # }
                },
                # GrantFullControl='string',
                # GrantRead='string',
                # GrantReadACP='string',
                # GrantWrite='string',
                # GrantWriteACP='string',
                # ObjectLockEnabledForBucket=True|False,
                # ObjectOwnership='BucketOwnerPreferred'|'ObjectWriter'|'BucketOwnerEnforced'
                )
            logger.info(f"Created Bucket {bucket_name} in S3 successfully!")
        except ClientError as e:
            logger.info(f"Error Creating Bucket {bucket_name} in S3")
            raise e

    def get_bucket(self,bucket_name:str):
        try:
            return self.s3_resource.meta.client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            logger.error(f"Bucket '{bucket_name}' Does Not Exists")
            return None

    def create_file_path(self,file_path:str) -> str:
        # return f"s3://{self.bucket_name}/{file_path}"
        return file_path


    def upload_file(self, file: UploadFile, file_path: str):
        try:
            bucket = self.s3_resource.Bucket(self.bucket_name)
            file.file.seek(0)
            with file.file as f:
                bucket.upload_fileobj(f, file_path)
            return self.get_file(file_path)

        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise Exception(f"Failed to upload file: {e}")

    def get_file(self,file_path:str):
        try:
            file_data = self.s3_resource.meta.client.head_object(Bucket=self.bucket_name, Key=file_path)
            return file_data
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                logger.error(f"File does not exisits '{file_path}' file:  {e}")
            else:
                raise e
        return None

    def download_file(self, file_path:str):
        file_obj  = self.get_file(file_path)
        try:

            file_stream = file_obj.get()['Body']
            # file_stream = file_obj['Body']
            return file_stream
        except ClientError as e:
            logger.error(f"Error downloading '{file_path}' file:  {e}")
            raise Exception(f"Failed to getting file: {e}")

    def download_file_sync(self,file_path:str) -> BytesIO:
        file_stream = self.download_file(file_path)
        complete_file_io = BytesIO()
        while True:
            chunk = file_stream.read(1024)
            if not chunk:
                break
            complete_file_io.write(chunk)
        complete_file_io.seek(0)
        return complete_file_io

    def delete_file(self, file_path:str):
        file_obj = self.get_file(file_path)
        if file_obj is None:
            raise Exception("file cannot be deleted , it does not exists")
        try:
            file_obj = self.s3_resource.Object(self.bucket_name, file_path)
            file_obj.delete()  # Delete the file from S3
            logger.info(f"File {file_path} deleted successfully from bucket {self.bucket_name}.")
            return True
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")
            raise Exception(f"Failed to delete file: {e}")

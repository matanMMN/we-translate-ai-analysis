from abc import ABC, abstractmethod

from fastapi import UploadFile

from meditranslate.src.files.file_constants import FileStorageProvider

class BaseStorageService:

    def __init__(self,storage_provider:FileStorageProvider, base_url:str, bucket_name:str, is_testing:bool=False):
        super().__init__()
        self.storage_provider = storage_provider
        self.bucket_name = bucket_name
        self.base_url = base_url
        self.is_testing = is_testing

    def upload_file(self, file:UploadFile, file_path:str):
        """Uploads a file to the storage service."""
        raise NotImplementedError

    def download_file(self, file_path:str):
        """Downloads a file from the storage service."""
        raise NotImplementedError

    def delete_file(self, file_path:str):
        """Deletes a file from the storage service."""
        raise NotImplementedError

    def get_file(self, file_path:str):
        """Retrieves metadata for a file in the storage service."""
        raise NotImplementedError

    def create_file_path(self,file_path:str) -> str:
        raise NotImplementedError

    def test_connection():
        raise NotImplementedError

from abc import ABC, abstractmethod

class BaseStorageService(ABC):
    @abstractmethod
    def upload_file(self, file_data, filename):
        """Uploads a file to the storage service."""
        pass

    @abstractmethod
    def download_file(self, file_id):
        """Downloads a file from the storage service."""
        pass

    @abstractmethod
    def delete_file(self, file_id):
        """Deletes a file from the storage service."""
        pass

    @abstractmethod
    def get_file_metadata(self, file_id):
        """Retrieves metadata for a file in the storage service."""
        pass

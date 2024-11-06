import gridfs
from pymongo import MongoClient
import pymongo
from bson import ObjectId
import pymongo.errors
from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.app.loggers import logger

class MongoGridFSStorageService(BaseStorageService):
    def __init__(self, mongo_uri:str="mongodb://localhost:27017", database_name:str="mydatabase"):

        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[database_name]
            self.fs = gridfs.GridFS(self.db)

            self.client.admin.command('ping')  # Simple command to check connection
            logger.info("Connected to MongoDB successfully.")
        except pymongo.errors.ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred while connecting to MongoDB: {e}")
            raise

    def upload_file(self, file_data, filename):
        """
        Uploads a file to GridFS.

        :param file_data: Binary data of the file to upload
        :param filename: Name of the file to save in GridFS
        :return: ID of the stored file
        """
        file_id = self.fs.put(file_data, filename=filename)
        return str(file_id)

    def download_file(self, file_id):
        """
        Downloads a file from GridFS.

        :param file_id: The ID of the file to download
        :return: The binary content of the file
        """
        try:
            file = self.fs.get(ObjectId(file_id))
            return file.read()
        except gridfs.errors.NoFile:
            logger("File not found.")
            return None

    def delete_file(self, file_id):
        """
        Deletes a file from GridFS.

        :param file_id: The ID of the file to delete
        """
        try:
            self.fs.delete(ObjectId(file_id))
            logger(f"File with ID {file_id} has been deleted.")
        except gridfs.errors.NoFile:
            logger("File not found, nothing to delete.")

    def get_file_metadata(self, file_id):
        """
        Retrieves metadata of a file in GridFS.

        :param file_id: The ID of the file
        :return: Metadata dictionary for the file, or None if not found
        """
        try:
            file = self.fs.get(ObjectId(file_id))
            metadata = {
                "filename": file.filename,
                "upload_date": file.upload_date,
                "size": file.length,
                "content_type": file.content_type if hasattr(file, "content_type") else "unknown"
            }
            return metadata
        except gridfs.errors.NoFile:
            logger("File not found.")
            return None

    def __del__(self):
        if hasattr(self, 'client') and self.client:
            self.client.close()

import typing
from typing import List
import os
import shutil
import uuid
from datetime import datetime
from .filename import generate_unique_filename



class TempFileModel:
    def __init__(self, original_filename: str, filename: str, file_path: str, user_id: str, created_at: datetime) -> None:
        """
        Stores information about a temporary file.
        """
        self.original_filename = original_filename  # The original file name provided by the user
        self.filename = filename  # The system-generated unique file name
        self.file_path = file_path  # The full path where the file is stored
        self.user_id = user_id  # The ID of the user who uploaded the file
        self.created_at = created_at  # The timestamp when the file was created

    def __eq__(self, value: object) -> bool:
        if isinstance(value, TempFileModel):
            return (self.original_filename == value.original_filename and
                    self.filename == value.filename and
                    self.file_path == value.file_path)
        elif isinstance(value, str):
            return (self.original_filename == value or
                    self.filename == value or
                    self.file_path == value)
        return False

class TemporaryFileHandler:
    global_temp_files:List[TempFileModel] = []
    directory: str = "/tmp/files/"

    # -------- Instance Context --------

    def __init__(self, directory: str = "/tmp/files/"):
        """
        Initialize the handler with the directory where files will be temporarily stored.
        """
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        self.temp_files: List[TempFileModel] = []

    def save_file(self, file_data: bytes, filename: str, user_id: str) -> str:
        """
        Save the file with a unique name based on the user ID and a UUID.
        Returns the full path to the file.
        """
        unique_filename = generate_unique_filename(filename, user_id)
        file_path = os.path.join(self.directory, unique_filename)
        with open(file_path, "wb") as f:
            f.write(file_data)

        temp_file = TempFileModel(original_filename=filename, filename=unique_filename, file_path=file_path, user_id=user_id, created_at=datetime.now())
        self.temp_files.append(temp_file)
        return file_path

    def delete_instance_file(self, file_path: str) -> bool:
        """
        Delete a specific file from the filesystem and instance-level tracking.
        Returns True if successful, False if the file is not found.
        """
        temp_file = next((f for f in self.temp_files if f.file_path == file_path), None)
        if temp_file:
            if os.path.exists(file_path):
                os.remove(file_path)
            self.temp_files.remove(temp_file)
            return True
        return False

    def delete_all_instance_files(self):
        """
        Delete all files tracked by the instance and clear the list.
        """
        for temp_file in self.temp_files:
            if os.path.exists(temp_file.file_path):
                os.remove(temp_file.file_path)
        self.temp_files.clear()

    def get_instance_files(self) -> List[TempFileModel]:
        """
        Return the list of temp files tracked by this instance.
        """
        return self.temp_files

    def delete_temp_directory(self):
        """
        Remove the temporary directory and all its contents.
        """
        shutil.rmtree(self.directory, ignore_errors=True)

    # -------- Global Context --------

    @classmethod
    def save_global_file(cls, file_data: bytes, filename: str, user_id: str) -> str:
        """
        Save a file globally, accessible across all instances.
        """
        os.makedirs(cls.directory, exist_ok=True)
        unique_filename = generate_unique_filename(filename, user_id)
        file_path = os.path.join(cls.directory, unique_filename)
        with open(file_path, "wb") as f:
            f.write(file_data)

        temp_file = TempFileModel(original_filename=filename, filename=unique_filename, file_path=file_path, user_id=user_id, created_at=datetime.now())
        cls.global_temp_files.append(temp_file)
        return file_path

    @classmethod
    def delete_global_file(cls, file_path: str) -> bool:
        """
        Delete a specific file from the filesystem and global tracking.
        Returns True if successful, False if the file is not found.
        """
        temp_file = next((f for f in cls.global_temp_files if f.file_path == file_path), None)
        if temp_file:
            if os.path.exists(file_path):
                os.remove(file_path)
            cls.global_temp_files.remove(temp_file)
            return True
        return False

    @classmethod
    def delete_all_global_files(cls):
        """
        Delete all files tracked globally and clear the list.
        """
        for temp_file in cls.global_temp_files:
            if os.path.exists(temp_file.file_path):
                os.remove(temp_file.file_path)
        cls.global_temp_files.clear()

    @classmethod
    def get_global_files(cls) -> List[TempFileModel]:
        """
        Return the list of global temp files tracked by the class.
        """
        return cls.global_temp_files

    @classmethod
    def set_global_directory(cls,directory: str = "/tmp/files/") -> None:
        """
        Return the list of global temp files tracked by the class.
        """
        cls.directory = directory

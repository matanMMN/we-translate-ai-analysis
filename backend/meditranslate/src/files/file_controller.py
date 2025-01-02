from typing import Any, Dict, List,Tuple
from meditranslate.app.shared.base_controller import BaseController
from meditranslate.src.files.file_service import FileService
from meditranslate.src.files.file_schemas import (
    GetManySchema
)
from meditranslate.app.db.models import File
from meditranslate.app.db.transaction import Transactional,Propagation
from fastapi import UploadFile, BackgroundTasks

from meditranslate.src.users.user import User


class FileController(BaseController[File]):
    def __init__(self, file_service:FileService) -> None:
        super().__init__(File,file_service)
        self.file_service:FileService = file_service

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def upload_file(self,current_user:User,file:UploadFile, background_tasks:BackgroundTasks) -> File:
        return await self.file_service.upload_file(current_user,file, background_tasks=background_tasks)

    async def get_file(self,file_id: str) -> Dict[str, Any]:
        return await self.file_service.get_file(file_id)

    @Transactional(propagation=Propagation.REQUIRED_NEW)
    async def delete_file(self,file_id: str):
        return await self.file_service.delete_file(file_id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_file(self,current_user:User,file_id: str,file:UploadFile):
        return await self.file_service.update_file(current_user,file_id,file)

    async def get_many_files(self,files_get_many_schema:GetManySchema) -> Tuple[List[File],int]:
        return await self.file_service.get_many_files(files_get_many_schema)

    async def download_file(self,file_id:str):
        return await self.file_service.download_file(file_id=file_id)

    async def get_file_versions(self, file_id: str):
        return await self.file_service.get_file_versions(file_id=file_id)
    
    async def get_specific_version(self, file_id: str, version_number: int):
        return await self.file_service.get_specific_version(file_id=file_id, version_number=version_number)
    
    async def restore_version(self, file_id: str, version_number: int, current_user: User):
        return await self.file_service.restore_version(file_id=file_id, version_number=version_number, current_user=current_user)


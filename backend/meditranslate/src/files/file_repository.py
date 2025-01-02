from typing import List
from sqlalchemy import and_, select
from meditranslate.src.files.file import File, FileVersion
from meditranslate.app.db.base_repository import BaseRepository
from meditranslate.src.files.file_version_schemas import FileVersionCreateSchema

class FileRepository(BaseRepository[File]):
    def __init__(self, db_session):
        super().__init__(File, db_session)

    async def create_version(self, version_data: FileVersionCreateSchema) -> FileVersion:
        """Creates a new file version"""
        try:
            # Use the create method from BaseRepository
            version = await self.create(version_data.model_dump())
            await self.session.flush()
            return version
        except Exception as e:
            print(f"Error creating file version: {e}")
            raise

    async def get_versions(self, file_id: str) -> List[FileVersion]:
        """Get all versions of a file"""
        query = select(FileVersion).where(FileVersion.file_id == file_id).order_by(FileVersion.version_number.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_version(self, file_id: str, version_number: int) -> FileVersion:
        """Get a specific version of a file"""
        query = select(FileVersion).where(
            and_(
                FileVersion.file_id == file_id,
                FileVersion.version_number == version_number
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
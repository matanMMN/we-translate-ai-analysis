from meditranslate.app.storage.base_storage_service import BaseStorageService
from meditranslate.app.storage.mongo_grid_fs import MongoGridFSStorageService
from meditranslate.app.configurations import config

file_storage_service:BaseStorageService = MongoGridFSStorageService(
    mongo_uri=str(config.FILE_STORAGE_URL),
    database_name=str(config.FILE_STORAGE_NAME),
)

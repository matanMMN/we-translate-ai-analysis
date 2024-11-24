from enum import Enum
from meditranslate.utils.files.file_size_unit import FileSizeUnit
from meditranslate.utils.files.file_format_type import FileFormatType





class FileStorageProvider(str,Enum):
    MONGO_GRID_FS = "mongodb_grid_fs"
    LOCAL = "local"
    AWS_S3 = "aws_s3"

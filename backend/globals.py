import os
import sys
import logging
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
CLI_DIVIDER = f"-" * 100

# logging.getLogger('pymongo').setLevel(logging.WARNING)
# logging.getLogger('urllib3').setLevel(logging.WARNING)

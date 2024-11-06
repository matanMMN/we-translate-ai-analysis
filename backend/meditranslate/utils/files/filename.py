import re
import uuid
from datetime import datetime

MAX_FILENAME_LENGTH = 255

def get_extension_from_filename(filename: str) -> str:
    """
    Extract the file extension from a filename.
    Returns an empty string if no extension is found.
    """
    split = filename.rsplit('.', 1)  # Split on the last dot only
    if len(split) == 2:
        return split[1]  # Return the part after the last dot
    return ''  # No extension found

def get_name_from_filename(filename: str) -> str:
    """
    Extract the name part (without the extension) from a filename.
    Returns the full filename if no extension is found.
    """
    split = filename.rsplit('.', 1)  # Split on the last dot only
    if len(split) == 2:
        return split[0]  # Return the part before the last dot
    return filename  # No extension found, return the full filename

def normalize_filename(filename: str) -> str:
    """
    Normalize the filename to make it safe for use.
    - Remove any unwanted characters.
    - Replace spaces with underscores.
    - Convert to lowercase.
    - Truncate to a maximum filename length.
    """
    # Remove any unwanted characters
    filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Convert to lowercase
    filename = filename.lower()
    # Truncate to the maximum filename length
    return filename[:MAX_FILENAME_LENGTH]

def generate_unique_filename(filename: str, user_id: str) -> str:
    """
    Generate a unique filename using the user's ID, current timestamp, and a UUID.
    The original filename is normalized for security reasons.
    """
    # Get file extension and normalize the filename
    ext = get_extension_from_filename(filename)
    normal_filename = normalize_filename(get_name_from_filename(filename))
    
    # Ensure there's an extension
    file_extension = f".{ext}" if ext else ".tmp"
    
    # Generate a UUID and timestamp for uniqueness
    unique_id = uuid.uuid4()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Construct the unique filename
    unique_filename = f"{normal_filename}_{user_id}_{timestamp}_{unique_id}{file_extension}"
    
    return unique_filename

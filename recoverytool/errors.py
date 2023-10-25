# errors.py

class DiskRecoveryError(Exception):
    """Custom exception for DiskRecoveryTool errors."""
    pass


class FilesystemNotFoundError(DiskRecoveryError):
    """Exception raised when a filesystem is not detected."""
    pass


class FileRecoveryError(DiskRecoveryError):
    """Exception raised during file recovery processes."""
    pass

# ... You can add more custom exceptions here if needed in the future ...

import hashlib
import logging
import os
import re

# Professional Logging Configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("pybnafar")


def sanitize_filename(filename: str) -> str:
    """Protects against Path Traversal and invalid characters."""
    base_name = os.path.basename(filename)
    return re.sub(r"[^a-zA-Z0-9._-]", "_", base_name)


def validate_path(path: str, base_dir: str):
    """Ensures file operations stay within the designated workspace."""
    absolute_base = os.path.abspath(base_dir)
    absolute_path = os.path.abspath(path)
    if not absolute_path.startswith(absolute_base):
        raise PermissionError(f"Access denied outside of workspace: {path}")


def calculate_hash(file_path: str) -> str:
    """Calculates SHA256 for public data integrity auditing."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
